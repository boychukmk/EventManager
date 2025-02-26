from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework.decorators import permission_classes,  api_view
from rest_framework.response import Response
from rest_framework import generics, permissions, status

from EventManager import settings
from .forms import UserRegistrationForm, EventForm
from .models import Event
from .serializers import EventSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organiser=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.organiser != self.request.user:
            raise PermissionDenied("You are not allowed to edit this event.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.organiser != self.request.user:
            raise PermissionDenied("You are not allowed to delete this event.")
        instance.delete()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_event_api(request):
    serializer = EventSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(organiser=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_event_api(request, pk):
    try:
        event = Event.objects.get( pk=pk)
        if event.organiser != request.user:
            return Response({"detail":"You are not allowed to edit this event."},
                           status=status.HTTP_403_FORBIDDEN)

    except Event.DoesNotExist:
        return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(organiser=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_event_api(request, pk):
    try:
        event = Event.objects.get(pk=pk)

        if event.organiser != request.user:
            return Response({"detail": "You are not the organiser of this event."},
                            status=status.HTTP_403_FORBIDDEN)
    except Event.DoesNotExist:
        return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

    event.delete()
    return Response({"detail": "Event deleted successfully ."}, status=status.HTTP_204_NO_CONTENT)


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {"form": form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'event_list')
            return redirect(next_url)

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {"form": form})


def logout_user(request):
    logout(request)

    return redirect('user_login')


def event_list(request):
    search_query = request.GET.get('search', '')
    events = Event.objects.filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(location__icontains=search_query)
    ).order_by('-date')

    return render(request, 'event_list.html' ,
                  {'events': events, 'search_query': search_query})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organiser = request.user
            event.save()
            return redirect('event_list')

    else:
        form = EventForm()

    return render(request, 'event_create.html', {"form": form})


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organiser != request.user:
        messages.error(request, 'You are not allowed to edit this event.')
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event successfully updated.')
            return redirect('event_list')

    else:
        form = EventForm(instance=event)

    return render(request, 'event_create.html', {"form": form})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organiser != request.user:
        messages.error(request, 'You are not allowed to delete this event.')
        return redirect('event_list')

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event successfully deleted.')
        return redirect('event_list')

    return render(request , 'event_confirm_delete.html', {"event": event})


@login_required
def register_for_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    if request.user not in event.attendees.all():
        event.attendees.add(request.user)
        subject = "Registration on event"
        html_message = render_to_string('email/event_registration.html', {
            'user': request.user,
            'event': event,
        })
        plain_message = strip_tags(html_message)
        recipient = request.user.email
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [recipient],
            html_message=html_message
        )
    return redirect('event_list')