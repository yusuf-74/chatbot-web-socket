from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/register-login.html')
    
    def post(self, request):
        data = dict(request.POST)
        
        username = data['username'][0]
        password = data['password'][0]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'chat/chat-view.html')
        else:
            return render(request, 'auth/register-login.html', {'error': 'Invalid username or password'})

class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register-login.html')
    
    def post(self, request):
        data = dict(request.POST)
        
        username = data['username'][0]
        password = data['password'][0]
        repeat_password = data['repeat_password'][0]
        email = data['email'][0]
        
        user = User.objects.create_user(username, email, password)
        user.save()
        
        login(request, user)
        
        return render(request, 'chat/chat-view.html')

    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'auth/register-login.html')
