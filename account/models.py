# Подключаем классы для создания пользователей
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models  # Подключаем работу с моделями


# Создаем класс менеджера пользователей
class MyUserManager(BaseUserManager):
    # Создаём метод для создания пользователя
    def _create_user(self, email, username, password, **extra_fields):
        # Проверяем есть ли Email
        if not email:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Email")
        # Проверяем есть ли логин
        if not username:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Логин")
        # Делаем пользователя
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем всё остальное
        user.save(using=self._db)
        # Возвращаем пользователя
        return user

    # Делаем метод для создание обычного пользователя
    def create_user(self, email, username, password, **extra_fields):
        # Возвращаем нового созданного пользователя
        return self._create_user(email, username, password, **extra_fields)

    # Делаем метод для создание админа сайта
    def create_superuser(self, email, username, password):
        # Возвращаем нового созданного админа
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    username = models.CharField(max_length=50, unique=True)  # Логин
    email = models.EmailField(max_length=100, unique=True)  # Email
    is_active = models.BooleanField(default=True)  # Статус активации
    is_staff = models.BooleanField(default=False)  # Статус админа
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=250)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    USERNAME_FIELD = 'username'  # Идентификатор для обращения
    REQUIRED_FIELDS = ['email']  # Список имён полей для Superuser

    objects = MyUserManager()  # Добавляем методы класса MyUserManager

    # Метод для отображения в админ панели
    def __str__(self):
        return self.username


class Avatar(models.Model):
    user = models.OneToOneField(User, related_name='avatar', on_delete=models.CASCADE)
    img = models.ImageField(blank=True)

