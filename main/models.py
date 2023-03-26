from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class ProfileImage(models.Model):
    image = models.ImageField(upload_to="profile/", default="profile/no-image.png", verbose_name="Рисунок")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Пользователь",
                                related_name="profile_image")

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return f"ProfileImage(username={self.user.username})"

    class Meta:
        verbose_name = "Рисунок профиля"
        verbose_name_plural = "Рисунки профиля"


class Category(models.Model):
    title = models.CharField(max_length=250, unique=True, null=False, blank=False, verbose_name="Категория")
    image = models.ImageField(upload_to="category/", null=False, blank=False, verbose_name="Рисунок")
    score = models.IntegerField(null=False, blank=False, verbose_name="Балл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Category(title={self.title})"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Venue(models.Model):
    title = models.CharField(max_length=250, unique=True, null=False, blank=False, verbose_name="Заголовок")
    image = models.ImageField(upload_to="venue/", null=False, blank=False, verbose_name="Рисунок")
    location = models.CharField(max_length=500, null=False, blank=False, verbose_name="Геолокация")
    lat = models.FloatField(blank=True, null=True, verbose_name="Широта")
    lon = models.FloatField(blank=True, null=True, verbose_name="Долгота")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Venue(title={self.title})"

    class Meta:
        verbose_name = "Место сбора"
        verbose_name_plural = "Места сбора"


class MeasurementUnit(models.Model):
    unit = models.CharField(max_length=50, null=False, blank=False, verbose_name="Ед. измерение")

    def __str__(self):
        return self.unit

    def __repr__(self):
        return f"MeasurementUnit(unit={self.unit})"

    class Meta:
        verbose_name = "Ед. измерение"
        verbose_name_plural = "Ед. измерения"


class Waste(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Пользователь")
    title = models.CharField(max_length=250, null=False, blank=False, verbose_name="Заголовок")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Категория", related_name="waste")
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Место сбора")
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True, blank=False,
                             verbose_name="Ед. измерение")
    weight = models.FloatField(default=1, null=False, blank=False, verbose_name="Вес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Waste(title={self.title})"

    class Meta:
        verbose_name = "Отход"
        verbose_name_plural = "Отходы"

    def get_update_url(self):
        return reverse('waste_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('waste_delete', kwargs={'pk': self.pk})

    def get_sum(self):
        sum = 0
        if self.unit.unit == "тонна":
            sum = (self.weight * 1000) * self.category.score
        elif self.unit.unit == "грамм":
            sum = (self.weight / 1000) * self.category.score
        else:
            sum = self.weight * self.category.score
        return round(sum, 2)


class Recommendation(models.Model):
    category = models.ForeignKey(Category, unique=True, on_delete=models.CASCADE, null=False, blank=False,
                                 verbose_name="Категория")
    title = models.CharField(max_length=150, blank=False, null=False, verbose_name="Заголовок")
    preview_text = models.TextField(null=False, blank=False, verbose_name="Текст")
    text = models.TextField(null=False, blank=False, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Recommendation(title={self.title})"

    class Meta:
        verbose_name = "Рекомендации"
        verbose_name_plural = "Рекомендации"


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Пользователь")
    title = models.CharField(max_length=150, blank=False, null=False, verbose_name="Заголовок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"ActivityLog(title={self.title})"

    class Meta:
        verbose_name = "Журнал активности"
        verbose_name_plural = "Журнал активности"


class Badge(models.Model):
    image = models.ImageField(upload_to="badge/", null=False, blank=False, verbose_name="Бейдж")
    title = models.CharField(max_length=150, null=False, blank=True, verbose_name="Заголовок")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Категории")
    weight = models.FloatField(default=0, null=False, blank=False, verbose_name="Вес")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Badge(title={self.title})"

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Пользователь",
                             related_name="user_badge")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Достижение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.badge.title

    def __repr__(self):
        return f"UserBadge(title={self.badge.title})"

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"
