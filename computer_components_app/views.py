from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,UpdateView,DeleteView,CreateView,TemplateView
from .models import Component,Manufacturer,Type
from .forms import *
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group


class Main(LoginRequiredMixin, TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_manager = Group.objects.get(name='Manager') in user.groups.all()
        context['is_manager'] = is_manager
        return context

class ManufacturerListView(LoginRequiredMixin,ListView):
    queryset = Manufacturer.objects.all()
    context_object_name = 'list_object'
    template_name = 'list.html'

class ManufacturerDetailView(LoginRequiredMixin, DetailView):
    model = Manufacturer
    context_object_name = 'object'
    template_name = 'manufacturer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_manager = self.request.user.groups.filter(name='Manager').exists()
        context['is_manager'] = is_manager
        return context

class ManufacturerUpdateView(LoginRequiredMixin,UpdateView):
    model = Manufacturer
    fields = ['name']
    template_name = 'update.html'  
    success_url = '/manufacturers'

class ManufacturertDeleteView(LoginRequiredMixin,DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("manufacturers")
    template_name = 'delete.html'    

class ManufacturerCreateView(LoginRequiredMixin,CreateView):
    model = Manufacturer
    fields = ["name"]
    template_name = 'create.html'

class TypeListView(LoginRequiredMixin,ListView):
    queryset = Type.objects.all()
    context_object_name = 'list_object'
    template_name = 'list.html'

class TypeDetailView(LoginRequiredMixin, DetailView):
    model = Type
    context_object_name = 'object'
    template_name = 'type_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_manager = self.request.user.groups.filter(name='Manager').exists()
        context['is_manager'] = is_manager
        return context

class TypeUpdateView(LoginRequiredMixin,UpdateView):
    model = Type
    fields = ['name']
    template_name = 'update.html'  
    success_url = '/types' 

class TypetDeleteView(LoginRequiredMixin,DeleteView):
    model = Type
    success_url = reverse_lazy("types")
    template_name = 'delete.html'  

class TypeCreateView(LoginRequiredMixin,CreateView):
    model = Type
    fields = ["name"]
    template_name = 'create.html'

class ComponentListView(LoginRequiredMixin,ListView):
    queryset = Component.objects.all()
    context_object_name = 'list_object'
    template_name = 'list.html'

class ComponentDetailView(LoginRequiredMixin, DetailView):
    model = Component
    context_object_name = 'object'
    template_name = 'component_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_manager = self.request.user.groups.filter(name='Manager').exists()
        context['is_manager'] = is_manager
        return context

class ComponentUpdateView(LoginRequiredMixin,UpdateView):
    model = Component
    fields = ['name', 'type', 'manufacturer']
    template_name = 'update.html'  
    success_url = '/components'  

class ComponentDeleteView(LoginRequiredMixin,DeleteView):
    model = Component
    success_url = reverse_lazy("components")
    template_name = 'delete.html'  

class ComponentCreateView(LoginRequiredMixin,CreateView):
    model = Component
    fields = ["name","manufacturer","type"]
    template_name = 'create.html'



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('main')

@login_required
def change_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Username successfully updated.')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UsernameChangeForm()
    return render(request, 'change_username.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Password successfully updated.')
            return redirect('main')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})