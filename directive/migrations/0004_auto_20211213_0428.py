# Generated by Django 3.2.5 on 2021-12-13 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directive', '0003_auto_20211018_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directivepage',
            name='discussion',
            field=models.TextField(max_length=2000, null=True, verbose_name='Directive Discussion'),
        ),
        migrations.DeleteModel(
            name='DirectiveImage',
        ),
    ]
