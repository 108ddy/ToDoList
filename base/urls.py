from django.urls import path
from .views import TaskList, TaskDetail


app_name = 'base'
urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
]
