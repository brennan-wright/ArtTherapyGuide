# Generated by Django 3.2.11 on 2022-01-30 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directive', '0005_auto_20220130_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectiveTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Applicable theme for directive')),
            ],
        ),
        migrations.RemoveField(
            model_name='directivepage',
            name='diagnosis',
        ),
        migrations.DeleteModel(
            name='DirectiveDiagnosis',
        ),
        migrations.AddField(
            model_name='directivepage',
            name='theme',
            field=models.ManyToManyField(help_text='*Use <kbd>CTRL</kbd> + click on windows, or <kbd>CMD ⌘</kbd> + click on a Mac to select more than one.', related_name='educationposts', to='directive.DirectiveTheme', verbose_name='Target Theme'),
        ),
    ]
