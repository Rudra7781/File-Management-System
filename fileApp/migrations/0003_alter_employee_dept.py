# Generated by Django 4.0.5 on 2022-07-07 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileApp', '0002_file_upload_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dept',
            field=models.CharField(choices=[('I.T', 'IT'), ('H.R', 'HR')], max_length=10),
        ),
    ]