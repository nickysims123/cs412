# File: forms.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: ModelForms for admin Create/Update views in the project app



from django import forms
from django.db.models import Q
from .models import *


def _validate_dorm_department(cleaned):
    '''Ensure a student entering a department affiliated dorm is in that department
    preceded with _ as to not unnecessarily import :D'''

    target_dorm = cleaned.get('lives_in')
    program = cleaned.get('course_program')
    if not target_dorm or not target_dorm.department_id:
        return
    if not program or program.pk != target_dorm.department_id:
        first = (cleaned.get('first_name') or '').strip() or 'this student'
        last = (cleaned.get('last_name') or '').strip()
        student_label = (first + ' ' + last).strip()
        program_name = program.name if program else 'no department'
        raise forms.ValidationError(
            f'Cannot move {student_label} into {target_dorm.name}: this dorm '
            f'is reserved for {target_dorm.department.name} students, but '
            f'{student_label} is in {program_name}.'
        )


class CreateStudentForm(forms.ModelForm):
    '''Create student form'''

    hated_students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Hates',
    )

    class Meta:
        '''Associate this form with the Student model'''
        model = Student
        fields = ['first_name', 'last_name', 'hometown', 'course_program', 'lives_in']

    def clean(self):
        '''Reject a dorm assignment that violates the dorm's department restriction'''

        cleaned = super().clean()
        _validate_dorm_department(cleaned)
        return cleaned

    def save(self, commit=True):
        '''Save the Student, then create Hatred rows for each selected enemy'''

        student = super().save(commit=commit)
        for other in self.cleaned_data.get('hated_students') or []:
            already = Hatred.objects.filter(
                Q(first_student=student, second_student=other) |
                Q(first_student=other, second_student=student)
            ).exists()
            if not already:
                Hatred.objects.create(first_student=student, second_student=other)
        return student

class UpdateStudentForm(forms.ModelForm):
    '''Form to update an existing Student'''

    hated_students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Hates',
    )

    class Meta:
        '''Associate this form with the Student model'''
        model = Student
        fields = ['first_name', 'last_name', 'hometown', 'course_program', 'lives_in']

    def __init__(self, *args, **kwargs):
        '''Populate the hated_students choices and preselect existing hatreds.'''

        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['hated_students'].queryset = Student.objects.exclude(pk=self.instance.pk)
            self.fields['hated_students'].initial = self._current_enemies()

    def _current_enemies(self):
        '''Return all Students who currently share a Hatred with this Student.'''

        student = self.instance
        hatreds = Hatred.objects.filter(
            Q(first_student=student) | Q(second_student=student)
        ).select_related('first_student', 'second_student')
        enemies = []
        for h in hatreds:
            enemies.append(h.second_student if h.first_student_id == student.pk else h.first_student)
        return enemies

    def clean(self):
        '''Reject a dorm assignment if a hated student already lives there,
        or if the dorm is restricted to a department this student is not in.'''

        cleaned = super().clean()
        _validate_dorm_department(cleaned)

        target_dorm = cleaned.get('lives_in')
        student = self.instance

        if not target_dorm or not student.pk:
            return cleaned

        # if we have checked hated_students already
        if 'hated_students' in cleaned:
            enemies = list(cleaned['hated_students'])
        else:
            enemies = self._current_enemies()

        for enemy in enemies:
            if enemy.lives_in_id == target_dorm.id:
                raise forms.ValidationError(
                    f'Cannot move {student.first_name} {student.last_name} into '
                    f'{target_dorm.name}: {student.first_name} {student.last_name} '
                    f'hates {enemy.first_name} {enemy.last_name}, who already lives '
                    f'in {target_dorm.name}.'
                )
        return cleaned

    def save(self, commit=True):
        '''Save the Student, then sync Hatred rows'''

        student = super().save(commit=commit)
        new_set = set(self.cleaned_data.get('hated_students') or [])
        current_set = set(self._current_enemies())

        for removed in current_set - new_set:
            Hatred.objects.filter(
                Q(first_student=student, second_student=removed) |
                Q(first_student=removed, second_student=student)
            ).delete()

        for added in new_set - current_set:
            Hatred.objects.create(first_student=student, second_student=added)

        return student

class CreateProfessorForm(forms.ModelForm):
    '''Form to create a new Professor'''

    class Meta:
        '''Associate this form with the Professor model'''
        model = Professor
        fields = ['title', 'surname', 'image_file']

class UpdateProfessorForm(forms.ModelForm):
    '''Form to update an existing Professor'''

    class Meta:
        '''Associate this form with the Professor model'''
        model = Professor
        fields = ['title', 'surname', 'image_file']

class CreateDormForm(forms.ModelForm):
    '''Form to create a new Dorm'''

    class Meta:
        '''Associate this form with the Dorm model'''
        model = Dorm
        fields = ['name', 'address', 'image_url', 'capacity', 'current_size',
                  'resident_assistant', 'department']

class UpdateDormForm(forms.ModelForm):
    '''Form to update an existing Dorm'''

    class Meta:
        '''Associate this form with the Dorm model'''
        model = Dorm
        fields = ['name', 'address', 'image_url', 'capacity', 'current_size',
                  'resident_assistant', 'department']

class CreateDepartmentForm(forms.ModelForm):
    '''Form to create a new Department'''

    class Meta:
        '''Associate this form with the Department model'''
        model = Department
        fields = ['name', 'staff', 'students', 'capacity']

class UpdateDepartmentForm(forms.ModelForm):
    '''Form to update an existing Department'''

    class Meta:
        '''Associate this form with the Department model'''
        model = Department
        fields = ['name', 'staff', 'students', 'capacity']
