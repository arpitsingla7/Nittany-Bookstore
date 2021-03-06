# Generated by Django 3.2 on 2021-04-29 13:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0006_bookdb_keywordm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authordb',
            name='isbn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mystore.bookdb', validators=[django.core.validators.MinLengthValidator(13)]),
        ),
        migrations.AlterField(
            model_name='bookdb',
            name='isbn',
            field=models.CharField(max_length=13, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(13)]),
        ),
    ]
