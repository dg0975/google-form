# Generated by Django 5.1.4 on 2024-12-12 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0010_remove_responses_response_code_texttype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='responses',
            old_name='response',
            new_name='answers',
        ),
    ]
