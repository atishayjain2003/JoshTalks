from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task, User
from .serializers import (
    TaskCreateSerializer, TaskSerializer, TaskAssignSerializer, UserSerializer
)

# API to create a user
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to create a task (Only requires name & description)
class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to assign a task to users
class TaskAssignView(APIView):
    def post(self, request):
        serializer = TaskAssignSerializer(data=request.data)
        if serializer.is_valid():
            task = Task.objects.get(id=serializer.validated_data['task_id'])
            users = User.objects.filter(id__in=serializer.validated_data['user_ids'])
            task.assigned_users.set(users)
            return Response({"message": "Task assigned successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to get tasks assigned to a specific user
class UserTasksView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            tasks = user.tasks.all()  # Fetch tasks assigned to this user
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
