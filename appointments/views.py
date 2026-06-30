from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.shortcuts import render, get_object_or_404,redirect
from .forms import AppointmentForm
from accounts.decorators import role_required
# Create your views here.
@login_required
def appointment_list(request):
    if request.user.role == 'doctor':
        appointments = Appointment.objects.filter(staff=request.user)
    else:
        appointments = Appointment.objects.all()
    return render(request, 'appointments/list.html', {'appointments': appointments})

@login_required
def appointment_detail(request, pk):
    appt = get_object_or_404(Appointment, pk=pk,)
    return render(request, 'appointments/detail.html', {'appt': appt})

@login_required
@role_required('admin', 'staff')
def appointment_create(request):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('appointment_list')
    return render(request, 'appointments/form.html', {'form': form})

@login_required
def appointment_cancel(request, pk):
    if request.user.role == 'doctor':
        appt = get_object_or_404(Appointment, pk=pk, staff=request.user)
    else:
        appt = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        appt.status = 'cancelled'
        appt.save()
        return redirect('appointment_list')
    return render(request, 'appointments/confirm_cancel.html', {'appt': appt})

@login_required
@role_required('doctor')
def appointment_complete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, staff=request.user)
    if request.method == 'POST':
        appt.status = 'completed'
        appt.save()
        return redirect('appointment_list')
    return render(request, 'appointments/confirm_complete.html', {'appt': appt})
