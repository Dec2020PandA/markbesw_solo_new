# Generated by Django 2.2 on 2020-12-13 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('holiday_proto_app', '0003_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='holiday_proto_app.User'),
            preserve_default=False,
        ),
    ]
