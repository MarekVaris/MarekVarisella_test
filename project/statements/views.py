from django.shortcuts import render
from django.http import JsonResponse
from .models import report_turnover_by_year_month


def home(request):
    return render(request, "../templates/home.html")


def report_api(request):
    period_begin = request.GET.get('from')
    period_end = request.GET.get('to')

    if not period_begin or not period_end:
        return JsonResponse({'error': 'Missing from/to date'}, status=400)

    report = report_turnover_by_year_month(period_begin, period_end)
    return JsonResponse(report, safe=False)
