from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy


from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UpdateUserForm, UpdateProfileForm


# Create your views here.

from .forms import RegisterForm, LoginForm

def home(request):
    template = loader.get_template('users/home.html')
    return HttpResponse(template.render(request=request))



class RegisterView(View):
    form_class = RegisterForm
    initial = {'key' : 'value'}
    template_name = 'users/register.html'
    template = loader.get_template(template_name)
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {
            'form' : form,
        }

        return HttpResponse(self.template.render(context, request))
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} created successfuly!')

            return redirect(to='login')
        
        return HttpResponse(self.template.render({'form' : form}, request))
    
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register 
        if request.user.is_authenticated:
            return redirect(to='/')


        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect(to='users-profile')
    
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    template = loader.get_template('users/profile.html')
    context = {'user_form': user_form, 'profile_form': profile_form,}
    return HttpResponse(template.render(request=request, context=context))


