from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('topics/<int:topic_id>', views.update_topic, name='topic_add'),
    path('topics/add', views.add_topic, name='topic_add'),

    path('teachers/<int:teacher_id>/topics', views.show_teacher_topic, name='show_teacher_topic'),
    path('topics/<int:topic_id>/students/', views.show_students_in_topic, name='show_students_in_topic'),
    path('teachers/<int:teacher_id>/topics/<int:topic_id>/connect', views.create_connection_with_topic, name='create_connection_with_topic'),
    path('topic-connections/<int:connection_id>', views.dialog_with_topic, name='dialog_with_topic'),

]