# Generated by Django 2.0.2 on 2018-05-24 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspectors', '0002_auto_20180326_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspector',
            name='resume',
            field=models.FileField(blank=True, upload_to='', verbose_name='resume/'),
        ),
        migrations.AlterField(
            model_name='inspector',
            name='is_employee',
            field=models.BooleanField(default=False, verbose_name='Is this your Employee?'),
        ),
    ]
