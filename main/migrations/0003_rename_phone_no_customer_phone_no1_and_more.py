# Generated by Django 4.0.1 on 2022-02-13 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_clothe_id_alter_customer_id_alter_tailor_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='phone_no',
            new_name='phone_no1',
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_no2',
            field=models.IntegerField(null=True),
        ),
    ]
