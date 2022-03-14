# Generated by Django 3.2 on 2021-05-01 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0019_rename_amaount_orderinfo_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='reqbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=13)),
                ('title', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_status',
            field=models.CharField(default='not delivered', max_length=50),
        ),
    ]