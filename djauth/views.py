import uuid, time, logging
from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import JsonResponse
from tgbot.config import TELEGRAM_BOT_USERNAME, SITE_TO_AUTH
from djbot.settings import TIME_OUT
from django.contrib.auth import get_user_model
User = get_user_model()

logging.basicConfig(level=logging.INFO, filename='log_tgbot.log',
                    format='%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.INFO)

# Страница авторизации
def index(request):
    # Если пользователь авторизован - привествие
    if request.user.is_authenticated:
        name = f'{request.user.first_name} {request.user.last_name} ({request.user.username})'
        message = {'username': name, 'site':SITE_TO_AUTH}
        return render(request, 'auth.html', message )
    # Если не авторизован - генерируется токен и передается в форму броузера пользователя
    # для формирования GET-запроса в Telegram
    else:
        token = {'bot': TELEGRAM_BOT_USERNAME,'token': str(uuid.uuid4()),'site':SITE_TO_AUTH}
        return render(request, 'index.html', token)

# Обработчик запроса из броузера пользователя
# При нажатии пользователем кнопки "Войти через Telegram", формируется два запроса
# 1. В Telegram. Этот запрос обрабатывается в bot.py
# 2. В Django, этот обработчик.
def rqst_tlg(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        # Засекаем время, начиная с которого ждем появления пользователя и/или токена в базе данных 
        intime = time.time()
        # Каждую секунду проверяем не появился ли пользователь и/или токен в базе данных
        while True:
            # Выбираем запись базы данных с токеном равным пришедшим от пользователя
            user = User.objects.filter(token=token).first()
            # Если такой пользователь нашелся - авторизуем его механизмом Django 
            if user:
                login(request, user)
                # Возвращаем признак успешной авторизации в JS броузера пользователя
                return JsonResponse({'error': '0'})
            # Если время ожидания меньше, чем установленный в settings.py, ждем секунду и новый цикл
            elif time.time() < intime + TIME_OUT:
                time.sleep(1)
            # Если время ожидания больше TIME_OUT, отправляем пользователю 
            # в броузер сообщение о невозможности авторизоваться через Telegram
            # также отправляем новый токен
            else:
                token = {'bot': TELEGRAM_BOT_USERNAME,'token': str(uuid.uuid4()),'massage':'Не получено авторизации от Telegram'}
                return JsonResponse({'error': '1', 'message': token})     
    else:
        # Если пришел не POST запрос - ппризнак ошибки в JS броузера пользователя 
        token = {'bot': TELEGRAM_BOT_USERNAME,'token': str(uuid.uuid4())}
        return JsonResponse({'error': '1', 'message': token}) 

# Обрабочик выхода из авторизации, возвращаем начальную страницу
def logout_view(request):
    logout(request)
    token = {'bot': TELEGRAM_BOT_USERNAME,'token': str(uuid.uuid4()),'site':SITE_TO_AUTH}
    return render(request, 'index.html', token )
