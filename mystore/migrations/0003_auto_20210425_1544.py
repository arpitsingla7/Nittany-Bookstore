# Generated by Django 3.2 on 2021-04-25 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0002_alter_registerdb_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registerdb',
            old_name='fname',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='registerdb',
            old_name='lname',
            new_name='lastname',
        ),
    ]
