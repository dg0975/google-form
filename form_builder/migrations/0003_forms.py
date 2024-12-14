# Generated by Django 5.1.4 on 2024-12-08 13:18

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0002_user_created_user_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Forms',
            },
        ),
    ]