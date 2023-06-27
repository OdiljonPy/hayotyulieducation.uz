import functools

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect, render

from authentication.decorators.v1 import if_role_not_empty, if_person_info_not_empty, if_teacher, if_student
from authentication.models import StudentTopic, Topic, Teacher
from authentication.utils.v1 import is_student_or_teacher_str, is_student_or_teacher_obj
from tasksManager.forms import TopicForm, MessageForm, ConnectionForm, UpdateTopicForm


@login_required(login_url='sign_in')
@if_role_not_empty
@if_person_info_not_empty
def index(request):
    if is_student_or_teacher_str(request.user) == "Студент":
        obj = is_student_or_teacher_obj(request.user)
        teachers = obj.teachers.all()
        return render(request,
                      'dashboard/index-student.html',
                      {
                          'role': request.role_of_user,
                          'teachers': teachers
                      }
                      )
    if is_student_or_teacher_str(request.user) == "Учитель":
        obj = is_student_or_teacher_obj(request.user)
        topics = obj.topics.all()
        return render(request,
                      'dashboard/index-teacher.html',
                      {
                          'role': request.role_of_user,
                          'topics': topics
                      }
                      )


@login_required(login_url='sign_in')
@if_role_not_empty
@if_teacher
def add_topic(request):
    obj = request.user.teacher

    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.teacher = obj
            topic.save()

            return redirect('/tasks-manager/home')
    else:
        form = TopicForm()

    return render(request, 'dashboard/add-topic.html',
                  {
                      "form": form,
                      'role': request.role_of_user
                  })


@login_required(login_url='sign_in')
@if_role_not_empty
@if_teacher
def update_topic(request, topic_id):
    obj = request.user.teacher

    if request.method == 'POST':
        form = UpdateTopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = request.user.teacher.topics.get(id=topic_id)
            title = form.cleaned_data.get('title')
            if title:
                topic.title=title
            description = form.cleaned_data.get('description')
            if description:
                topic.description = description
            upload = form.cleaned_data.get('upload')
            if upload:
                topic.upload = upload
            topic.save()
            # return redirect('/tasks-manager/home')
    else:
        form = UpdateTopicForm()

    return render(request, 'dashboard/update-topic.html',
                  {
                      "form": form,
                      'role': request.role_of_user
                  })


@login_required(login_url='sign_in')
@if_role_not_empty
@if_teacher
def show_students_in_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            student=topic.students.get(id=form.cleaned_data['student_id'])
            connection = StudentTopic.objects.filter(topic=topic, student=student).first()
            return redirect('/tasks-manager/topic-connections/%s' % (connection.id,))
    form = ConnectionForm()

    students = topic.students.all()
    return render(request, 'dashboard/show-students-in-topic.html', {"students": students, "form": form,'role': request.role_of_user})


@login_required(login_url='sign_in')
@if_role_not_empty
@if_student
def show_teacher_topic(request, teacher_id):
    obj = request.user.student.teachers.get(id=teacher_id)
    return render(request, 'dashboard/show-topics.html', {"topics": obj.topics.all(),'role': request.role_of_user})


@login_required(login_url='sign_in')
@if_role_not_empty
@if_student
def create_connection_with_topic(request, teacher_id, topic_id):
    topic = Topic.objects.get(id=topic_id)
    connection = StudentTopic(topic=topic, student=request.user.student)

    try:
        connection.save()
    except:
        pass
    connection = StudentTopic.objects.filter(topic=topic, student=request.user.student).first()
    return redirect('/tasks-manager/topic-connections/%s' % (connection.id,))


@login_required(login_url='sign_in')
@if_role_not_empty
def dialog_with_topic(request, connection_id):
    connection = StudentTopic.objects.get(id=connection_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.title = "%s: %s" % (request.user.username, message.title)
            message.studenttopic = connection
            message.save()

    form = MessageForm()

    messages = connection.messages.all()
    return render(request, 'dashboard/dialog-with-topic.html', {
        "messages": messages,
        "form": form,
        'role': request.role_of_user

    })
