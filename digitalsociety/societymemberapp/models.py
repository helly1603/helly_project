from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True,max_length=30,blank=False)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Societymember(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=30)
    House_no = models.CharField(max_length=50)
    
    def __str__(self):
        return self.firstname
