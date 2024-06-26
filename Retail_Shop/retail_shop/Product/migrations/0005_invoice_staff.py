# Generated by Django 4.2.7 on 2024-03-24 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0004_customeraccount_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('invoice_id', models.CharField(blank=True, db_column='Invoice_Id', max_length=200, null=True)),
                ('customer_id', models.IntegerField(blank=True, db_column='Customer_Id', null=True)),
                ('shipping_cost', models.DecimalField(blank=True, db_column='Shipping_Cost', decimal_places=2, max_digits=10, null=True)),
                ('labour_cost', models.DecimalField(blank=True, db_column='Labour_Cost', decimal_places=2, max_digits=10, null=True)),
                ('vat', models.DecimalField(blank=True, db_column='Vat', decimal_places=2, max_digits=10, null=True)),
                ('discount', models.DecimalField(blank=True, db_column='Discount', decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(blank=True, db_column='Totall', decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'invoice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.AutoField(db_column='Staff_Id ', primary_key=True, serialize=False)),
                ('staff_name', models.CharField(blank=True, db_column='Staff_Name', max_length=255, null=True)),
                ('salary', models.DecimalField(blank=True, db_column='Salary', decimal_places=2, max_digits=10, null=True)),
                ('phone_Number', models.CharField(blank=True, db_column='Phone_Number', max_length=255, null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=200, null=True)),
            ],
            options={
                'db_table': 'staff',
                'managed': False,
            },
        ),
    ]
