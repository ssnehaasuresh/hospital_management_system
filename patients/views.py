from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm
from accounts.decorators import role_required
from appointments.models import Appointment
# Create your views here.

@login_required
def patient_list(request):
    patients=Patient.objects.all().order_by('full_name')
    return render(request, 'patients/list.html', {'patients': patients})

@login_required
def patient_detail(request, pk):
    patient=get_object_or_404(Patient, pk=pk)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')
    return render(request, 'patients/detail.html', {'patient':patient, 'appointments': appointments})

@login_required
@role_required('admin','staff')
def patient_create(request):
    form=PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('patient_list')
    return render(request, 'patients/form.html', {'form': form, 'title': 'Add Patient' })

@login_required
@role_required('admin','staff')
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('patient_detail', pk=pk)
    return render(request, 'patients/form.html', {'form': form, 'title': 'Edit Patient'})

@login_required
@role_required('admin','staff')
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/confirm_delete.html', {'patient': patient})
