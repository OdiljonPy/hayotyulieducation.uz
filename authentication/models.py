import datetime
import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.db import models
from ckeditor.fields import RichTextField
from app import settings

languages_list = []
with open('/root/hayotyulieducation.uz/data/languages.txt', 'r') as file:
    languages_list = [(lan.strip(), lan.strip()) for lan in file.read().split('\n')]


class PersonInfo(models.Model):
    first_name = models.CharField(max_length=120, verbose_name="Фамилия", null=False)
    second_name = models.CharField(max_length=120, verbose_name="Имя", null=False)
    father_name = models.CharField(max_length=120, verbose_name="Отчество", null=False)

    number_of_contract = models.CharField(max_length=120, verbose_name="Номер Договора", null=True)
    passport_serial_with_number = models.CharField(max_length=120, verbose_name="Серия и номер паспорта", null=True)
    study_major = models.CharField(max_length=120, verbose_name="Направление обучения", null=True)
    region = models.CharField(max_length=120, verbose_name="Регион", null=True)
    school = models.CharField(max_length=120, verbose_name="Школа", null=True)

    contract = models.FileField(upload_to='contracts/', blank=True, null=True, verbose_name="Загрузить договор")
    birthday = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    university = models.CharField(max_length=120, blank=True, null=True, verbose_name="Университет")
    country = models.CharField(max_length=120, blank=True, null=True, verbose_name="Страна")

    LANG_CHOICES = languages_list
    nationality = models.CharField(
        verbose_name="Национальность",
        max_length=100,
        choices=LANG_CHOICES,
        null=True
    )

    def __str__(self):
        return "%s %s %s" % (self.first_name, self.second_name, self.father_name)

    class Meta(object):
        verbose_name = 'Персональные данные'
        verbose_name_plural = 'Персональные данные'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    person_info = models.OneToOneField(PersonInfo, on_delete=models.CharField, null=True)
    course_name = models.CharField("Предмет", null=True, max_length=120)

    def __str__(self):
        try:
            return "%s %s %s" % (
                self.person_info.first_name, self.person_info.second_name, self.person_info.father_name)
        except Exception as e:
            return "error"

    class Meta(object):
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Topic(models.Model):
    title = models.CharField("Название", max_length=120)
    description = models.TextField("Описание", blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="topics")

    def user_directory_path(instance, filename):
        return 'uploaded/topic/{0}/{1}'.format(
            int(datetime.datetime.now().timestamp()),
            filename)

    upload = models.FileField(upload_to=user_directory_path, null=True)

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = 'Топик'
        verbose_name_plural = 'Топики'


class Student(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', blank=True, null=True,
                               verbose_name="Менеджер")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # billing = models.One(Billing, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher, through='StudentTeacher')
    topics = models.ManyToManyField(Topic, through='StudentTopic', related_name='students')
    person_info = models.OneToOneField(PersonInfo, on_delete=models.CharField, null=True)

    status = models.IntegerField(choices=(
        (1, "Активный"),
        (0, "Архив"),
    ), default=1)

    full_verified = models.BooleanField(default=False, verbose_name="Полностью проверен")

    main_documents = models.FileField(upload_to='main_documents', blank=True, null=True,
                                      verbose_name="Общие документы студента")
    passport_red = models.FileField(upload_to='passport_red', blank=True, null=True, verbose_name="Красный паспорт "
                                                                                                  "студента")
    passport_red_translate = models.FileField(upload_to='passport_red', blank=True, null=True,
                                              verbose_name="Красный паспорт студента  (Таржима натариус)")
    tabel = models.FileField(upload_to='tabel', blank=True, null=True, verbose_name="Табель")
    school_certificate = models.FileField(upload_to='school_certificate', blank=True, null=True,
                                          verbose_name="Аттестат")
    school_certificate_translate = models.FileField(upload_to='school_certificate', blank=True, null=True,
                                                    verbose_name="Аттестат (Таржима натариус)")
    medical_certificate = models.FileField(upload_to='medical_certificate', blank=True, null=True,
                                           verbose_name="Медицинская справка")

    dalolatnoma = models.FileField(upload_to="dalolatnoma", blank=True, null=True, verbose_name="Далолатнома")
    dalolatnoma_translate = models.FileField(upload_to="dalolatnoma", blank=True, null=True,
                                             verbose_name="Далолатнома (Таржима натариус)")

    passport_me = models.BooleanField(default=False, verbose_name="Паспорт студента")
    passport_me_translate = models.BooleanField(default=False, verbose_name="Паспорт студента (Таржима натариус)")
    passport_father = models.BooleanField(default=False, verbose_name="Паспорт отца")
    passport_father_translate = models.BooleanField(default=False, verbose_name="Паспорт отца  (Таржима натариус)")
    passport_mother = models.BooleanField(default=False, verbose_name="Паспорт матери")
    passport_mother_translate = models.BooleanField(default=False, verbose_name="Паспорт матери (Таржима натариус)")
    metric_me = models.BooleanField(default=False, verbose_name="Метрика студента")
    metric_me_translate = models.BooleanField(default=False, verbose_name="Метрика студента (Таржима натариус)")
    metric_father = models.BooleanField(default=False, verbose_name="Метрика отца")
    metric_father_translate = models.BooleanField(default=False, verbose_name="Метрика отца (Таржима натариус)")
    metric_mother = models.BooleanField(default=False, verbose_name="Метрика матери")
    metric_mother_translate = models.BooleanField(default=False, verbose_name="Метрика матери (Таржима натариус)")
    marriage_certificate = models.BooleanField(default=False, verbose_name="Свидетельство о браке")
    marriage_certificate_translate = models.BooleanField(default=False, verbose_name="Свидетельство о браке (Таржима "
                                                                                     "натариус)")
    picture = models.BooleanField(default=False, verbose_name="Фотография студента ")

    spid = models.BooleanField(default=False, verbose_name="СПИД")
    forma_086 = models.BooleanField(default=False, verbose_name="Форма 086")
    forma_064 = models.BooleanField(default=False, verbose_name="Форма 064")
    narkologiya = models.BooleanField(default=False, verbose_name="Наркология")
    psix_bolnitsa = models.BooleanField(default=False, verbose_name="Психиатрическая больница")
    tuberklyoz = models.BooleanField(default=False, verbose_name="Туберкулез")
    sifliz = models.BooleanField(default=False, verbose_name="Сифилис")

    description = RichTextField(blank=True, null=True)

    def __str__(self):
        try:
            return "%s %s %s" % (
                self.person_info.first_name, self.person_info.second_name, self.person_info.father_name)
        except Exception as e:
            return "error"

    class Meta(object):
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class StudentTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='student'
    )

    class Meta(object):
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'student'], name='teacher_student_idx'),
        ]


class StudentTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='student'
    )

    class Meta(object):
        constraints = [
            models.UniqueConstraint(fields=['topic', 'student'], name='topic_student_idx'),
        ]
        verbose_name = 'Студент-Топик Канал'
        verbose_name_plural = 'Студент-Топик Канал'

    def __str__(self):
        return "%s %s %s" % (
            self.topic.title, self.student.person_info.first_name, self.student.person_info.second_name)


class Message(models.Model):

    def user_directory_path(instance, filename):
        return 'uploaded/user_{0}/{1}/{2}'.format(
            instance.studenttopic.student.user.id,
            int(datetime.datetime.now().timestamp()),
            filename)

    title = models.CharField("Сообщение", max_length=1000)
    upload = models.FileField(upload_to=user_directory_path, null=True)
    studenttopic = models.ForeignKey(StudentTopic, on_delete=models.CASCADE, related_name="messages")


class Billing(models.Model):
    def upload_receipt_folder(self, filename):
        return 'uploaded/receipt/{0}'.format(
            filename)

    def delete_receipt(self):
        if self.receipt:
            file_path = os.path.join(settings.MEDIA_ROOT, self.receipt.name)

            if os.path.exists(file_path):
                os.remove(file_path)

            self.receipt = None
            self.save()

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Комментарий", max_length=100, blank=True, null=True)
    receipt = models.FileField("Чек", upload_to=upload_receipt_folder, null=True)
    create_at = models.DateField("Время создания", default=datetime.datetime.now().date())
    verified = models.BooleanField(default=False, verbose_name="Проверена")

    def __str__(self):
        try:
            return "%s %s" % (
                self.create_at, self.student)
        except Exception as e:
            return "error"

    class Meta(object):
        verbose_name = 'Чеки оплаты'
        verbose_name_plural = 'Чеки оплаты'
