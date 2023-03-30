import math
from collections import defaultdict

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core import serializers
from .decorators import redirect_to_dashboard
from .models import Waste, Venue, Recommendation, ActivityLog, Badge, UserBadge, ProfileImage, Category
from .forms import LoginForm, WasteForm, UserRegisterForm, UserUpdateForm, ProfileImageUpdateForm
from django.contrib import messages
from datetime import datetime


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile_image = ProfileImage(user=user)
            profile_image.save()

            # username = form.cleaned_data.get('username')
            messages.success(request, f'Вы успешно создали аккаунт!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})


@redirect_to_dashboard
def login_view(request):
    context = {
        'form': LoginForm(),
    }
    return render(request, 'main/login.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return reverse_lazy('dashboard')
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли!")
            log = ActivityLog(user=request.user, title="User:Вы успешно вошли!")
            log.save()
            return redirect('dashboard')
        else:
            messages.error(request, "Что то пошло не так!")
            return redirect('login')


def user_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли!")
    return redirect('login')


def get_monthly_score(request):
    current_month = datetime.now().strftime('%m')
    wastes_score_monthly = list(
        Waste.objects.filter(user=request.user, created_at__month__gte=current_month,
                             created_at__month__lte=current_month).values(
            'category__score', 'weight', 'unit__unit'))
    month_result = 0
    for el in wastes_score_monthly:
        if el['unit__unit'] == 'грамм':
            month_result += (el['weight'] / 1000) * el['category__score']
            continue
        if el['unit__unit'] == 'тонна':
            month_result += (el['weight'] * 1000) * el['category__score']
            continue
        month_result += el['weight'] * el['category__score']
    return round(month_result, 2)


def get_yearly_score(request):
    current_year = datetime.now().strftime('%Y')
    wastes_score_yearly = list(
        Waste.objects.filter(user=request.user, created_at__year__gte=current_year,
                             created_at__year__lte=current_year).values(
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


@login_required
def dashboard_view(request):
    context = {}
    context['wastes'] = Waste.objects.filter(user=request.user).order_by("-created_at")[:10]

    context['monthly_scores'] = get_monthly_score(request)

    context['yearly_scores'] = get_yearly_score(request)

    user_badges_count = request.user.user_badge.all().count()
    all_badges_count = Badge.objects.all().count()
    tasks_count = all_badges_count - user_badges_count
    context['tasks'] = tasks_count if tasks_count >= 0 else 0

    percentage = (user_badges_count * 100) // all_badges_count

    context['tasks_percentage'] = percentage

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
              'Nov', 'Dec']

    line_data = []
    for index in range(len(months)):
        all_sales = []
        wastes = Waste.objects.filter(user=request.user, created_at__month=index + 1)
        for waste in wastes:
            all_sales.append(waste.get_sum())
        line_data.append({'month': months[index], 'wastes': sum(all_sales)})
    context['line_data'] = json.dumps(line_data)

    pie_data = []

    hashmap = dict()
    categories = Category.objects.all()

    for category in categories:
        hashmap[category.title] = dict()
        hashmap[category.title]['weight'] = sum(
            list(Waste.objects.filter(user=request.user, category=category).values_list("weight", flat=True)))
        hashmap[category.title]['color'] = Category.objects.get(pk=category.pk).color
    context['pie_data'] = json.dumps(hashmap)
    context['categories'] = Category.objects.order_by('-title').values('title', 'color')

    return render(request, 'main/dashboard.html', context)


@login_required
def waste_list_view(request):
    context = {}
    context['wastes'] = Waste.objects.filter(user=request.user).order_by("-created_at")
    return render(request, 'main/waste_list.html', context)


@login_required
def venue_list_view(request):
    context = {}
    context['venues'] = Venue.objects.order_by("-created_at")
    return render(request, 'main/venue_list.html', context)


def badge_handler(request, waste):
    badges = Badge.objects.all().values("pk", "weight", "category__pk")
    total_weight = sum(
        list(Waste.objects.filter(user=request.user, category=waste.category).values_list('weight', flat=True)))
    print(badges)
    print(total_weight)
    print(waste.category.pk)
    for badge in badges:
        print(list(UserBadge.objects.filter(user=request.user).values_list('badge__pk', flat=True)))
        if total_weight >= badge['weight'] and waste.category.pk == badge['category__pk'] and badge['pk'] not in list(
                UserBadge.objects.filter(user=request.user).values_list('badge__pk', flat=True)):
            print("CONDITION WORKS")
            badge_obj = Badge.objects.get(pk=badge['pk'])
            user_badge = UserBadge(user=request.user, badge=badge_obj)
            user_badge.save()
            messages.success(request, f'Вы получили новое достижение "{user_badge.badge.title}"!')
            log = ActivityLog(user=request.user,
                              title=f'Badge:Вы получили новое достижение "{user_badge.badge.title}"!')
            log.save()


@login_required
def waste_create_view(request):
    context = {}
    form = WasteForm()

    if request.method == "POST":
        form = WasteForm(request.POST)
        if form.is_valid():
            waste = form.save(commit=False)
            waste.user = request.user
            waste.save()
            messages.success(request, "Новый отход успешно добавлен!")
            log = ActivityLog(user=request.user, title="Waste:Новый отход успешно добавлен!")
            log.save()
            badge_handler(request, waste)

            return redirect('waste_list')
        else:
            messages.error(request, "Что то пошло не так!")
            log = ActivityLog(user=request.user, title="Waste:Что то пошло не так!")
            log.save()
    else:
        context['form'] = form
        return render(request, 'main/waste_create.html', context)


@login_required
def waste_update_view(request, pk):
    obj = get_object_or_404(Waste, pk=pk)

    if request.method == "POST":
        form = WasteForm(request.POST or None, instance=obj)
        if form.is_valid():
            waste = form.save()
            messages.success(request, f"Отход № {pk} успешно изменен!")
            log = ActivityLog(user=request.user, title=f"Waste:Отход № {pk} успешно изменен!")
            log.save()

            badge_handler(request, waste)

            return redirect('waste_list')
    else:
        form = WasteForm(instance=obj)
        return render(request, 'main/waste_update.html', {"form": form})


@login_required
def waste_delete_view(request, pk):
    try:
        obj = Waste.objects.get(pk=pk)
        obj.delete()
        messages.success(request, f"Отход № {pk} успешно удален!")
        log = ActivityLog(user=request.user, title=f"Waste:Отход № {pk} успешно удален!")
        log.save()
    except Exception as e:
        print(str(e).upper())
        messages.error(request, f"При удалении отхода № {pk} что-то пошло не так!")
        log = ActivityLog(user=request.user, title=f"При удалении отхода № {pk} что-то пошло не так!")
        log.save()
    return redirect('waste_list')


@login_required
def get_recommendation(request):
    if request.method == "GET":
        category_id = request.GET.get("category_id")
        data = Recommendation.objects.get(category__pk=category_id)
        context = {
            "image": data.category.image.url,
            "title": data.title,
            "preview_text": data.preview_text,
            "text": data.text,
            "score": data.category.score
        }
        # json_data = serializers.serialize('json', context)
        return JsonResponse([context], safe=False)


@login_required
def get_all_venues_locations(request):
    if request.method == "GET":
        data = Venue.objects.values('lat', 'lon', 'title', 'image', 'location')
        return JsonResponse(list(data), safe=False)


@login_required
def activity_log_view(request):
    logs = ActivityLog.objects.filter(user=request.user)
    return render(request, 'main/activity_log.html', {'logs': logs})


@login_required
def task_list_view(request):
    tasks = Badge.objects.all()
    result = []
    user_badges = request.user.user_badge.all()
    all_badges = []
    print(user_badges)
    for i in user_badges:
        result.append(i.badge)

    for i in tasks:
        if i not in result:
            all_badges.append(i)
    context = {
        "user_badges": user_badges,
        "badges": all_badges
    }
    return render(request, "main/task_list.html", context)


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileImageUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile_image)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно изменен!')
            return redirect('profile_update')  # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileImageUpdateForm(instance=request.user.profile_image)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main/profile.html', context)
