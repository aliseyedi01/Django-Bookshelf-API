# Generated by Django 5.0.2 on 2024-03-05 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_otptoken_otp_code_alter_otptoken_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='cdf618', max_length=6),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
