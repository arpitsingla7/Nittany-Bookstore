# Generated by Django 3.2 on 2021-04-30 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0011_auto_20210430_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentdb',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]