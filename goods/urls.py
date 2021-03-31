from django.urls import path
from .views import *

app_name = 'goods'

urlpatterns = [
    path('', goods_form_view, name='goods_form_url'),
    path('amount/', amount_form_view, name='amount_form_url'),
    path('delete_items/', delete_goods, name="delete_goods_url"),
] 