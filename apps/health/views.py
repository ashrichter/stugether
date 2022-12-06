import datetime

from django.shortcuts import render, redirect

from apps.health.forms import HealthTrackerForm
from apps.health.models import Health
from apps.health.utilities import get_weekly_health_averages, get_weekly_health_totals, date_diff_in_seconds


def health_page(request):
    """ Displays the well being page

    :param request: http request
    :return: well being tracker page
    """
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        form = HealthTrackerForm()
        if request.method == 'POST':
            form = HealthTrackerForm(request.POST)
            if form.is_valid():
                sleep_start = datetime.datetime.strptime(request.POST.get("sleep_start"), '%Y-%m-%d %H:%M:%S')
                sleep_end = datetime.datetime.strptime(request.POST.get("sleep_end"), '%Y-%m-%d %H:%M:%S')
                sleep = date_diff_in_seconds(sleep_end, sleep_start)
                Health.objects.create(user=request.user, sleep=sleep,
                                      steps=request.POST.get("steps"),
                                      water=request.POST.get("water"))
                return redirect('health')

        # getting weekly avg data
        current_week = datetime.date.today().isocalendar()[1]
        health_data = Health.objects.filter(date__week=current_week, user=request.user)
        weekly_averages = get_weekly_health_averages(health_data)
        weekly_totals = get_weekly_health_totals(health_data)

        context = {
            'form': form,
            'title': 'Health',
            'active': 'health',
            'weekly_averages': weekly_averages,
            'weekly_totals': weekly_totals
        }

        return render(request, 'health/health.html', context)
