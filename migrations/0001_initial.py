# Generated by Django 4.0 on 2023-07-05 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, null=True)),
                ('service', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=50, null=True)),
                ('cost', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('book_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AddEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=50, null=True)),
                ('emp_id', models.CharField(max_length=50, null=True)),
                ('emp_name', models.CharField(max_length=50, null=True)),
                ('yoj', models.IntegerField(null=True)),
                ('mobile_no', models.CharField(max_length=10, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('salary', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=50, null=True)),
                ('utype', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50, null=True)),
                ('lname', models.CharField(max_length=50, null=True)),
                ('gender', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('pincode', models.IntegerField(null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('mobile_no', models.CharField(max_length=10, null=True)),
            ],
        ),
    ]