from django.urls import path
from .views import UserCreateView, TaskCreateView, TaskAssignView, UserTasksView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='create-user'),  # Add this line
    path('tasks/', TaskCreateView.as_view(), name='create-task'),
    path('tasks/assign/', TaskAssignView.as_view(), name='assign-task'),
    path('tasks/user/<int:user_id>/', UserTasksView.as_view(), name='user-tasks'),
]
