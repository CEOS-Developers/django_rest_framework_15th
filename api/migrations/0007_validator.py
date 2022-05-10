# Generated by Django 3.0.8 on 2022-05-10 15:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_relatedname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, validators=[django.core.validators.MinLengthValidator(2, '2글자 이상 입력하세요.')]),
        ),
    ]
