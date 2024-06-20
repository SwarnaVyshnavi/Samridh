# Generated by Django 5.0.3 on 2024-04-08 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifiedOrganizations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('profile_photo', models.ImageField(default='verified_organizations/Org_dp.jpg', upload_to='verified_organizations/')),
                ('certificate', models.FileField(blank=True, null=True, upload_to='verified_organizations/certificate/')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=30)),
                ('pincode', models.CharField(max_length=7)),
                ('head_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organization.organizationheads')),
            ],
        ),
    ]