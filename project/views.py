# File: views.py
# Name: Nicholas Sima (nicksima@bu.edu)
# Description: views file for the university tracker project app

from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy

import plotly.graph_objects as go
from plotly.offline import plot
from django.db.models import Count, F

from .models import *
from .forms import (
    CreateStudentForm, UpdateStudentForm,
    CreateProfessorForm, UpdateProfessorForm,
    CreateDormForm, UpdateDormForm,
    CreateDepartmentForm, UpdateDepartmentForm,
)

# Create your views here.


class ProjectLoginRequiredMixin(LoginRequiredMixin):
    '''Restrict views to any logged-in User'''

    def get_login_url(self):
        return reverse('login')


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    '''Restrict a view to logged-in admin Users'''

    def get_login_url(self):
        return reverse('login')

    def test_func(self):
        return Admin.objects.filter(user=self.request.user).exists()


class AdminContextMixin:
    '''Add an `is_admin` flag to the context so templates can show admin-only links'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_admin'] = (
            user.is_authenticated and Admin.objects.filter(user=user).exists()
        )
        return context


class DashboardView(AdminContextMixin, TemplateView):
    '''Landing dashboard which shows stats to anyone'''
    template_name = 'project/dashboard.html'

    def get_context_data(self, **kwargs):
        '''Build all three dashboard Plotly charts (Students per Department,
        Dorm Occupancy, and Hatreds per Student) each with their own filter'''

        context = super().get_context_data(**kwargs)

        # chart #1: students by departments

        hometown = self.request.GET.get('hometown', '').strip()

        students_qs = Student.objects.all()
        if hometown:
            students_qs = students_qs.filter(hometown=hometown)

        departments = list(Department.objects.all().order_by('name'))
        dept_names = [d.name for d in departments]
        student_counts = [students_qs.filter(course_program=d).count() for d in departments]
        capacities = [d.capacity for d in departments]

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Students', x=dept_names, y=student_counts, marker_color='#2c5282'))
        fig.add_trace(go.Bar(name='Capacity', x=dept_names, y=capacities, marker_color='#a0aec0'))
        title = 'Students per Department'
        if hometown:
            title += f' — hometown: {hometown}'
        fig.update_layout(
            title=title,
            xaxis_title='Department',
            yaxis_title='Count',
            barmode='group',
            margin=dict(l=40, r=20, t=60, b=60),
            height=420,
        )
        context['students_per_department_graph'] = plot(
            fig, output_type='div', include_plotlyjs=False
        )

        hometowns = (
            Student.objects.exclude(hometown='')
            .values_list('hometown', flat=True)
            .distinct()
            .order_by('hometown')
        )
        context['hometown_choices'] = list(hometowns)
        context['selected_hometown'] = hometown

        # chart #2: dorm occupancy 

        dept = self.request.GET.get('dept', '').strip()

        dorms_qs = Dorm.objects.all().order_by('name')
        if dept == '__none__':
            dorms_qs = dorms_qs.filter(department__isnull=True)
        elif dept:
            dorms_qs = dorms_qs.filter(department_id=dept)

        dorms_list = list(dorms_qs)
        dorm_names = [d.name for d in dorms_list]
        occupied = [Student.objects.filter(lives_in=d).count() for d in dorms_list]
        available = [
            max(int(d.capacity) - occupied[i], 0) for i, d in enumerate(dorms_list)
        ]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name='Occupied', x=dorm_names, y=occupied, marker_color='#2c5282'))
        fig2.add_trace(go.Bar(name='Available', x=dorm_names, y=available, marker_color='#a0aec0'))
        title2 = 'Dorm Occupancy'
        if dept == '__none__':
            title2 += ' — Unrestricted dorms'
        elif dept:
            try:
                title2 += f' — {Department.objects.get(pk=dept).name}'
            except Department.DoesNotExist:
                pass
        fig2.update_layout(
            title=title2,
            xaxis_title='Dorm',
            yaxis_title='Beds',
            barmode='stack',
            margin=dict(l=40, r=20, t=60, b=60),
            height=420,
        )
        context['dorm_occupancy_graph'] = plot(
            fig2, output_type='div', include_plotlyjs=False
        )

        context['department_choices'] = list(Department.objects.all().order_by('name'))
        context['selected_dept'] = dept

        # chart #3: hatreds per student - top 3

        program = self.request.GET.get('program', '').strip()

        ranked_qs = Student.objects.all()
        if program:
            ranked_qs = ranked_qs.filter(course_program_id=program)

        ranked = list(
            ranked_qs.annotate(
                h1=Count('first_hatred', distinct=True),
                h2=Count('second_hatred', distinct=True),
            )
            .annotate(hatred_count=F('h1') + F('h2'))
            .filter(hatred_count__gt=0)
            .order_by('-hatred_count', 'last_name', 'first_name')[:3]
        )

        names = [f'{s.first_name} {s.last_name}' for s in ranked]
        counts = [s.hatred_count for s in ranked]

        # reverse so the highest count appears at the top of the horizontal bar
        
        names.reverse()
        counts.reverse()

        fig3 = go.Figure(go.Bar(
            x=counts,
            y=names,
            orientation='h',
            marker_color='#b91c1c',
        ))
        title3 = 'Hatreds per Student (Top 3)'
        if program:
            try:
                title3 += f' — {Department.objects.get(pk=program).name}'
            except Department.DoesNotExist:
                pass
        fig3.update_layout(
            title=title3,
            xaxis_title='Hatred count',
            yaxis_title='Student',
            margin=dict(l=140, r=20, t=60, b=60),
            height=max(420, len(names) * 28 + 120),
        )
        context['hatreds_per_student_graph'] = plot(
            fig3, output_type='div', include_plotlyjs=False
        )
        context['program_choices'] = context['department_choices']
        context['selected_program'] = program

        return context


class ShowAllStudentsView(ProjectLoginRequiredMixin, AdminContextMixin, ListView):
    '''Display every Student (login required)'''
    model = Student
    template_name = 'project/show_all_students.html'
    context_object_name = 'students'


class ShowAllProfessorsView(ProjectLoginRequiredMixin, AdminContextMixin, ListView):
    '''Display every Professor (login required)'''
    model = Professor
    template_name = 'project/show_all_professors.html'
    context_object_name = 'professors'


class ShowAllDormsView(ProjectLoginRequiredMixin, AdminContextMixin, ListView):
    '''Display every Dorm in the (login required)'''
    model = Dorm
    template_name = 'project/show_all_dorms.html'
    context_object_name = 'dorms'


class ShowAllDepartmentsView(ProjectLoginRequiredMixin, AdminContextMixin, ListView):
    '''Display every Department (login required)'''
    model = Department
    template_name = 'project/show_all_departments.html'
    context_object_name = 'departments'


class ShowAllHatredsView(ProjectLoginRequiredMixin, AdminContextMixin, ListView):
    '''Display every Hatred (login required)'''
    model = Hatred
    template_name = 'project/show_all_hatreds.html'
    context_object_name = 'hatreds'


# Admin create/update views


class CreateStudentView(AdminRequiredMixin, CreateView):
    '''Create a new Student'''
    model = Student
    form_class = CreateStudentForm
    template_name = 'project/create_student_form.html'
    success_url = reverse_lazy('show_all_students')


class UpdateStudentView(AdminRequiredMixin, UpdateView):
    '''Update an existing Student'''
    model = Student
    form_class = UpdateStudentForm
    template_name = 'project/update_student_form.html'
    success_url = reverse_lazy('show_all_students')


class CreateProfessorView(AdminRequiredMixin, CreateView):
    '''Create a new Professor'''
    model = Professor
    form_class = CreateProfessorForm
    template_name = 'project/create_professor_form.html'
    success_url = reverse_lazy('show_all_professors')


class UpdateProfessorView(AdminRequiredMixin, UpdateView):
    '''Update an existing Professor'''
    model = Professor
    form_class = UpdateProfessorForm
    template_name = 'project/update_professor_form.html'
    success_url = reverse_lazy('show_all_professors')


class CreateDormView(AdminRequiredMixin, CreateView):
    '''Create a new Dorm'''
    model = Dorm
    form_class = CreateDormForm
    template_name = 'project/create_dorm_form.html'
    success_url = reverse_lazy('show_all_dorms')


class UpdateDormView(AdminRequiredMixin, UpdateView):
    '''Update an existing Dorm'''
    model = Dorm
    form_class = UpdateDormForm
    template_name = 'project/update_dorm_form.html'
    success_url = reverse_lazy('show_all_dorms')


class CreateDepartmentView(AdminRequiredMixin, CreateView):
    '''Create a new Department'''
    model = Department
    form_class = CreateDepartmentForm
    template_name = 'project/create_department_form.html'
    success_url = reverse_lazy('show_all_departments')


class UpdateDepartmentView(AdminRequiredMixin, UpdateView):
    '''Update an existing Department'''
    model = Department
    form_class = UpdateDepartmentForm
    template_name = 'project/update_department_form.html'
    success_url = reverse_lazy('show_all_departments')


