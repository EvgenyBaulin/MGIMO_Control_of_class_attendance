from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Group, Auditorium, Lecture, NFCRecord
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'group', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'date', 'start_time', 'end_time', 'auditorium', 'groups']


class NFCRecordSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    auditorium = AuditoriumSerializer(read_only=True)

    class Meta:
        model = NFCRecord
        fields = ['id', 'student', 'auditorium', 'timestamp', 'nfc_code']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token
