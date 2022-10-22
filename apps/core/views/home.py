from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.messages import constants


class HomeView(TemplateView):
    template_name = 'index.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
    def get(self, request):
        #carrinho = Carrinho.objects.all()
        #produtos = ProdutoModel.objects.all()
        context = {
            'produtos': 'produtos',
            'carrinho':'carrinho'
        }
        return render(request, self.template_name, context)


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('produtos')
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            messages.error(self.request, f"""O usuário 
                        {self.request.user.first_name} 
                        {self.request.user.last_name}
                        já está logado """)
            return redirect(reverse_lazy("produtos"))
        else:
            login(self.request, form.get_user())
            messages.success(self.request, f"""Seja bem vindo(a) 
                            {self.request.user.first_name} 
                            {self.request.user.last_name}
                            """)
            return redirect(reverse_lazy("products"))


class LogoutView(auth_views.LogoutView):
    next_page = 'produtos'