from django.shortcuts import render,  redirect
from django.contrib import messages
from .models import *
import bcrypt 
import re

def index(request):
    return render (request, 'login.html')

def register(request):
    if request.method=='POST':
        errors=User.objects.reg_validator(request.POST)
        if len(errors) !=0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        hashed_pw=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], 
        password=hashed_pw)
        request.session['user']=new_user.first_name
        request.session['user_id']=new_user.id
        return redirect('/success')
    return redirect('/')

def login(request):
    if request.method=='POST':
        errors=User.objects.log_validator(request.POST)
        if len(errors) !=0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        this_user=User.objects.get(email=request.POST['email'])
        request.session['user_id']= this_user.id
        request.session['user']=this_user.first_name
        return redirect('/success')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect ('/')
    context= {
        'booklist': Book.objects.all()
    }
    return render(request, 'books.html', context)   

def add_book(request):
    if request.method=="POST":
        errors=Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/success')
        else:
            title= request.POST['title']
            description= request.POST['description']
            user= User.objects.get(id=request.session['user_id'])
            book= Book.objects.create(
                title=title,
                description=description,
                uploaded_by=user
                )
            user.favorited_books.add(book)
        return redirect('/success')

def view_book(request,id):
    if 'user_id' not in request.session:
        return redirect ('/')
    one_book=Book.objects.filter(id=id)
    if len(one_book) !=1:
        return redirect('/success')
    context={
        'book': one_book[0],
    }
    
    return render(request,'view.html', context)

def update(request, id):
    if request.method=="POST":
        errors=Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect(f"/view_book/{id}")
        else:
            one_book=Book.objects.filter(id=id)
            print(one_book)
            if len(one_book) !=1:
                return redirect('/success')
            elif one_book[0].uploaded_by.id != request.session['user_id']:
                return redirect(f"/view_book/{id}")
            one_book[0].title=request.POST['title']
            one_book[0].description = request.POST['description']
            one_book[0].save()
    return redirect(f"/view_book/{id}")

def delete(request, id):
    if request.method=='POST':
        one_book=Book.objects.filter(id=id)
        if len(one_book) !=1:
            return redirect('/success')
        elif one_book[0].uploaded_by.id != request.session['user_id']:
            return redirect(f"/view_book/{id}")
        one_book[0].delete()
    return redirect('/success')

  
def favorite(request, id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=id)
    user.favorited_books.add(book)
    return redirect('/success')

def unfavorite(request, id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=id)
    user.favorited_books.remove(book)
    return redirect('/success')

# Create your views here.
