from django.shortcuts import render, redirect
from django.views import View
from . forms import UserRegistrationForm
from .models import OtpCode
from django.contrib import messages
import random
from utils import send_otp_code

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
            random_code = random.randint(10000, 99999)
            send_otp_code(
                phone_number=cd['phone_number'],
                code=random_code
            )

            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)

            # session is save in server and a hash of that is on client sys
            requeset.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'emial': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password']
            }

            messages.success(requeset, 'a code sent you', 'success')
            return redirect('accounts:verify_code')
        
        return redirect('home:home')
    

class UserRegistrationVerifyCodeView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass