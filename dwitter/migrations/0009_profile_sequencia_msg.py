# Generated by Django 4.0.4 on 2022-07-04 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0008_mensagens_msg_ativa_mensagens_sequencia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sequencia_msg',
            field=models.IntegerField(default=0),
        ),
    ]