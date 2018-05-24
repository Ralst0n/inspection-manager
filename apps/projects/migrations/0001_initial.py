# Generated by Django 2.0.2 on 2018-05-24 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('partners', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('prudent_number', models.CharField(help_text='i.e. 101.083', max_length=7, primary_key=True, serialize=False)),
                ('penndot_number', models.CharField(help_text='i.e. E02430', max_length=6)),
                ('office', models.CharField(choices=[('King of Prussia', 'KOP'), ('Pittsburgh', 'PGH'), ('Test', 'TEST')], default='King of Prussia', max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('district', models.DecimalField(decimal_places=0, max_digits=2)),
                ('start_date', models.DateField()),
                ('payroll_budget', models.DecimalField(decimal_places=2, default=30000.0, max_digits=9)),
                ('other_cost_budget', models.DecimalField(decimal_places=2, default=30000.0, max_digits=9)),
                ('straight_hours_budget', models.DecimalField(decimal_places=2, default=2000.0, max_digits=9)),
                ('overtime_hours_budget', models.DecimalField(decimal_places=2, default=2000.0, max_digits=9)),
                ('active', models.BooleanField(default=True, help_text='Is this project actively being worked on?')),
                ('completed', models.BooleanField(default=False)),
                ('budget_letter', models.BooleanField(default=False, verbose_name='75 percent letter sent')),
                ('business_partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.BusinessPartner')),
            ],
        ),
    ]
