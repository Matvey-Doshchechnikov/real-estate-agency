from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    BUILDING_CHOICES = [
        (True, 'Новостройка'),
        (False, 'Старое здание'),
        (None, 'Не заполнено'),
    ]
    new_building = models.BooleanField(choices=BUILDING_CHOICES, null=True, blank=True)
    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)
    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True
    )
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное'
    )
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4'
    )
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж'
    )
    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True
    )
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True
    )
    has_balcony = models.NullBooleanField('Наличие балкона', db_index=True)
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True
    )
    liked_by = models.ManyToManyField(User, related_name='liked_flats', blank=True)
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True
    )

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Complaint(models.Model):
    user = models.ForeignKey(User, related_name='user_complaints', on_delete=models.CASCADE)
    apartment = models.ForeignKey(Flat, related_name='apartment_complaints', on_delete=models.CASCADE)
    text = models.TextField('Текст жалобы', max_length=1000)

    def __str__(self):
        return f'Complaint by {self.user} on {self.apartment}'


class Owner(models.Model):
    holder = models.CharField('ФИО владельца', max_length=200)
    pure_phone = PhoneNumberField('Нормализованный номер телефона', blank=True)
    phonenumber = models.CharField('Номер владельца', max_length=20)
    apartments = models.ManyToManyField('Flat', related_name='owned_by', blank=True)

    def __str__(self):
        return self.holder

