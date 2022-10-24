from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.messages import constants
from apps.sales_products.views.sales import sell_produc

from sales_products.models.balance import Balance
from sales_products.models.sales import SellProduct
from datetime import datetime, timedelta
from django.utils.timezone import utc



class HomeView(TemplateView):
    template_name = 'index.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

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
            week_amount += x.amount

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
            'sell_products': sell_month[:5]
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
    next_page = 'products'