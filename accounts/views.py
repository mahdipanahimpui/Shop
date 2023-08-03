from django.shortcuts import render
from django.views import View
from . forms import UserRegistrationForm

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    

    def post(self, requeset):
        pass