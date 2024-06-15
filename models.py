from django.db import models

class UserLogin(models.Model):
    username = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,null=True)
    utype = models.CharField(max_length=50,null=True)


class UserRegistration(models.Model):
    fname = models.CharField(max_length=50,null=True)
    lname = models.CharField(max_length=50,null=True)
    gender = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=50,null=True)
    pincode = models.IntegerField(null=True)
    email = models.CharField(max_length=50,null=True)
    mobile_no = models.CharField(max_length=10,null=True)

class AddEmployee(models.Model):
    emp_name = models.CharField(max_length=50,null=True)
    yoj = models.IntegerField(null=True)
    experience = models.CharField(max_length=50,null=True)
    mobile_no = models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=50,null=True)
    profile = models.FileField(upload_to='document/',null=True)

class AddBooking(models.Model):
    user_id = models.CharField(max_length=50,null=True)
    service = models.CharField(max_length=500,null=True)
    description = models.CharField(max_length=500,null=True)
    cost = models.IntegerField(null=True)
    status = models.CharField(max_length=50,null=True)
    book_date = models.DateField(null=True)
    provider_id = models.CharField(max_length=50,null=True)
    payment_status = models.CharField(max_length=50, null=True)


class GiveFeedback(models.Model):
    user_id = models.CharField(max_length=50,null=True)
    service = models.CharField(max_length=50,null=True)
    comments = models.CharField(max_length=50,null=True)


class UploadDesigns(models.Model):
    user_id = models.CharField(max_length=50,null=True)
    service_type = models.CharField(max_length=50,null=True)
    design_photo = models.FileField(upload_to='documents/',null=True)


class AddPayment(models.Model):
    user_id = models.CharField(max_length=50,null=True)
    book_id = models.CharField(max_length=50,null=True)
    amount = models.IntegerField(null=True)
    paid_date = models.DateField(null=True)
    provider_id = models.CharField(max_length=50,null=True)









