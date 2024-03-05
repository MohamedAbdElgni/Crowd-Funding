# Generated by Django 5.0.3 on 2024-03-05 04:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundprojects', '0004_projectsreports'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('report', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_reports', to='fundprojects.comments')),
            ],
        ),
    ]
