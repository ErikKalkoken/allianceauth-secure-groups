# Generated by Django 4.0.10 on 2023-11-20 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('securegroups', '0013_useringroupfilter_reversed_logic'),
    ]

    operations = [
        migrations.AddField(
            model_name='useringroupfilter',
            name='groups',
            field=models.ManyToManyField(
                related_name='in_group', to='auth.group'),
        ),
    ]
