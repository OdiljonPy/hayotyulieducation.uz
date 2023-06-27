import datetime

from django.contrib import admin
from django.db.models import Count, Q

# Register your models here.
from .models import Student, Teacher, PersonInfo, StudentTeacher, Topic, StudentTopic, Message, Billing


class StudentTeacherInline(admin.TabularInline):
    model = StudentTeacher


class StudentTopicInline(admin.TabularInline):
    model = StudentTopic


class TopicInline(admin.TabularInline):
    model = Topic


class MessageInline(admin.TabularInline):
    model = Message


class IsThereReceiptFilter(admin.SimpleListFilter):
    title = 'Чек'
    parameter_name = 'custom_filter'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Есть чек'),
            ('no', 'Нет чека'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(~Q(billing__receipt__exact=''))
        if self.value() == 'no':
            return queryset.filter(billing__receipt__exact='')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # inlines = (StudentTeacherInline, StudentTopicInline)
    list_display = ('person_info', 'user', 'get_create_at', "get_courses_name")
    list_filter = (IsThereReceiptFilter, "billing__create_at", "teachers__course_name")
    search_fields = ('person_info__first_name__icontains',)

    def get_create_at(self, obj):
        from django.utils.html import format_html
        try:
            color = 'black'

            if (datetime.datetime.now().date() - obj.billing.create_at).days >= 3:
                color = '#e69b00'
            if (datetime.datetime.now().date() - obj.billing.create_at).days >= 7:
                color = 'red'
            if obj.billing.receipt:
                color = 'green'

            return format_html("<div style='color:{}'>{}</div>", color, obj.billing.create_at)
        except Exception:
            return "N/A"

    def get_courses_name(self, obj):
        from django.utils.html import format_html
        try:
            buffer = []
            for teacher in obj.teachers.all():
                buffer.append(teacher.course_name)
            to_paste = '<br>'.join(buffer)
            return format_html(to_paste)
        except Exception:
            return "N/A"

    get_create_at.short_description = 'Дата создания'
    get_courses_name.short_description = 'Предметы'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = (StudentTeacherInline, TopicInline)
    search_fields = ('person_info__first_name__icontains', "course_name",)
    list_display = ('person_info', 'user', 'get_student_count', "course_name")
    list_filter = ("course_name",)

    def get_student_count(self, obj):
        return f"{obj.student_count}/15"

    get_student_count.short_description = 'Количество студентов'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(student_count=Count('student__id'))
        return queryset.order_by('student_count')


@admin.register(PersonInfo)
class PersonInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('id', 'receipt', 'create_at', "student")
    list_filter = ('create_at', "student")
    search_fields = ('student__person_info__first_name__icontains',)
    actions = ['delete_selected']

    def delete_selected(modeladmin, request, queryset):
        for billing in queryset:
            billing.delete_receipt()

    delete_selected.short_description = "Delete selected billing receipts"


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentTopic)
class StudentTopicAdmin(admin.ModelAdmin):
    inlines = (MessageInline,)
