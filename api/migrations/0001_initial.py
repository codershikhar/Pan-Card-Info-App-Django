# Generated by Django 3.1.1 on 2020-10-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PanInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.TextField()),
                ('fathers_name', models.TextField()),
                ('date_of_birth', models.DateField()),
                ('pan_number', models.TextField()),
                ('scanned_signature', models.FileField(upload_to='')),
                ('photo', models.FileField(upload_to='')),
                ('pan_file', models.FileField(upload_to='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pan_info',
            },
        ),
    ]
