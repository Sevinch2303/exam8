from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import League, Team
from .models import Vacancy


class LeagueDetailView(DetailView):
    model = League
    template_name = 'league_detail.html'
    context_object_name = 'league'

class TeamListView(ListView):
    model = Team
    template_name = 'team_list.html'
    context_object_name = 'teams'



class LeagueListView(ListView):
    model = League
    template_name = 'league_list.html'


def soft_delete_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)


    user.delete()

    return redirect('home')


def restore_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    user.is_active = True
    user.save()

    return redirect('home')




def filter_vacancies_by_salary(request, salary_amount):
    filtered_vacancies = Vacancy.objects.filter(salary_from__lte=salary_amount, salary_to__gte=salary_amount)

    context = {
        'filtered_vacancies': filtered_vacancies,
        'salary_amount': salary_amount,
    }
    return render(request, 'filtered_vacancies.html', context)
