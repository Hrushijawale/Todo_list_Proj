# Generated by Django 4.2.9 on 2024-01-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_todotask_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email_host_password',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email_host_user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
