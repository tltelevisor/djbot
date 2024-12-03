from django.shortcuts import render
import uuid, time
from django.contrib.auth import logout, login
from django.http import JsonResponse
from tgbot.config import TELEGRAM_BOT_USERNAME
from djbot.settings import TIME_OUT
from django.contrib.auth import get_user_model
User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        return render(request, 'auth.html')
    else:
        token = {"bot": TELEGRAM_BOT_USERNAME,"token": str(uuid.uuid4())}
        return render(request, 'index.html', token)


def rqst_tlg(request):
    if request.method == 'POST':
        token = request.POST.get("token")
        intime = time.time()
        while True:
            user = User.objects.filter(token=token).first()
            if user:
                login(request, user)
                return JsonResponse({"error": '0'})
            elif time.time() < intime + TIME_OUT:
                time.sleep(1)
            else:
                token = {"bot": TELEGRAM_BOT_USERNAME,"token": str(uuid.uuid4()),"massage":"Не получено авторизации от Telegram"}
                return JsonResponse({"error": '1', "message": token})     
    else:
        token = {"bot": TELEGRAM_BOT_USERNAME,"token": str(uuid.uuid4())}
        return JsonResponse({"error": '1', "message": token}) 
    
def logout_view(request):
    logout(request)
    token = {"bot": TELEGRAM_BOT_USERNAME,"token": str(uuid.uuid4())}
    return render(request, 'index.html', token)
