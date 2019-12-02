# Generated by Django 2.2.7 on 2019-12-02 08:47

from django.db import migrations, models
import pitter.models.base


class Migration(migrations.Migration):
    dependencies = [
        ('pitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pitt',
            fields=[
                ('id', models.CharField(default=pitter.models.base.default_uuid_id, editable=False, max_length=256,
                                        primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(max_length=256)),
                ('audio_file', models.CharField(max_length=1024)),
                ('audio_file_transcription', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
