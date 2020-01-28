# Generated by Django 2.2.4 on 2020-01-28 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_account_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts_tasks', to='tasks.Account'),
        ),
    ]