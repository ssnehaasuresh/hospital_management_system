from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import LeaveRequest
from .forms import LeaveRequestForm

@login_required
@role_required('admin','doctor')
def leave_list(request):
    leaves = LeaveRequest.objects.filter(staff=request.user)
    return render(request, 'leaves/list.html', {'leaves': leaves})

@login_required
def leave_create(request):
    form = LeaveRequestForm(request.POST or None)
    if form.is_valid():
        leave = form.save(commit=False)
        leave.staff = request.user
        leave.save()
        return redirect('leave_list')
    return render(request, 'leaves/form.html', {'form': form})

@login_required
@role_required('admin')
def leave_approve(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'approved'
    leave.save()
    return redirect('leave_admin_list')

@login_required
@role_required('admin')
def leave_reject(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'rejected'
    leave.save()
    return redirect('leave_admin_list')

@login_required
@role_required('admin')
def leave_admin_list(request):
    leaves = LeaveRequest.objects.all().order_by('-start_date')
    return render(request, 'leaves/admin_list.html', {'leaves': leaves})
