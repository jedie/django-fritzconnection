# Generated by Django 4.0.3 on 2022-04-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djfritz', '0001_add_host_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostmodel',
            name='ip_v4',
            field=models.GenericIPAddressField(blank=True, help_text='HostModel.ip_v4.help_text', null=True, protocol='IPv4', verbose_name='HostModel.ip_v4.verbose_name'),
        ),
        migrations.AddField(
            model_name='hostmodel',
            name='ip_v6',
            field=models.GenericIPAddressField(blank=True, help_text='HostModel.ip_v6.help_text', null=True, protocol='IPv6', verbose_name='HostModel.ip_v6.verbose_name'),
        ),
    ]
