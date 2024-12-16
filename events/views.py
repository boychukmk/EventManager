from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, EventForm
from .models import Event
from django.contrib import messages
from django.db.models import Q


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def event_list(request):
    search_query = request.GET.get('search', '')

    events = Event.objects.filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(location__icontains=search_query)
    ).order_by('-date')

    return render(request, 'event_list.html', {'events': events, 'search_query': search_query})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_create.html', {'form': form})


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        messages.error(request, "You are not the organizer of this event.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event successfully updated!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_create.html', {'form': form})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        messages.error(request, "You are not the organizer of this event.")
        return redirect('event_list')

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event successfully deleted!')
        return redirect('event_list')

    return render(request, 'event_confirm_delete.html', {'event': event})


@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user not in event.attendees.all():
        event.attendees.add(request.user)

    return redirect('event_list')
