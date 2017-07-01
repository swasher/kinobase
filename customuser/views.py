# coding: utf-8
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db import IntegrityError

#from .forms import UserRegistrationForm



# def user_registration(request):
#     """
#     User account registration view.
#     """
#     #check if user is already logged in and if he is redirect him to some other url, e.g. home
#     if request.user.is_authenticated():
#         if request.user.is_authenticated():
#             messages.add_message(request, messages.ERROR, 'You are logged in already. Please log out first.')
#             return redirect('/login/')
#
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         #email, password = request.POST['email'], request.POST['password']
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = form.cleaned_data['email'].split('@')[0]
#
#             try:
#                 user.save()
#             except IntegrityError:
#                 #messages.add_message(request, messages.SUCCESS, 'this email already used')
#                 form.add_error('email', 'this email already used')
#                 form.email = user.username
#                 return render(request, 'registration/login.html', {'form': form})
#
#             user = authenticate(username=user.email, password=user.password)
#             if user is not None:
#                 if user.is_active:
#                     messages.add_message(request, messages.SUCCESS, 'You are sucessfully registered!')
#                     login(request, user)
#                     return HttpResponseRedirect('/')
#                 else:
#                     messages.add_message(request, messages.SUCCESS, 'Your account are disabled')
#                     return HttpResponseRedirect('hello')
#             else:
#                 messages.add_message(request, messages.WARNING, 'Invalid login')
#                 return HttpResponseRedirect('login')
#     else:
#         form = UserRegistrationForm()
#
#     return render(request, 'registration/login.html', {'form': form})
#
#
# def user_login(request):
#
#     form = UserRegistrationForm()
#
#     if request.user.is_authenticated():
#         messages.add_message(request, messages.ERROR, 'You are logged in already. Please log out first.')
#         return redirect('/')
#
#     if request.POST:
#         form = UserRegistrationForm(data=request.POST)
#         email = request.POST['email']
#         password = request.POST['password']
#
#         user = authenticate(username=email, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 messages.add_message(request, messages.SUCCESS, 'You are sucessfully login!')
#                 return redirect('/')
#         else:
#             users = get_user_model()
#             email_found = users.objects.filter(email=email)
#             if email_found:
#                 form.add_error('password', 'incorrect password')
#             else:
#                 form.add_error('email', 'this email not registered')
#
#     return render(request, 'registration/login.html', {'form': form})