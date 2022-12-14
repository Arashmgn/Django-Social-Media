from pyexpat.errors import messages
from urllib import request
from django.contrib.auth import authenticate , login

from .models import User
from core.models import *
from core.models import Post
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404,render
from django.urls import reverse_lazy
from django.views.generic import CreateView , DetailView ,UpdateView,ListView
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as SigninView
from .forms import UserRegisterForm, UserLoginForm, UserSettingsForm, MyPasswordChangeForm


class SignUpView(CreateView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('core.home')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        
        return super().dispatch(request, *args, **kwargs)
        
    
    
    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return


class LoginView(SigninView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('core:home')
    form_class = UserLoginForm
    success_message = "successfully logged in"
    

class ProfileView(LoginRequiredMixin,ListView):
    model = User
    template_name: str = 'account/profile.html'
    context_object_name = 'userprofile'
    
    def get_user_profile(self, username):
        # print(username)
        return get_object_or_404(User, username=username)
    
    
    def get_queryset(self):
        print(self.kwargs.get('username'))
        context_data = {}
        username=self.kwargs.get('username')
        user = self.get_user_profile(username=username)
        context_data['user'] = user
        context_data['posts'] = Post.objects.filter(user=user)
        follow_relation = Follow.objects.filter(user=user,follower=self.request.user).first()
        if(follow_relation is None):
            context_data['unfollow'] = False
        else:
            context_data['unfollow'] = True
            
        return context_data

    
  
class SettingsView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = 'account/settings.html'
    success_url = reverse_lazy('settings')
    fields = ['username', 'email', 'first_name',
              'last_name', 'bio', ]
    form = UserSettingsForm
    
    def get_object(self):
            return self.request.user


@login_required
def PasswordChangeView(request):
    if request.method == 'POST':
        password_form = MyPasswordChangeForm(request.user,request.POST)
        if password_form.is_valid():
            user=password_form.save()
            update_session_auth_hash(request, user)
            # messages.success(request,'Your password wa successfully updated')
            return redirect('settings')
        else:
            pass
            # messages.error(request,'Please correct  the error below.')
    else:
        password_form = MyPasswordChangeForm(request.user)
        
    return render(request, 'account/password.html', {
        'form':password_form
    })


@login_required        
def LogoutView(request):
    logout(request)
    return redirect('login')