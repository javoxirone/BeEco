from django import template
from django.core.signing import dumps
from main.models import Waste
from datetime import datetime

register = template.Library()


@register.simple_tag()
def get_monthly_scores(user):
    current_month = datetime.now().strftime('%m')
    wastes_score_monthly = list(
        Waste.objects.filter(user=user, reated_at__month__gte=current_month, created_at__month__lte=current_month).values(
            'category__score', 'weight', 'unit__unit'))
    result = 0
    for el in wastes_score_monthly:
        if el['unit__unit'] == 'грамм':
            result += (el['weight'] / 1000) * el['category__score']
            continue
        if el['unit__unit'] == 'тонна':
            result += (el['weight'] * 1000) * el['category__score']
            continue
        result += el['weight'] * el['category__score']

    return round(result, 2)


@register.simple_tag()
def get_yearly_scores(user):
    current_year = datetime.now().strftime('%Y')
    wastes_score_yearly = list(
        Waste.objects.filter(user=user, created_at__year__gte=current_year, created_at__year__lte=current_year).values(
            'category__score', 'weight', 'unit__unit'))
    result = 0
    for el in wastes_score_yearly:
        if el['unit__unit'] == 'грамм':
            result += (el['weight'] / 1000) * el['category__score']
            continue
        if el['unit__unit'] == 'тонна':
            result += (el['weight'] * 1000) * el['category__score']
            continue
        result += el['weight'] * el['category__score']

    return round(result, 2)



