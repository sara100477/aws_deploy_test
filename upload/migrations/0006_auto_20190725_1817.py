# Generated by Django 2.2.3 on 2019-07-25 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_auto_20190725_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfilemodel',
            name='user_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]