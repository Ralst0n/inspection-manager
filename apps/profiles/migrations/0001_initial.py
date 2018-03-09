# Generated by Django 2.0.2 on 2018-03-09 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.CharField(choices=[('King of Prussia', 'KOP'), ('Pittsburgh', 'PGH'), ('Syracuse', 'SYR')], default='King of Prussia', max_length=30)),
                ('role', models.CharField(choices=[('Preparer', 'Preparer'), ('Manager', 'Manager'), ('Reviewer', 'Reviewer'), ('Observer', 'Observer')], default='Observer', max_length=30)),
                ('receive_newsletter', models.BooleanField(default=True, verbose_name='Would you like to receive notification emails?')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
