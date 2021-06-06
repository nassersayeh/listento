from django.contrib.messages import default_app_config
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
import re
from django.db.models.fields import BooleanField
class UserManger(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # add keys and values to errors dictionary for each invalid field
        if postData['password'] != postData['confirmPass']:
            errors['notsame']="password doesnt equal confirmation"
        if len(postData['first_name'])<2:
            errors['short']="fname should be atleast 2 letters"
        if len(postData['last_name'])<2:
            errors['shorts']="lname should be atleast 2 letters"
        if len(User.objects.filter(email=postData['email']))!=0:
            errors['unique']="email is not unqiue" 
        if len(postData['password']) < 8:
            errors["desc"] = "password should be at least 8 characters"
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors
    def login_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors

# Create your models here.
class Role(models.Model):
    role=models.CharField(max_length=5)


class Gender(models.Model):
    gender=models.CharField(max_length=6)


class User(models.Model):
    
    username=models.CharField(max_length=45)
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birh_date=models.DateTimeField()
    image = models.ImageField(upload_to='images/',default='pic.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender=models.ForeignKey(Gender,related_name="users",on_delete=models.CASCADE)
    role=models.ForeignKey(Role,related_name="users",on_delete=models.CASCADE)
    objects = UserManger() 

class LOL(models.Model):
    bool=models.BooleanField(default=False)
    user=models.ForeignKey(User,related_name="requests",on_delete=models.CASCADE)
    
class Follower(models.Model):
    followeduser=models.ForeignKey(User,related_name="userfollowers",on_delete=models.CASCADE)
    followinguser=models.ForeignKey(User,related_name="userfollowings",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)