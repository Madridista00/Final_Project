from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

from .models import Team

from django.core.paginator import Paginator

from django.views.generic.list import ListView
from django.views.generic import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

# Login / Logout
from django.contrib.auth.views import LoginView

# mixin 
from django.contrib.auth.mixins import LoginRequiredMixin

# Registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q


class RegisterPage(FormView):
    template_name = 'teams/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)

        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')

        return super(RegisterPage, self).get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'teams/login.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('main')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')    
        
        return super(CustomLoginView, self).get(*args, **kwargs)




class TeamsList(LoginRequiredMixin, ListView):
    model = Team
    template_name = "teams/main.html"
    context_object_name = 'teams'
    paginate_by = 4  

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        sort_by = self.request.GET.get('sort_by')

        queryset = self.model.objects.all()

        if search_query:
            if search_query.startswith("group "):
                group_letter = search_query.split("group ")[1].strip().upper()
                queryset = queryset.filter(
                    Q(group__iexact=group_letter)
                )
            else:
                queryset = queryset.filter(
                    Q(team__icontains=search_query) |
                    Q(group__icontains=search_query)
                )

        if sort_by == 'alphabetical':
            queryset = queryset.order_by('team')
        elif sort_by == 'group_asc':
            queryset = queryset.order_by('group')
        elif sort_by == 'group_desc':
            queryset = queryset.order_by('-group')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        context['sort_by'] = self.request.GET.get('sort_by', '')
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        context['sort_by'] = self.request.GET.get('sort_by', '')
        context['page'] = self.request.GET.get('page')
        context['query_params'] = self.request.GET.urlencode()
        return context

class TeamsDetail(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "teams/team.html"
    context_object_name = 'team'


class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    fields = ['team', 'logo', 'url', 'group', 'squad', 'qualifying', 'euro_best', 'coach', 'key_player', 'did_you_know']
    success_url = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not able to add a team.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TeamCreate, self).form_valid(form)


class TeamUpdate(LoginRequiredMixin, UpdateView):
    model = Team
    fields = ['team', 'logo', 'url', 'group', 'squad', 'qualifying', 'euro_best', 'coach', 'key_player', 'did_you_know']
    success_url = reverse_lazy('main')
    template_name = 'teams/team_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not able to update a team.")
        return super().dispatch(request, *args, **kwargs)


class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    context_object_name = 'team'
    success_url = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not able to delete a team.")
        return super().dispatch(request, *args, **kwargs)
