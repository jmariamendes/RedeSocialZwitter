# Generated by Django 4.0.4 on 2022-07-12 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dwitter', '0011_controlemsgs_exibida_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dweet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dweets', to=settings.AUTH_USER_MODEL),
        ),
    ]
