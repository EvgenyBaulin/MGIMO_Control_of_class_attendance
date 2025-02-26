from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .permissions import IsInstructor, IsStudent
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    GroupSerializer,
    UserSerializer,
    AuditoriumSerializer,
    LectureSerializer,
    NFCRecordSerializer,
    MyTokenObtainPairSerializer
)
from .models import *
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


# 1. Student Registration
class StudentRegisterView(APIView):
    permission_classes = []
    
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'student'
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student registered successfully!'}, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Instructor Registration
class InstructorRegisterView(APIView):
    permission_classes = []
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
        if self.action == 'list':
            # Allow unauthenticated access for listing groups (needed for registration)
            return []
        # For other actions (create, update, delete) keep the instructor permission
        return [IsInstructor()]


# 4. Auditorium Management (ViewSet)
class AuditoriumViewSet(viewsets.ModelViewSet):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer
    permission_classes = [IsInstructor]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auditorium = serializer.save()
        # Генерируем NFC код
        import uuid
        nfc_code = uuid.uuid4().hex
        auditorium.nfc_code = nfc_code
        # Формируем ссылку для автоматической отметки
        auditorium.nfc_link = f"http://mgimo.tarakan-tuc.ru/nfc_attendance.html?code={nfc_code}"
        auditorium.save()

        return Response(self.serializer_class(auditorium).data, status=status.HTTP_201_CREATED)

    def update_nfc(self, request, pk=None):
        auditorium = get_object_or_404(Auditorium, pk=pk)
        new_code = request.data.get('nfc_code')
        if not new_code:
            return Response({'error': 'No NFC code provided.'}, status=status.HTTP_400_BAD_REQUEST)
        auditorium.nfc_code = new_code
        auditorium.nfc_link = f"http://mgimo.tarakan-tuc.ru/nfc_attendance.html?code={new_code}"
        auditorium.save()
        return Response(self.serializer_class(auditorium).data, status=status.HTTP_200_OK)


# 5. Lecture Management (ViewSet)
class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Lecture.objects.all().select_related('auditorium').prefetch_related('groups')

    def list(self, request, *args, **kwargs):
        lectures = self.get_queryset()
        data = []
        for lecture in lectures:
            lecture_data = {
                'id': lecture.id,
                'title': lecture.title,
                'date': str(lecture.date),
                'start_time': str(lecture.start_time),
                'end_time': str(lecture.end_time),
                'auditorium': lecture.auditorium.name,
                'groups': [group.name for group in lecture.groups.all()],
            }
            data.append(lecture_data)
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            lecture = serializer.save()
            response_data = {
                'id': lecture.id,
                'title': lecture.title,
                'date': str(lecture.date),
                'start_time': str(lecture.start_time),
                'end_time': str(lecture.end_time),
                'auditorium': lecture.auditorium.name,
                'groups': [group.name for group in lecture.groups.all()],
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # Instructors only
        return super().destroy(request, *args, **kwargs)


# 6. Attendance Tracking
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def record_nfc(request):
    """
    Просто записываем NFC отметку
    """
    code = request.data.get('code')
    if not code:
        return Response({'error': 'NFC code is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Находим аудиторию по коду
        auditorium = Auditorium.objects.get(nfc_code=code)
        
        # Сохраняем NFC-отметку
        nfc_record = NFCRecord.objects.create(
            student=request.user,
            auditorium=auditorium,
            nfc_code=code
        )

        return Response({
            'message': 'NFC record saved',
            'record_id': nfc_record.id,
            'timestamp': nfc_record.timestamp
        }, status=status.HTTP_201_CREATED)

    except Auditorium.DoesNotExist:
        return Response({'error': 'Invalid NFC code'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 7. Attendance Report
class AttendanceReportView(APIView):
    permission_classes = [IsInstructor]

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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LectureAttendanceView(APIView):
    permission_classes = [IsInstructor]

    def get(self, request, lecture_id):
        lecture = get_object_or_404(Lecture, id=lecture_id)
        
        # Получаем всех студентов из групп лекции
        students = CustomUser.objects.filter(
            role='student',
            group__in=lecture.groups.all()
        ).distinct()

        # Получаем временные границы лекции
        lecture_date = lecture.date
        lecture_start = timezone.datetime.combine(
            lecture_date,
            lecture.start_time,
            tzinfo=timezone.get_current_timezone()
        )
        lecture_end = timezone.datetime.combine(
            lecture_date,
            lecture.end_time,
            tzinfo=timezone.get_current_timezone()
        )

        # Получаем все NFC-записи для этой аудитории в период лекции
        nfc_records = NFCRecord.objects.filter(
            auditorium=lecture.auditorium,
            timestamp__date=lecture_date,
            timestamp__gte=lecture_start - timedelta(minutes=20),  # Разрешаем отметиться за 20 минут до начала
            timestamp__lte=lecture_end
        ).select_related('student', 'student__group')

        on_time = []
        late = []
        absent = []

        for student in students:
            # Ищем самую раннюю отметку студента
            student_record = nfc_records.filter(student=student).order_by('timestamp').first()
            
            if not student_record:
                absent.append({
                    'id': student.id,
                    'username': student.username,
                    'group': student.group.name if student.group else 'No Group'
                })
                continue

            # Приводим timestamp к той же временной зоне, что и lecture_start
            record_time = student_record.timestamp.astimezone(timezone.get_current_timezone())
            
            # Если отметился до начала лекции или в течение 15 минут после начала
            if record_time <= lecture_start + timedelta(minutes=15):
                on_time.append({
                    'id': student.id,
                    'username': student.username,
                    'group': student.group.name if student.group else 'No Group',
                    'timestamp': record_time
                })
            else:
                late.append({
                    'id': student.id,
                    'username': student.username,
                    'group': student.group.name if student.group else 'No Group',
                    'timestamp': record_time
                })

        return Response({
            'lecture_info': {
                'title': lecture.title,
                'date': str(lecture.date),
                'start_time': str(lecture.start_time),
                'end_time': str(lecture.end_time),
                'auditorium': lecture.auditorium.name,
                'auditorium_nfc_code': lecture.auditorium.nfc_code,
                'groups': [group.name for group in lecture.groups.all()]
            },
            'on_time': on_time,
            'late': late,
            'absent': absent,
            'stats': {
                'total_students': len(students),
                'on_time_count': len(on_time),
                'late_count': len(late),
                'absent_count': len(absent)
            }
        })


class StudentAttendanceHistoryView(APIView):
    permission_classes = [IsInstructor]

    def get(self, request, student_id):
        student = get_object_or_404(User, id=student_id, role='student')
        attendance_records = Attendance.objects.filter(student=student).select_related('lecture')
        
        lectures = Lecture.objects.all()
        history = []
        
        for lecture in lectures:
            lecture_start = timezone.datetime.combine(
                lecture.date,
                lecture.start_time,
                tzinfo=timezone.get_current_timezone()
            )
            
            try:
                record = attendance_records.get(lecture=lecture)
                if record.timestamp <= lecture_start + timedelta(minutes=15):
                    status = "on_time"
                else:
                    status = "late"
            except Attendance.DoesNotExist:
                status = "absent"
                
            history.append({
                'lecture': {
                    'id': lecture.id,
                    'title': lecture.title,
                    'date': lecture.date,
                    'start_time': lecture.start_time,
                    'end_time': lecture.end_time,
                },
                'status': status
            })
            
        return Response({
            'student': {
                'id': student.id,
                'username': student.username,
                'email': student.email
            },
            'history': history
        })


class StudentListView(APIView):
    permission_classes = [IsInstructor]

    def get(self, request):
        students = User.objects.filter(role='student')
        data = [{
            'id': student.id,
            'username': student.username,
            'email': student.email
        } for student in students]
        return Response(data)


class NFCRecordsListView(APIView):
    permission_classes = [IsInstructor]

    def get(self, request):
        try:
            records = NFCRecord.objects.select_related('student', 'student__group', 'auditorium').all().order_by('-timestamp')
            data = []
            for record in records:
                try:
                    data.append({
                        'id': record.id,
                        'student': {
                            'id': record.student.id,
                            'username': record.student.username,
                            'group': record.student.group.name if record.student and record.student.group else 'No Group'
                        },
                        'auditorium': record.auditorium.name if record.auditorium else 'Unknown',
                        'timestamp': record.timestamp,
                        'nfc_code': record.nfc_code
                    })
                except Exception as e:
                    print(f"Error processing record {record.id}: {str(e)}")
                    continue
            
            return Response(data)
        except Exception as e:
            print(f"Error in NFCRecordsListView: {str(e)}")
            return Response(
                {'error': 'Internal server error', 'details': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
