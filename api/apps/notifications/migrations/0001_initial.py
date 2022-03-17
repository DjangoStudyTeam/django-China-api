# Generated by Django 3.2.8 on 2022-03-17 02:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.TREE_COMMENT_MODEL),
        ('notifications_plus', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notifications_plus.notification')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.TREE_COMMENT_MODEL)),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
            },
            bases=('notifications_plus.notification',),
        ),
    ]
