# Generated by Django 3.0 on 2020-04-21 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='p_no',
            new_name='sno',
        ),
    ]