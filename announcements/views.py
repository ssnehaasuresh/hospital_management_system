from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Announcements
from .forms import AnnouncementForm


@login_required
def announcement_list(request):
    announcements = Announcements.objects.all()
    return render(request, 'announcements/list.html', {'announcements': announcements})

@login_required
@role_required('staff')
def announcement_create(request):
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        ann = form.save(commit=False)
        ann.posted_by = request.user
        ann.save()
        return redirect('announcement_list')
    return render(request, 'announcements/form.html', {'form': form})
