# Generated by Django 2.2.3 on 2019-07-25 07:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_uploadfilemodel_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfilemodel',
            name='product_id',
        ),
        migrations.AddField(
            model_name='uploadfilemodel',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='published date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadfilemodel',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]