from django.urls import path
from .views import (
    StudentRegisterView,
    InstructorRegisterView,
    GroupViewSet,
    AuditoriumViewSet,
    LectureViewSet,
    record_nfc,
    LectureAttendanceView,
    StudentAttendanceHistoryView,
    StudentListView,
    NFCRecordsListView
)

urlpatterns = [
    # Registration
    path('register/student/', StudentRegisterView.as_view(), name='register_student'),
    path('register/instructor/', InstructorRegisterView.as_view(), name='register_instructor'),

    # Group
    path('groups/', GroupViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='groups'),

    # Auditorium
    path('auditoriums/', AuditoriumViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='auditoriums'),
    path('auditoriums/<int:pk>/nfc/', AuditoriumViewSet.as_view({
        'patch': 'update_nfc'
    }), name='auditoriums_nfc'),

    # Lecture
    path('lectures/', LectureViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='lectures'),
    path('lectures/<int:pk>/', LectureViewSet.as_view({
        'delete': 'destroy'
    }), name='delete_lecture'),
    path('lectures/<int:lecture_id>/attendance/', LectureAttendanceView.as_view(), name='lecture-attendance'),

    # NFC Records
    path('nfc-record/', record_nfc, name='record_nfc'),
    path('nfc-records/', NFCRecordsListView.as_view(), name='nfc-records-list'),
]
