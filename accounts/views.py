from django.shortcuts import render
from accounts.decorators import role_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django_ratelimit.decorators import ratelimit
from patients.models import Patient
from appointments.models import Appointment
from leaves.models import LeaveRequest
from announcements.models import Announcements
from datetime import date
from django.core.cache import cache

def login_view(request):
    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR')
        cache_key = f'login_attempts_{ip}'
        attempts = cache.get(cache_key, 0)

        if attempts >= 5:
            return render(request, 'accounts/login.html', {
                'error': 'Too many login attempts. Please wait 1 minute.'
            })

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            cache.delete(cache_key)  # reset on successful login
            login(request, user)
            if user is not None:
                cache.delete(cache_key)
                login(request, user)
            return redirect('/dashboard/')
        else:
            cache.set(cache_key, attempts + 1, timeout=60)  # 60 second timeout
            return render(request, 'accounts/login.html', {
                'error': f'Invalid credentials. Attempt'
            })

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


@login_required
def dashboard(request):
    today = date.today()
    user = request.user

    if user.role == 'admin':
        context = {
            'patient_count': Patient.objects.count(),
            'todays_appointments': Appointment.objects.filter(date=today).count(),
            'pending_leaves': LeaveRequest.objects.filter(status='pending').count(),
            'announcement_count': Announcements.objects.count(),
            'recent_appointments': Appointment.objects.filter(date=today)[:5],
            'recent_announcements': Announcements.objects.all()[:3],
        }
        return render(request, 'dashboard_admin.html', context)
    
    elif user.role == 'doctor':
        context = {
            'patient_count': Patient.objects.count(),
            'todays_appointments': Appointment.objects.filter(date=today).count(),
            'pending_leaves': LeaveRequest.objects.filter(status='pending').count(),
            'announcement_count': Announcements.objects.count(),
            'recent_appointments': Appointment.objects.filter(date=today)[:5],
            'recent_announcements': Announcements.objects.all()[:3],
        }
        return render(request, 'dashboard_doctor.html', context)

    else:  # staff
        context = {
        'patient_count': Patient.objects.count(),
        'todays_appointments': Appointment.objects.filter(date=today).count(),
        'total_appointments': Appointment.objects.count(),
        'recent_appointments': Appointment.objects.filter(date=today)[:5],
        'recent_announcements': Announcements.objects.all()[:3],
        }
        return render(request, 'dashboard_staff.html', context)