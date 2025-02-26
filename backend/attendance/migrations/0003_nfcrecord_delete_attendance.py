# Generated by Django 5.1.4 on 2025-02-26 09:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_lecture_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='NFCRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('nfc_code', models.CharField(max_length=255)),
                ('auditorium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_records', to='attendance.auditorium')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]
