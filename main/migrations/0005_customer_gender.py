# Generated by Django 4.0.1 on 2022-04-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_fabric_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1),
        ),
    ]
