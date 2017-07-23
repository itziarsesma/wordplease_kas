from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from login.forms import LoginForm, SignupForm


class LoginView(View):
    def get(self, request):
        """
        Presenta el formulario de login a un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """
        context = {
            'form': LoginForm()
        }
        return render(request, 'login/login.html', context)

    def post(self, request):
        """
        Hace login de un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """
        form = LoginForm(request.POST)
        context = dict()
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                url = request.GET.get('next', 'posts_list')
                return redirect(url)
            else:
                context["error"] = "Wrong username or password"
        context["form"] = form
        return render(request, 'login/login.html', context)


def logout(request):
    """
    Hace logout de un usuario
    :param request: HttpRequest
    :return: HttpResponse
    """
    django_logout(request)
    return redirect('login')

class SignupView(View):
    def get(self, request):
        """
        Presenta el formulario de registro de un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """
        context = {
            'form': SignupForm()
        }
        return render(request, 'login/signup.html', context)

    def post(self, request):
        """
        Hace login de un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data.get("username"))
                message = 'Ya existe el usuario ' + form.cleaned_data.get("username")
            except User.DoesNotExist:
                new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
                new_user.first_name = form.cleaned_data['first_name']
                new_user.last_name = form.cleaned_data['last_name']
                new_user.save()

                message = 'Se ha creado correctamente el usuario'
                form = SignupForm()

            except User.MultipleObjectsReturned:
                message = 'Ya existe el usuario ' + form.cleaned_data.get("username")
        else:
            message = 'Introduce los datos correctamente'

        context = {
            'form': form,
            'message': message
        }
        return render(request, 'login/signup.html', context)