from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.messages import constants

from users.models.user_model import ProfileUser
from users.forms.form_user import UserForm, SignUpForm, ProfileUserForm


class SignUpView(LoginRequiredMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    redirect_field_name = 'login'
    template_name = 'register-user.html'

    def form_valid(self, form):
        fornecedor_cliente = self.request.POST.get('fornecedor_cliente')

        url = super(SignUpView, self).form_valid(form)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        print('Senha:',password)
        # logando = authenticate(self.request, username=username, password=password)
        # login(self.request, logando)
        messages.add_message(self.request, constants.SUCCESS, f'Usuário cadastrado  com sucesso!')
        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Cadastre-se'
        context['botao'] = 'Cadastrar'
        return context


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'edit-profile.html'
    redirect_field_name = 'login'
    
    def get(self, request):
        user = request.user
        profile = user.profileuser
        user_form = UserForm(instance=user)
        profile_form = ProfileUserForm(instance=profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        profile = user.profileuser
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileUserForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, constants.SUCCESS, 'Perfil editado com sucesso!')
            return redirect(reverse_lazy('profile'))
        context = {
            'user_form':user_form,
            'profile_form':profile_form,
        }
        return self.render_to_response(context)