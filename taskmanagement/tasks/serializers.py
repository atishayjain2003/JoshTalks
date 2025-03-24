from rest_framework import serializers
from .models import Task, User  # Import the correct User model

# Serializer for creating a task (only name & description required)
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description']

# Serializer for retrieving a task (includes all fields)
class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_at', 'status', 'completed_at', 'assigned_users']

    def get_assigned_users(self, obj):
        return UserSerializer(obj.assigned_users.all(), many=True).data

# Serializer for assigning users to a task
class TaskAssignSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    user_ids = serializers.ListField(child=serializers.IntegerField())

    def validate(self, data):
        task_id = data.get('task_id')
        user_ids = data.get('user_ids')

        # Ensure the task exists
        if not Task.objects.filter(id=task_id).exists():
            raise serializers.ValidationError({"task_id": "Task not found."})

        # Ensure all users exist
        existing_users = User.objects.filter(id__in=user_ids)
        if existing_users.count() != len(user_ids):
            raise serializers.ValidationError({"user_ids": "Some users do not exist."})

        return data

# Serializer for user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile']  # Fixed: removed 'username'
