# Generated by Django 3.1.6 on 2021-02-18 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210218_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroompostcomment',
            name='classroom',
        ),
    ]
