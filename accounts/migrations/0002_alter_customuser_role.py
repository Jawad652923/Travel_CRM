# Generated by Django 5.1.1 on 2024-09-16 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('sales_agent', 'Sales Agent'), ('admin', 'Admin')], max_length=20),
        ),
    ]
