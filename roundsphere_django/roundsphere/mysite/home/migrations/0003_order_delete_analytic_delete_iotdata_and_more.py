# Generated by Django 5.1.3 on 2024-12-20 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_analytic_analyticid_alter_iotdata_dataid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderId', models.AutoField(primary_key=True, serialize=False)),
                ('quatity', models.PositiveIntegerField(null=True)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'Order_data',
                'ordering': ['orderId'],
            },
        ),
        migrations.DeleteModel(
            name='Analytic',
        ),
        migrations.DeleteModel(
            name='Iotdata',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='profileId',
            new_name='userId',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='postcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('admin', 'Admin'), ('researcher', 'Researcher')], default='researcher', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user'),
        ),
    ]
