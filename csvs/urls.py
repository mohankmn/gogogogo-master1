from django.urls import path
from .views import upload_file_view, upload_product_file_view

app_name = 'csvs'

urlpatterns = [
    path('purchase/', upload_file_view, name='upload_view_url'),
    path('product/', upload_product_file_view, name='upload_view_product_url'),
]