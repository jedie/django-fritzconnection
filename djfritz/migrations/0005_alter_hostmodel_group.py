# Generated by Django 3.2.12 on 2022-04-08 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djfritz', '0004_host_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostmodel',
            name='group',
            field=models.ForeignKey(blank=True, help_text='HostModel.group.help_text', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hosts', to='djfritz.hostgroupmodel', verbose_name='HostModel.group.verbose_name'),
        ),
    ]
