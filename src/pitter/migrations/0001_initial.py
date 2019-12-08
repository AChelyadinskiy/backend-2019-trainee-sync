# Generated by Django 2.2.7 on 2019-12-08 12:41

from django.db import migrations, models
import django.db.models.deletion
import pitter.models.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(default=pitter.models.base.default_uuid_id, editable=False, max_length=256,
                                        primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('login', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('salt', models.CharField(max_length=256)),
                ('profile', models.CharField(blank=True, max_length=256)),
                ('email', models.CharField(blank=True, max_length=256)),
                ('email_notification', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.CharField(default=pitter.models.base.default_uuid_id, editable=False, max_length=256,
                                        primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed',
                                               to='pitter.User')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower',
                                               to='pitter.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pitt',
            fields=[
                ('id', models.CharField(default=pitter.models.base.default_uuid_id, editable=False, max_length=256,
                                        primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('audio_file', models.FileField(upload_to='uploads/')),
                ('audio_file_transcription', models.CharField(max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pitter.User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
