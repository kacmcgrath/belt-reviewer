# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.

### User models and managers here

class UserManager(models.Manager):
    def check_reg(self, postData):
        response = []
        errors = []
        if not len(postData['fname']) > 2:
            errors.append("First name must be longer than 2 characters.")
        if not len(postData['lname']) > 2:
            errors.append("Last name must be longer than 2 characters.")
        if not EMAIL_REGEX.match(postData['email']) or User.objects.filter(email = postData['email']):
            errors.append("Please enter a valid email address.")
        if not len(postData['pword']) > 8:
            errors.append("Password must be longer than 8 characters.")
        if not postData['pword'] == postData['conf_pword']:
            errors.append("Passwords must match.")
        if errors:
            response.append(False)
            response.append(errors)
        else:
            response.append(True)
            response.append(User.objects.create(fname=postData['fname'], lname=postData['lname'], email=postData['email'], pword=postData['pword']))
        return response

    def check_login(self, postData):
        response = []
        errors = []
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Please enter a valid email address.")
        if not len(postData['pword']) > 0:
            errors.append("Oops!  Did you forget something?")
        if errors:
            response.append(False)
            response.append(errors)
        else:
            response.append(True)
            response.append(User.objects.get(email=postData['email']))
        return response

class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    pword = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

### Book/review models and managers here

class ReviewManager(models.Manager):
    def check_review(self, postData, request):
        response = []
        errors = []
        if not len(postData['aname']) > 2:
            errors.append('Please enter an author name.')
        if not len(postData['title']) > 0:
            errors.append('Please enter a title.')
        if not len(postData['review']) > 0:
            errors.append('Please enter a review.')
        if not postData['rating'] > 0:
            errors.append('Please select a rating')
        if errors:
            response.append(False)
            response.append(errors)
        else:
            a = Author.objects.get_or_create(name=postData['aname'])
            b = Book.objects.get_or_create(title=postData['title'])
            if a[1] or b[1]:
                b[0].author.add(a[0])
            r = Review.objects.create(review=postData['review'], rating=postData['rating'], reviewer=User.objects.get(id=request.session['user_id']))
            r.book = b[0]
            r.save()
            response.append(True)
            response.append(b[0])
        print response
        return response

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, related_name="books", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

class Review(models.Model):
    reviewer = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews", null=True)
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()
