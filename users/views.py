from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logouts
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse





class LoginAjaxView(View):

    def post(self, request):
        email = request.POST.get('username')
        password = request.POST.get('password')

        if email and password:
            print(email, password)
            user = authenticate(username=email, password=password)
            print(user)
            if user:
                login(request, user)
                return JsonResponse(
                    data={
                        'status': 201
                    },
                    status=200
                )
            return JsonResponse(
                data={
                    'status': 400,
                    'error': 'Пароль и логин не валидные'
                },
                status=200
            )
        return JsonResponse(
            data={
                'status': 400,
                'error': 'Введите логин и пароль'
            },
            status=200
        )


def logout(request):
    if request.method == 'POST':
        logouts(request)
        return redirect('index')