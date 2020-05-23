from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from app.forms import LoginForm, SignUpForm, AddTicketForm, EditTicketForm
from app.models import Tickets, MyUser


# Create your views here.
@login_required
def index(request):
    new = Tickets.objects.filter(status='NEW')
    in_progress = Tickets.objects.filter(status='IN_PROGRESS')
    done = Tickets.objects.filter(status='DONE')
    invalid = Tickets.objects.filter(status='INVALID')
    return render(request, 'index.html', {
        'new': new,
        'in_progress': in_progress,
        'done': done,
        'invalid': invalid
    }
    )


def login_view(request):
    html = 'login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', 'index.html')
                )
    form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    if request.user:
        logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_view(request, username):
    data = MyUser.objects.get(username=username)
    tickets_assigned = Tickets.objects.filter(
        assigned_to=MyUser.objects.get(username=username)
    )
    tickets_filed = Tickets.objects.filter(
        filed_by=MyUser.objects.get(username=username)
    )
    tickets_completed = Tickets.objects.filter(
        completed_by=MyUser.objects.get(username=username)
    )
    return render(
        request,
        'user_detail.html',
        {
            'data': data,
            'tickets_filed': tickets_filed,
            'tickets_completed': tickets_completed,
            'tickets_assigned': tickets_assigned
        }
    )


def ticket_detail(request, id):
    html = 'ticket_detail.html'
    data = Tickets.objects.get(id=id)
    return render(request, html, {'data': data})


def ticket_edit(request, id):
    html = 'ticket_edit.html'
    ticket = Tickets.objects.get(id=id)
    if request.method == 'POST':
        form = EditTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data['title']
            ticket.description = data['description']
            ticket.save()
        return HttpResponseRedirect(reverse('homepage'))
    form = EditTicketForm(initial={
        'title': ticket.title,
        'description': ticket.description
    })
    return render(request, html, {'ticket': ticket, 'form': form})


def add_ticket(request):
    html = 'add_ticket.html'
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.filed_by = request.user
            new_ticket.save()
        return HttpResponseRedirect(reverse('homepage'))
    form = AddTicketForm()
    return render(request, html, {'form': form})


def claim_ticket(request, id):
    url = reverse('ticket', kwargs={'id': id})
    data = Tickets.objects.get(id=id)
    data.status = 'IN_PROGRESS'
    data.assigned_to = request.user
    data.completed_by = None
    data.save()
    return HttpResponseRedirect(url)


def ticket_done(request, id):
    data = Tickets.objects.get(id=id)
    data.status = 'DONE'
    data.completed_by = request.user
    data.assigned_to = None
    data.save()
    return HttpResponseRedirect(reverse('homepage'))


def ticket_invalid(request, id):
    data = Tickets.objects.get(id=id)
    data.status = 'INVALID'
    data.assigned_to = None
    data.completed_by = None
    data.save()
    return HttpResponseRedirect(reverse('homepage'))
