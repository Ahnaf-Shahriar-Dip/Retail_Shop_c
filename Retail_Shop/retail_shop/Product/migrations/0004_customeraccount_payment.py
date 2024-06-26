# Generated by Django 4.2.3 on 2023-11-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('customer_account_id', models.AutoField(db_column='Customer_Account_Id', primary_key=True, serialize=False)),
                ('total_buys', models.DecimalField(blank=True, db_column='Total_Buys', decimal_places=2, max_digits=10, null=True)),
                ('total_paid', models.DecimalField(blank=True, db_column='Total_Paid', decimal_places=2, max_digits=10, null=True)),
                ('total_due', models.DecimalField(blank=True, db_column='Total_Due', decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'customer_account',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(db_column='Payment_Id', primary_key=True, serialize=False)),
                ('payment_date', models.DateField(blank=True, db_column='Payment_Date', null=True)),
                ('payment_amount', models.DecimalField(blank=True, db_column='Payment_Amount', decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'payment',
                'managed': False,
            },
        ),
    ]
