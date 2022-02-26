# Generated by Django 4.0.1 on 2022-02-22 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_rename_location_tailor_phone_no1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no1', models.TextField(null=True)),
                ('phone_no2', models.TextField(null=True)),
                ('spec', multiselectfield.db.fields.MultiSelectField(choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Baby'), ('T', 'Traditional'), ('O', 'Modern'), ('C', 'Classic')], default='M', max_length=6)),
                ('rating', models.IntegerField(choices=[(1, 'Bad'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], default=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
