import requests
from openpyxl import Workbook
from django.conf import settings

COLUMN_TITLE = (
    "PERSON INFO", "USER", "МЕНЕДЖЕР", "Дата рождения", "Номер Договора", "Направление обучения", "Университет",
    "ДАТА СОЗДАНИЯ", "ПРЕДМЕТЫ", "ПОЛНОСТЬЮ ПРОВЕРЕН", "ОПЛАЧЕННАЯ СУММА", "КРАСНЫЙ ПАСПОРТ СТУДЕНТА",
    "АТТЕСТАТ", "ПАСПОРТ СТУДЕНТА", "ПАСПОРТ ОТЦА", "ПАСПОРТ МАТЕРИ", "МЕТРИКА СТУДЕНТА", "МЕТРИКА ОТЦА",
    "МЕТРИКА МАТЕРИ", "СВИДЕТЕЛЬСТВО О БРАКЕ", "ФОТОГРАФИЯ СТУДЕНТА", "СПИД", "ФОРМА 086", "ФОРМА 064",
    "НАРКОЛОГИЯ", "ПСИХИАТРИЧЕСКАЯ БОЛЬНИЦА", "ТУБЕРКУЛЕЗ", "СИФИЛИС")


def create_exel_file(user_id):
    wb = Workbook()
    ws = wb.active
    from ..models import Student, Billing
    students = Student.objects.all()
    ws.append(COLUMN_TITLE)
    for student in students:
        billing = Billing.objects.filter(student_id=student.id).first()
        amount_paid = billing.sum
        passport_red = bool(student.passport_red)
        school_certificate = bool(student.school_certificate)
        course_names = ""
        res = [course_names + f"{name.course_name} " for name in student.teachers.all()]
        ws.append(
            (f"{student.person_info.first_name} {student.person_info.second_name} {student.person_info.father_name}",
             f"{student.user.first_name} {student.user.last_name}",
             f"{student.author.first_name} {student.author.last_name}",
             f"{student.person_info.birthday}",
             f"{student.person_info.number_of_contract}",
             f"{student.person_info.study_major}",
             f"{student.person_info.university}",
             f"{student.create_at}",
             f"{course_names}",
             f"{student.full_verified}",
             f"{amount_paid}",
             f"{passport_red}",
             f"{school_certificate}",
             f"{student.passport_me}",
             f"{student.passport_father}",
             f"{student.passport_mother}",
             f"{student.metric_me}",
             f"{student.metric_father}",
             f"{student.metric_mother}",
             f"{student.marriage_certificate}",
             f"{student.picture}",
             f"{student.spid}",
             f"{student.forma_086}",
             f"{student.forma_064}",
             f"{student.narkologiya}",
             f"{student.psix_bolnitsa}",
             f"{student.tuberklyoz}",
             f"{student.sifliz}"
             )
        )

    wb.save("/root/hayotyulieducation.uz/authentication/utils/students_exel.xlsx")
    document = open(f"/root/hayotyulieducation.uz/authentication/utils/students_exel.xlsx", "rb")
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendDocument"
    requests.post(url, data={'chat_id': user_id},
                  files={'document': document})
