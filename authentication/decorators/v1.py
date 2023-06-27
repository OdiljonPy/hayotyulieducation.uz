import functools

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


def if_role_not_empty(view_func, verification_url="choose_role"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user: User = request.user
        is_student = False
        is_teacher = False
        try:
            user.student
            is_student = True
            request.role_of_user = "Студент"
        except ObjectDoesNotExist:
            pass
        try:
            user.teacher
            is_teacher = True
            request.role_of_user = "Учитель"
        except ObjectDoesNotExist:
            pass

        if is_student or is_teacher:
            return view_func(request, *args, **kwargs)

        return redirect(verification_url)
    return wrapper

def if_role_not_empty(view_func, verification_url="choose_role"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user: User = request.user
        is_student = False
        is_teacher = False
        try:
            user.student
            is_student = True
            request.role_of_user = "Студент"
        except ObjectDoesNotExist:
            pass
        try:
            user.teacher
            is_teacher = True
            request.role_of_user = "Учитель"
        except ObjectDoesNotExist:
            pass

        if is_student or is_teacher:
            return view_func(request, *args, **kwargs)

        return redirect(verification_url)
    return wrapper


def if_role_empty(view_func, verification_url="home"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user: User = request.user
        is_student = False
        is_teacher = False
        try:
            user.student
            is_student = True
        except ObjectDoesNotExist:
            pass
        try:
            user.teacher
            is_teacher = True
        except ObjectDoesNotExist:
            pass

        if is_student or is_teacher:
            return redirect(verification_url)
        return view_func(request, *args, **kwargs)

    return wrapper


def if_person_info_not_empty(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user: User = request.user
        is_student = False
        is_teacher = False
        try:
            user.student
            if user.student.person_info != None:
                is_student = True
            else:
                return redirect("personal_student_info")
        except ObjectDoesNotExist:
            pass
        try:
            user.teacher
            if user.teacher.person_info != None:
                is_teacher = True
            else:
                return redirect("personal_teacher_info")
        except ObjectDoesNotExist:
            pass

        if is_student or is_teacher:
            return view_func(request, *args, **kwargs)



    return wrapper


def if_teacher(view_func, verification_url="home"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user: User = request.user
        try:
            user.teacher
            return view_func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            pass

        return redirect(verification_url)

    return wrapper


def if_student(view_func, verification_url="home"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user: User = request.user
        try:
            user.student
            return view_func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            pass

        return redirect(verification_url)

    return wrapper
