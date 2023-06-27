from django.core.exceptions import ObjectDoesNotExist


def is_student_or_teacher_str(user):
    try:
        user.student
        return "Студент"
    except ObjectDoesNotExist:
        pass
    try:
        user.teacher
        return "Учитель"
    except ObjectDoesNotExist:
        pass


def is_student_or_teacher_obj(user):
    try:

        user.student
        return user.student
    except ObjectDoesNotExist:
        pass
    try:
        user.teacher
        return user.teacher
    except ObjectDoesNotExist:
        pass
