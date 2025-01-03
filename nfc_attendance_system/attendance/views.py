from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .permissions import IsInstructor

from .models import Group, Auditorium, Lecture, Attendance
from .serializers import (
    GroupSerializer,
    UserSerializer,
    AuditoriumSerializer,
    LectureSerializer,
    AttendanceSerializer
)

User = get_user_model()


# 1. Student Registration
class StudentRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'student'
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student registered successfully!'},
                            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# 2. Instructor Registration
class InstructorRegisterView(APIView):
    SECRET_KEY = 'qweiopasdjklzxcbnm'

    def post(self, request):
        secret_key = request.data.get('secret_key')
        if secret_key != self.SECRET_KEY:
            return Response({'error': 'Invalid secret key'}, status = status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['role'] = 'instructor'
        data.pop('secret_key', None)
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Instructor registered successfully!'},
                            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# 3. Group Management (ViewSet)
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsInstructor]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


# 4. Auditorium Management (ViewSet)
class AuditoriumViewSet(viewsets.ModelViewSet):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        auditorium = serializer.save()
        # Example generating a random code
        import uuid
        nfc_code = uuid.uuid4().hex
        auditorium.nfc_code = nfc_code
        auditorium.nfc_link = f"http://example.com/attendance?code={nfc_code}"
        auditorium.save()

        return Response(self.serializer_class(auditorium).data, status = status.HTTP_201_CREATED)

    def update_nfc(self, request, pk = None):
        auditorium = get_object_or_404(Auditorium, pk = pk)
        new_code = request.data.get('nfc_code')
        if not new_code:
            return Response({'error': 'No NFC code provided.'},
                            status = status.HTTP_400_BAD_REQUEST)
        auditorium.nfc_code = new_code
        auditorium.nfc_link = f"http://example.com/attendance?code={new_code}"
        auditorium.save()
        return Response(self.serializer_class(auditorium).data, status = status.HTTP_200_OK)


# 5. Lecture Management (ViewSet)
class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def list(self, request, *args, **kwargs):
        date_filter = request.query_params.get('date')
        if date_filter:
            self.queryset = self.queryset.filter(date = date_filter)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Instructors only
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Instructors only
        return super().destroy(request, *args, **kwargs)


# 6. Attendance Tracking
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view


@api_view(['POST'])
def record_attendance(request):
    """
    POST /api/attendance/
    Input: code from NFC link, JWT token
    """
    code = request.data.get('code')
    if not code:
        return Response({'error': 'NFC code is required'}, status = status.HTTP_400_BAD_REQUEST)

    # Find the auditorium with this code
    try:
        auditorium = Auditorium.objects.get(nfc_code = code)
    except Auditorium.DoesNotExist:
        return Response({'error': 'Invalid NFC code'}, status = status.HTTP_404_NOT_FOUND)

    # Identify which lecture is in session or about to start
    now = timezone.now()
    # We'll assume "in session" means date == today and time range includes now.
    # Real logic might be more complex.
    try:
        lecture = Lecture.objects.get(
            auditorium = auditorium,
            date = now.date(),
            start_time__lte = now.time(),
            end_time__gte = now.time()
        )
    except Lecture.DoesNotExist:
        return Response({'error': 'No ongoing lecture for this auditorium'},
                        status = status.HTTP_404_NOT_FOUND)

    # Mark attendance
    user = request.user
    if user.role != 'student':
        return Response({'error': 'Only students can record attendance'},
                        status = status.HTTP_403_FORBIDDEN)

    attendance, created = Attendance.objects.get_or_create(student = user, lecture = lecture)
    if created:
        return Response({'message': 'Attendance recorded'}, status = status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Attendance already recorded'}, status = status.HTTP_200_OK)


# 7. Attendance Report
class AttendanceReportView(APIView):
    def get(self, request, lecture_id):
        # Instructors only
        lecture = get_object_or_404(Lecture, pk = lecture_id)
        attendances = Attendance.objects.filter(lecture = lecture).select_related('student')

        # Because we haven't linked Lecture to a specific Group in the model,
        # we might need a more complex approach to figure out which students belong.
        all_students = User.objects.filter(role = 'student')

        on_time = []
        late = []
        absent = []

        for student in all_students:
            try:
                record = attendances.get(student = student)
                start_datetime = timezone.make_aware(
                    timezone.datetime.combine(lecture.date, lecture.start_time)
                )
                arrival_time_diff = record.timestamp - start_datetime
                if arrival_time_diff <= timedelta(minutes = 30):
                    on_time.append(student.username)
                else:
                    late.append(student.username)
            except Attendance.DoesNotExist:
                absent.append(student.username)

        response_data = {
            "lecture": {
                "title": lecture.title,
                "start_time": str(lecture.start_time),
                "end_time": str(lecture.end_time)
            },
            "attendance": {
                "on_time": on_time,
                "late": late,
                "absent": absent
            }
        }
        return Response(response_data, status = status.HTTP_200_OK)
