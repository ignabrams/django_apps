# Generated by Django 3.2.15 on 2022-12-15 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-created', 'slug']},
        ),
    ]
