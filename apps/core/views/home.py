from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.messages import constants

from sales_products.models.sales import SellProduct
from datetime import datetime, timedelta
from django.utils.timezone import utc


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    redirect_field_name = 'login'

    def get(self, request):
        sell_month = SellProduct.objects.all()

        all_amount = 0
        day_amount = 0
        week_amount = 0
        month_amount = 0
        quantity = 0

        hoje = datetime.utcnow().replace(tzinfo=utc)
        semana = datetime.utcnow().replace(tzinfo=utc) - timedelta(days=7)
        
        day = SellProduct.objects.filter(date_sale__range = [semana, hoje])

        # Filtrar por dia e semana
        for x in day:
            if x.amount:
                week_amount += x.amount
            else:
                week_amount = 0

            if x.date_sale.day == hoje.day :
                day_amount += x.amount
        
        # Filtrar por todas as vendas e mês
        for sell_product in sell_month:
            all_amount += sell_product.amount
            quantity += sell_product.quantity

            if sell_product.date_sale.month > 0 and sell_product.date_sale.month < 31:
                month_amount += sell_product.amount

        context = {
            'day': day_amount,
            'month': month_amount,
            'week': week_amount,
            'amount_all': all_amount,
            'quantity': quantity,
            'sell_products': sell_month[:10]
        }
        return render(request, self.template_name, context)


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('produtos')
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            messages.error(self.request, f"""O usuário 
                        {self.request.user.username} 
                        já está logado """)
            return redirect(reverse_lazy("home"))
        else:
            login(self.request, form.get_user())
            messages.success(self.request, f"""Seja bem vindo(a) 
                            {self.request.user.username} 
                            """)
            return redirect(reverse_lazy("home"))


class LogoutView(auth_views.LogoutView):
    success_url = reverse_lazy('login')