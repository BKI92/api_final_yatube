# Generated by Django 3.0.6 on 2020-06-03 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_comment_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='group',
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_posts', to='api.Group'),
        ),
    ]
