from django.contrib.auth import authenticate, login
from accounts.forms import SignUpForm
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
# Create your views here.

def signup(request):
    if request.method == 'POST' :
        form = SignUpForm(request.POST)

        if form.is_valid() :
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username = username, password = raw_password)
            login(request, user) # 장고에서 제공하는 login 함수
            return render(request, 'accounts/signup_complete.html')
        
    else : 
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


    # if request.method == 'POST' :
    #     # TODO : 입력받은 내용을 통해 회원 생성
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     password2 = request.POST.get('password2')
    #     print(username, password, password2)
    #     # 객체 생성
    #     user = User()
    #     user.username = username
    #     user.set_password(password)
    #     user.save()
    #     return render(request, 'accounts/signup_complete.html')
    # else :
    #     context_values = {'form' : 'this is form'}
    #     return render(request, 'accounts/signup.html', context_values)
