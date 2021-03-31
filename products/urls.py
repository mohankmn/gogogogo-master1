from django.urls import path
from .views import * 

app_name = 'products'

urlpatterns = [
    path('', chart_select_view, name='main-products-view'),
    path('add/',add_purchase_view, name='add-purchase-view'),
    #path('sales/',sales_dist_view, name='sales-view'),    
    path('items/',items_list,name='items_list_url'),
    path('demand/',demand_list,name='demand_list_url'),
    path('calculations/',calculations,name='calculations_url'),
    #path('demand/create/',DemandCreate,name='demand_create_url'),
    path('item/create/',ItemCreate,name='item_create_url'),
    path('delete_items/<str:pk>/', delete_items, name="delete_items"),
    path('update_item/<str:pk>/',update_items,name="update_item"),  
]



