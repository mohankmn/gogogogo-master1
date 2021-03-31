from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.aggregates import Avg, StdDev,Sum,Variance
from django.db.models.expressions import F
from django.views.generic import TemplateView, View 
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from numpy.core.fromnumeric import product
from .models import Product, Purchase
from .utils import *
from .forms import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Create your views here.

@login_required(login_url='login')
def chart_select_view(request):
    error_message = None
    df = None
    graph = None
    Quantity = None

    product_df  = pd.DataFrame(Product.objects.all().values().filter(user=request.user))
    purchase_df = pd.DataFrame(Purchase.objects.all().values().filter(user=request.user))
    
    items = Product.objects.all().filter(user=request.user)

    if product_df.shape[0]>0 :
        product_df['product_id'] = product_df['id']
    
    if purchase_df.shape[0]>0 :
        df = pd.merge(purchase_df, product_df, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x':'id', 'date_x':'date'}, axis=1)
        if request.method == 'POST':
            chart_type = request.POST.get('plot')
            date_from  = request.POST.get('date_from') 
            date_to    = request.POST.get('date_to') 
            item       = request.POST.get('item')
            
            df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df2        = df.groupby(['date','name'], as_index=False)['quantity'].agg('sum')
            df2        = df2[df2["name"].isin([item])]
            Quantity = df2['quantity']   
            
            if chart_type!="":
                if item!="":
                    if date_from!="" and date_to!="":
                        df  = df[(df['date']>date_from)&(df['date']<date_to)]
                        df2 = df.groupby(['date','name'], as_index=False)['quantity'].agg('sum')
                        df2 = df2[df2["name"].isin([item])]
                    # function to get a graph
                    graph = get_simple_plot(chart_type, x=df2['date'], y=df2['quantity'] ,data=df)
                else:
                    error_message = 'please enter an item to continue'
            else:
                error_message = 'please select a chart to continue'

    else:
        error_message = 'no records in database'
        
    context ={
        'error_message': error_message,
        'graph' : graph,
        'Quantity' : Quantity,
        'items' : items,
        #'products' : product_df.to_html(),
        #'purchase' : purchase_df.to_html(),
    }
    return render(request, 'products/main.html', context)

@login_required(login_url='login')
def add_purchase_view(request):
        form=PurchaseForm(request.user)
        if request.method == 'POST':
            form=PurchaseForm(request.user,request.POST) 
            if form.is_valid():
                n = form.cleaned_data["product"]
                l = form.cleaned_data["quantity"]
                c = form.cleaned_data["price"]
                o = form.cleaned_data["recieved"] 
                d = form.cleaned_data["date"]

                reporter = request.user.items.get(name=n, user=request.user)
                reporter.total_inventory = F('total_inventory')-l+o
                reporter.save()
                t = Purchase(product=n,quantity=l,price=c,recieved=o,date=d)
                t.save()
                request.user.demand.add(t)
                
                return redirect('products:add-purchase-view')
                    
        return render(request,'products/add.html',context={'form':PurchaseForm(request.user) })

@login_required(login_url='login')
def items_list(request):
    ite   = None
    total = None

    try:
        ite = request.user.items.all()
        #ite = Product.objects.all()
    except ObjectDoesNotExist:
        messages.info(request,"There are no items.....")
    form = ItemSearchForm(request.POST or None)

    if request.method == 'POST':
            try:
                ite = request.user.items.filter(name__icontains=form['name'].value())
            except ObjectDoesNotExist:
                messages.info(request,"There are no items.....")
    
    context = {
        "form": form,
        "items":ite,
        "total":total
    }
    return render(request,'products/items_list.html',context)

@login_required(login_url='login')
def demand_list(request,*args,**kwargs):
    itee=None
    
    try:
        itee=request.user.demand.all()
        paginator = Paginator(itee, 30) # 3 posts in each page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
    except ObjectDoesNotExist:
        messages.info(request,"No purchases has been recorded.....")

    return render(request,'products/demand_list.html',context={'page': page, 'posts': posts})

@login_required(login_url='login')
def ItemCreate(request):
        form = ItemsForm()
        if request.method == 'POST':
            form=ItemsForm(request.POST) 
            if form.is_valid():
                n = form.cleaned_data["name"]
                l = form.cleaned_data["lead_time"]
                c = form.cleaned_data["carrying_cost"]
                o = form.cleaned_data["ordering_cost"]
                t = form.cleaned_data["total_inventory"]
                u = form.cleaned_data["unit_costprice"]
                s = form.cleaned_data["service_level"]
                w = form.cleaned_data["no_of_workingdays"]
                d = form.cleaned_data["standard_deviation"]
                a = form.cleaned_data["average_daily_demand"]

                for i in request.user.items.all():
                    if i.name==n:
                        messages.error(request, n +' Item Already Created')
                        return redirect('products:item_create_url')
              
                t = Product(name=n,lead_time=l,average_daily_demand=a,carrying_cost=c,ordering_cost=o,total_inventory=t,unit_costprice=u,service_level=s,no_of_workingdays=w,standard_deviation=d)
                t.save()
                request.user.items.add(t) 
                messages.success(request, n +' Item Created')
                return redirect('products:items_list_url')
                    
        return render(request,'products/item_create.html',context={'form':form, 'product_message':None })

@login_required(login_url='login')
def delete_items(request,pk):
    query_set = Product.objects.get(id=pk)
    
    if request.method =='POST':
        query_set.delete()
        messages.success(request,query_set.name + ' Removed')
        return redirect('products:items_list_url')
     
    context={
        'item':query_set.name
        }
    return render(request,'products/delete_items.html',context)

@login_required(login_url='login')
def update_items(request,pk):
    query_set = Product.objects.get(id=pk)
    form      = ItemsForm(instance=query_set)
    n         = query_set.name
    
    if request.method=='POST':
        form = ItemsForm(request.POST,instance=query_set)
        if form.is_valid():
            form.save()
            messages.info(request, n + '  Updated to ' + query_set.name)
            return redirect('products:items_list_url')
    
    context={
        'form':form
    }
    return render(request,'products/update_item.html',context)

@login_required(login_url='login')
def calculations(request):
    item_df   = pd.DataFrame(Product.objects.all().values().filter(user=request.user))
    demand_df = pd.DataFrame(Purchase.objects.all().values().filter(user=request.user))
    error = None
    
    if demand_df.shape[0]>0:
        item_df.rename(columns = {'id':'product_id'}, inplace = True)
        df = pd.merge(item_df,demand_df,on='product_id')
        df['date_y'] = pd.to_datetime(df['date_y'], format='%y-%m-%d')
        df = df.groupby(['date_y','name'], as_index=False).aggregate({'quantity':'sum', 'total_price':'sum'})
        
        df.rename(columns = {'name':'Item Name'}, inplace = True)
        df['Year/Month'] = df['date_y'].dt.strftime('%Y/%m')
        df = df.groupby(['Year/Month','Item Name']).aggregate({'quantity':['mean','std','count','sum']}) # groupby each 1 month
        
        df['Daily Average']=df['quantity']['sum']/30 
        a = df['quantity']['count']/30
        b = df['quantity']['std']*df['quantity']['std'] + df['quantity']['mean']*df['quantity']['mean']
        c = df['Daily Average']*df['Daily Average']
        d = a*b-c
        df['Standard deviation'] = d.transform(lambda x:x**0.5)
        df['Total demand'] = df['quantity']['sum']
        df['Frequency']    = df['quantity']['count']

        del df['quantity']
        df.columns = df.columns.droplevel(1)

        return render(request,'products/calculations.html',context={'df2':df.to_html(classes=('table table-striped')), 'error':error})

    else:
        error='<h3>No Data to Analyze</h3>' 
        df2 = None
        return render(request,'products/calculations.html',context={'df2':df2, 'error':error})


'''@login_required(login_url='login')
def sales_dist_view(request):
    graph = None
    error = None
    try:
        df = pd.DataFrame(Purchase.objects.filter(user=request.user).values())
        #df['user_id']=df['user_id'].apply(get_salesman_from_id)
        df.rename({'user_id':'user'}, axis=1, inplace=True)
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        
        plt.switch_backend('Agg')
        plt.xticks(rotation=90)
        sns.barplot(x='date', y='total_price', hue='user', data=df)
        plt.tight_layout
        graph = get_image()
    
    except:
        error = 'No data........'
    
    context ={
        'graph':graph,
        'error':error
    }
    return render(request, 'products/sales.html', context)'''    