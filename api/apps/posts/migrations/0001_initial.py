# Generated by Django 3.2.8 on 2022-01-04 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nodes', '0004_alter_node_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created_at')),
                ('modified_at', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified_at')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('body', models.TextField(blank=True, verbose_name='body')),
                ('views', models.IntegerField(default=0, verbose_name='views')),
                ('pinned', models.BooleanField(default=False, verbose_name='pinned')),
                ('highlighted', models.BooleanField(default=False, verbose_name='highlighted')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('edited_at', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='body', verbose_name='edited at')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='nodes.node', verbose_name='node')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
        ),
    ]
