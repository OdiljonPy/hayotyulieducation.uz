from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .decorators.v1 import if_role_empty, if_student
from .forms import RegisterForm, LoginForm, PersonalInfoForm, FullPersonalInfoForm
from .models import Teacher, Student, Billing
from .utils.v1 import is_student_or_teacher_obj


@login_required
def log_out(request):
    logout(request)
    return redirect('/tasks-manager/home')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/tasks-manager/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            return redirect('/tasks-manager/home')
    else:
        form = LoginForm()

    return render(request, 'registration/sign_in.html', {"form": form})


@login_required
@if_role_empty
def choose_role(request):
    return render(request, 'registration/choose-role.html')


@login_required
@if_role_empty
def register_teacher(request):
    teacher = Teacher(user=request.user)
    teacher.save()
    return redirect('/tasks-manager/home')


@login_required
@if_role_empty
def register_student(request):
    student = Student(user=request.user)
    billing = Billing()
    billing.save()
    student.billing = billing
    student.save()
    return redirect('/tasks-manager/home')


@login_required
@if_student
def personal_info_for_student(request):
    if request.method == 'POST':
        form = FullPersonalInfoForm(request.POST)

        if form.is_valid():
            per_inf = form.save()
            obj = is_student_or_teacher_obj(request.user)
            obj.person_info = per_inf
            obj.save()

            return redirect('/')
    else:
        form = FullPersonalInfoForm()

    return render(request, 'registration/person-info.html', {"form": form, 'role': "Ожидает регистрации"})


@login_required
def personal_info(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)

        if form.is_valid():
            per_inf = form.save()
            obj = is_student_or_teacher_obj(request.user)
            obj.person_info = per_inf
            obj.save()

            return redirect('/')
    else:
        form = PersonalInfoForm()

    return render(request, 'registration/person-info.html', {"form": form, 'role': "Ожидает регистрации"})
