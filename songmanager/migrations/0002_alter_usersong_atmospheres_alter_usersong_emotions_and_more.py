# Generated by Django 4.2.13 on 2024-05-10 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersong',
            name='atmospheres',
            field=models.ManyToManyField(blank=True, to='songmanager.atmosphere'),
        ),
        migrations.AlterField(
            model_name='usersong',
            name='emotions',
            field=models.ManyToManyField(blank=True, to='songmanager.emotion'),
        ),
        migrations.AlterField(
            model_name='usersong',
            name='tags',
            field=models.ManyToManyField(blank=True, to='songmanager.tag'),
        ),
    ]
