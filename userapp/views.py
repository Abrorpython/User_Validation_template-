from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout     #Avtorizatsiyadan o'tish uchun 3 ta funkisya
# from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm, LoginForm, ProfileForm
from MarsPro.mixins import LoginRequiredMixin

def index(request):
    return render(request, 'layout.html')

class RegistrationsView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        request.title = "Ro'yxatdan o'tish"

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         messages.warning(request, "Siz tizimga kirgansiz !")
    #         return redirect('user:index')
    #     return super(RegistrationsView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'main/registrations.html', {
            'form': RegistrationForm()
        })

    def post(self, request):

        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz")
            return redirect('user:index')

        return render(request, 'main/registrations.html', {
            'form': form
        })


class LoginView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        request.title = "Tizimga kirish"

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         messages.warning(request, "Siz tizimga kirgansiz !")
    #         return redirect('user:index')
    #     return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'main/login.html', {
            "form": LoginForm()
        })

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'],)
            if user is not None:
                login(request, user)

                messages.success(request, f"{user.get_short_name()} xush kelibsiz!!!")

                return redirect('user:index')
            form.add_error('password', "Login yoki Parol hato")

        return render(request, 'main/login.html', {
            'form': form
        })

class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, "Kelib turing !!!")

        return redirect('user:index')


class ProfileView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        request.title = "Profilni o'zgartirish"

    def get(self, request):
        return render(request, 'main/profile.html', {
            'form': ProfileForm(instance=request.user)
        })

    def post(self, request):
        form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Muvaffaqiyatli saqlandi")
            return redirect('user:profile')
        return render(request, 'main/profile.html', {
            'form': form
        })
