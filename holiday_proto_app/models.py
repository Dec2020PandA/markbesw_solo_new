from django.db import models

import re

# Create your models here.

class UserManager(models.Manager):
    def validate(self, postdata):
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postdata['f_n']) < 2:
            errors['f_n'] = "First name must be 2 or more characters"
        if len(postdata['l_n']) < 2:
            errors['l_n'] = "Last name must be 2 or more characters"
        if not email_check.match(postdata['email']):
            errors['email'] = "Invalid email address"
        if len(postdata['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters"
        if postdata['pw'] != postdata['conf_pw']:
            errors['conf_pw'] = "Password does not match confirm password"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # cards: list of Card's owned by this user. Here as a reminder comment...

class Page(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    img_file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Card(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    img_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="cards", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
