# Generated by Django 5.0.3 on 2024-03-09 23:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundprojects', '0014_alter_project_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpicture',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_images', to='fundprojects.project'),
        ),
    ]