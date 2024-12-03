from django.shortcuts import render
import uuid, time
from django.contrib.auth import logout, login
from djauth.handlers import isauth_f
from django.http import JsonResponse
from tgbot.config import TELEGRAM_BOT_USERNAME
from djbot.settings import TIME_OUT

from django.contrib.auth import get_user_model
User = get_user_model()

# user = User.objects.create_user(username="username",
#                                 first_name="first_name",
#                                 last_name="last_name",
#                                 idtlg="idtlg",
#                                 email="email",
#                                 token="token",
#                                 password="token")


def index(request):
    if request.user.is_authenticated:
        return render(request, 'auth.html')
    else:
        token = {"bot": TELEGRAM_BOT_USERNAME,"token": str(uuid.uuid4())}
        return render(request, 'index.html', token)


# def rqst_tlg(request):
#     user = User.objects.filter(id=2).first()
#     print(user)
#     login(request, user)
#     # return render(request, 'auth.html', user)  
#     return render(request, 'auth.html')  
    


def rqst_tlg(request):
    if request.method == 'POST':
        token = request.POST.get("token")
        intime = time.time()
        print("token", token)
        while True:
            print(token)
            user = User.objects.filter(token=token).first()
            if user:
                login(request, user)
                print("if user")
                # return render(request, 'auth.html', user)
                # return render(request, 'auth.html')
                
                return JsonResponse({"error": '0'})
            elif time.time() < intime + TIME_OUT:
                print(time.time(), "elif time.time() < intime + TIME_OUT")
                time.sleep(1)
            else:
                print("else")
                token = {"bot": TELEGRAM_BOT_USERNAME,"token": str(uuid.uuid4()),"massage":"Не получено авторизации от Telegram"}
                # return render(request, 'index.html', token)
                return JsonResponse({"error": '1', "message": token})     
    else:
        print("else-else")
        token = {"bot": TELEGRAM_BOT_USERNAME,"token": str(uuid.uuid4())}
        # return render(request, 'index.html', token) 
        return JsonResponse({"error": '1', "message": token}) 
    
    
    
    # if isauth_f(token):
    #     return render(request, 'auth.html')
    # else:
    #     return render(request, 'index.html')
    # return JsonResponse({"error": '0', "message": token})


def logout_view(request):
    logout(request)
    token = {"bot": TELEGRAM_BOT_USERNAME,"token": str(uuid.uuid4())}
    return render(request, 'index.html', token)
