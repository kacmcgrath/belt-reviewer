# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from .models import User, Book, Author, Review

from django.contrib import messages


# Create your views here.
### These are all user-related views

def index(request):
    print request.session
    return render(request, 'books/index.html')

# Register Users
def register(request):
    if request.method == "POST":
        response = User.objects.check_reg(request.POST)
        if response[0]:
            request.session['user_id'] = response[1].id
            request.session['name'] = response[1].fname
        else:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
    return redirect('/books')

# Log in Users
def login(request):
    if request.method == "POST":
        response = User.objects.check_login(request.POST)
        if response[0]:
            request.session['name'] = response[1].fname
            request.session['user_id'] = response[1].id
        else:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
        return redirect('/books')

# Log out users
def logout(request):
    request.session.flush()
    return redirect('/')

### Book and review related views are here

# display reviews for all books
def books(request):
    context = {
        'reviews': Review.objects.order_by('-created_at')[0:10],
        'other_reviews':Review.objects.order_by('-created_at')[10:],
        'authors': Author.objects.all(),
        'books': Book.objects.all()
    }
    return render(request, 'books/books.html', context)

# display form for adding reviews
def add(request):
    return render(request, 'books/add.html')

# process new reviews
def process(request):
    if request.method == "POST":
        response = Book.objects.check_review(request.POST, request)
        if not response[0]:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/add')
    return redirect('/book/{}'.format(response[1].id))

# delete a specific review
def delete_review(request, id):
    r = Review.objects.get(id=id)
    r.delete()
    messages.add_message(request, messages.SUCCESS, 'You have successfully deleted your review on this title.')
    return redirect('/book/{}'.format(r.book_id))

# display/edit a specific book
def book(request, id):
    b = Book.objects.get(id=id)
    context = {
        'book': b,
        'author': Author.objects.filter(books=b),
    }
    return render(request, 'books/book.html', context)

# display/edit a specific user
def user(request, id):
    u = User.objects.get(id=id)
    context = {
        'user': u,
        'reviews': Review.objects.filter(reviewer=u)
    }
    return render(request, 'books/user.html', context)
