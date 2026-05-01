# File: models.py
# Name: Nicholas Sima (nicksima@bu.edu)
# Description: models file to hold university registrar model types


from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Admin(models.Model):
    '''Admin model type to alter other model instances'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        '''Promote the User'''

        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Admin: {self.user.username}'


class Professor(models.Model):
    '''Teacher model type'''

    title = models.TextField()
    surname = models.TextField()
    image_file = models.ImageField(upload_to='project/')

    def __str__(self):

        return f'{self.title} {self.surname}'


class Department(models.Model):
    '''Department model type'''
    name = models.TextField()
    staff = models.ForeignKey(Professor, blank=True, on_delete=models.CASCADE)
    students = models.FloatField(default=0)
    capacity = models.FloatField()

    def __str__(self):

        return f'Department: {self.name} -- Staff: {self.staff}'


class Dorm(models.Model):
    '''Dorm model type'''
    name = models.TextField()
    address = models.TextField()
    image_url = models.TextField()
    capacity = models.FloatField()
    current_size = models.FloatField(default=0)
    resident_assistant = models.ForeignKey(Professor, blank=True, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        str = f'Dorm: {self.name} -- {self.address}'

        if self.resident_assistant:
            str += f' -- {self.resident_assistant}'

        if self.department:
            str += f' -- {self.department}'

        return str


class Student(models.Model):
    '''Student model type'''

    first_name = models.TextField()
    last_name = models.TextField()
    course_program = models.ForeignKey(Department, blank=True, null=True, on_delete=models.CASCADE)
    hometown = models.TextField()
    lives_in = models.ForeignKey(Dorm, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        str = f'{self.first_name} {self.last_name}'

        if self.course_program:
            str += f' -- {self.course_program}'

        if self.lives_in:
            str += f' -- {self.lives_in}'

        return str

class Hatred(models.Model):
    '''Hatred model type to show student relationship'''
    first_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='first_hatred')
    second_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='second_hatred')

    def __str__(self):
        first_name = f'{self.first_student.first_name} {self.first_student.last_name}'
        second_name = f'{self.second_student.first_name} {self.second_student.last_name}'
        return f'{first_name} and {second_name} hate each other!'
