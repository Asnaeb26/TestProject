# Generated by Django 4.0 on 2022-01-13 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_tickets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickets',
            name='messages',
        ),
        migrations.AddField(
            model_name='message',
            name='ticket',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='firstapp.tickets'),
            preserve_default=False,
        ),
    ]
