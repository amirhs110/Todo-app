from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm

# Create your views here.


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    fields = "username", "password"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("task:dashboard")


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("task:dashboard")
    success_message = "Registration successful. You are now logged in."

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response
