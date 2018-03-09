# Generated by Django 2.0.2 on 2018-03-09 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessPartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LetProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_number', models.CharField(max_length=6)),
                ('district', models.DecimalField(decimal_places=0, max_digits=2)),
                ('second_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seconds', to='partners.BusinessPartner')),
                ('third_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thirds', to='partners.BusinessPartner')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wins', to='partners.BusinessPartner')),
            ],
        ),
        migrations.CreateModel(
            name='PlannedProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_number', models.CharField(max_length=6)),
                ('district', models.DecimalField(decimal_places=0, max_digits=2)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('cost', models.CharField(max_length=30)),
                ('office', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('advance_date', models.DateField()),
                ('scrapped_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.LetProject')),
                ('prime', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asPrime', to='partners.BusinessPartner')),
                ('sub', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asSub', to='partners.BusinessPartner')),
            ],
        ),
    ]
