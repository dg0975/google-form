# Generated by Django 5.1.4 on 2024-12-11 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0007_user_email_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
