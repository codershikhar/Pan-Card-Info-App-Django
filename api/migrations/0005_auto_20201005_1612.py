# Generated by Django 3.1.1 on 2020-10-05 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201005_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paninfo',
            name='pan_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.file'),
        ),
    ]