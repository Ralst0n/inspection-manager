# Generated by Django 2.0.2 on 2018-08-22 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('stop_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inspector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('office', models.CharField(choices=[('King of Prussia', 'KOP'), ('Pittsburgh', 'PGH'), ('Test', 'TEST'), ('None', 'None')], default='None', max_length=30)),
                ('classification', models.CharField(blank=True, choices=[('TA-1', 'TA-1'), ('TA-2', 'TA-2'), ('TCI-1', 'TCI-1'), ('TCI-2', 'TCI-2'), ('TCI-3', 'TCI-3'), ('TCIS-1', 'TCIS-1'), ('TCIS-2', 'TCIS-2'), ('TCM', 'TCM')], default='TA-1', help_text='inspector classification i.e. TCI-2', max_length=6)),
                ('address', models.CharField(help_text="i.e. '321 Atwood St'", max_length=100, null=True)),
                ('home_city', models.CharField(blank=True, max_length=100)),
                ('home_state', models.CharField(blank=True, choices=[('Pennsylvania', 'PA'), ('New Jersey', 'NJ'), ('Delaware', 'DE'), ('Maryland', 'MD'), ('Ohio', 'OH'), ('New York', 'NY')], max_length=100)),
                ('home_zip', models.CharField(blank=True, max_length=5)),
                ('work_radius', models.DecimalField(decimal_places=0, help_text='number of miles', max_digits=3)),
                ('email', models.EmailField(max_length=60, verbose_name='E-mail')),
                ('phone_number', models.CharField(blank=True, max_length=10)),
                ('nicet_expiration', models.DateField(blank=True, null=True, verbose_name='NICET Expiration')),
                ('penndot_bituminous', models.DateField(blank=True, null=True, verbose_name='PennDOT Bituminous Expiration')),
                ('necept_bituminous', models.DateField(blank=True, null=True, verbose_name='NECEPT Expiration')),
                ('penndot_concrete', models.DateField(blank=True, null=True, verbose_name='PennDOT Concrete Expiration')),
                ('aci_concrete', models.DateField(blank=True, null=True, verbose_name='ACI Concrete Expiration')),
                ('is_employee', models.BooleanField(default=False, verbose_name='Is this your Employee?')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('inspector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspectors.Inspector')),
            ],
        ),
        migrations.AddField(
            model_name='history',
            name='inspector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspectors.Inspector'),
        ),
        migrations.AddField(
            model_name='history',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]
