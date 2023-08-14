from django.shortcuts import render, redirect
from django.views import View
from . forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
from .models import OtpCode, User
from django.contrib import messages
import random
from utils import send_otp_code, check_code_expire
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    

    def post(self, requeset):
        form = self.form_class(requeset.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # handle it by clean_fields in forms
            # if User.objects.filter(email=cd['email']).exists() or User.objects.filter(phone_number=cd['phone_number']).exists():
            #     messages.error(requeset, 'phone number or email is used before,', 'warning')
            #     return render(requeset, self.template_name, {'form': form})

            random_code = random.randint(10000, 99999)
            send_otp_code(phone_number=cd['phone_number'], code=random_code)


            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)

            # session is save in server and a hash of that is on client sys
            requeset.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password']
            }

            messages.success(requeset, 'a code sent you', 'success')
            return redirect('accounts:verify_code')
        
        return render(requeset, self.template_name, {'form': form})

    

class UserRegistrationVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify.html'

    def get(self, request):
        # user_session = request.session['user_registration_info']
        # print(user_session)
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        user_session = request.session['user_registration_info']

        # try:
        #     code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        # except OtpCode.DoesNotExist:
        #     messages.error(request, 'something went wrong, please register again', 'error')
        #     return redirect('accounts:user_register')
        
        code_instances = OtpCode.objects.filter(phone_number=user_session['phone_number'])

        
        form = self.form_class(request.POST)

        if form.is_valid():

            cd = form.cleaned_data
            for code_instance in code_instances:
                if cd['code'] == code_instance.code:
                    if not check_code_expire(code_instance.created, minutes=2, error_callback=lambda : messages.error(request, 'code has been expired', 'warning')):
                        return redirect('accounts:verify_code')
                
                    User.objects.create_user(
                        phone_number=user_session['phone_number'],
                        email=user_session['email'],
                        full_name=user_session['full_name'],
                        password=user_session['password']
                    )
                    code_instances.delete()

                    messages.success(request, 'user registered', 'info')
                    return redirect('home:home')
            
                else:
                    messages.error(request, 'code not match', 'danger')
                    return redirect('accounts:verify_code')
                
        return redirect('home:home')
    


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    

    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in', 'info')
                return redirect('home:home')
            
            messages.error(request, 'phone number or password is wrong', 'warning')
        return render(request, self.template_name, {'form':form})









class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out', 'success')
        return redirect('home:home')
    


        

