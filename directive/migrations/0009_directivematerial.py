# Generated by Django 3.2 on 2021-09-26 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directive', '0008_remove_directivepage_discussion'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectiveMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=250, verbose_name='Directive Materials')),
                ('directive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='directive.directivepage')),
            ],
        ),
    ]