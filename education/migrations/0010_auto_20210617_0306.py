# Generated by Django 3.1.10 on 2021-06-17 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_auto_20210617_0258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educationpage',
            name='audience',
        ),
        migrations.DeleteModel(
            name='EducationAudience',
        ),
    ]