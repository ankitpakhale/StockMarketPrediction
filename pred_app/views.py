from django.shortcuts import render, redirect
from pred_app.lstm_prediction import *

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserDetails
from .forms import UserForm
import math
import random
import pandas as pd
import numpy as np
from datetime import date 
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error 
import preprocessing
from sklearn.linear_model import LinearRegression

# visualization
import matplotlib.pyplot as plt 
from pylab import *

import nsepy as nse 
from nsetools import Nse

import numpy as np
from Demo1.settings import BASE_DIR
import os
import datetime
from .models import NseData
from plotly.offline import plot
from .forms import UserForm
from plotly.graph_objs import Scatter

def regview(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            password= form.data.get("password")
            re_password = form.data.get("re_password")
            if(password == re_password) :
                new_form.save()
                return redirect('login')
            else : 
                return render(request,'html/registration.html',{'error': "PASSWORDS ARE DIFFERENT! TRY AGAIN" })
        else: 
            return render(request,'html/registration.html',{'error': "INVALID FORM" })
    return render(request,'html/registration.html')


def loginview(request):
    if request.POST:
        try:
            model = UserDetails.objects.get(user_email = request.POST['user_email'])
            print("1")
            if model.password == request.POST['password']:
                print("2")
                request.session['name'] = model.user_name
                return redirect('dashboard')
            else:
                return render(request,'html/login.html',{'error': "INCORRECT DETAILS" })
        except:
            return render(request,'html/login.html',{'error': "INCORRECT DETAILS" })
    return render(request,'html/login.html')

def Index_Data(request):
    nsel = Nse()
    stock_list = nsel.get_stock_codes()
    del stock_list["SYMBOL"]
    print(stock_list)
    # stock_list= {v: k for k, v in stock_list.items()}
    # print(stock_list)
    endata = datetime.datetime.today().date()
    print(endata)
    if request.POST:
        print("1")
        nm = request.POST['cnm']
        sd = request.POST['sdate']
        ed = request.POST['edate']
        print(nm,sd,ed)
        # print(date(sd),date(ed))
        # print(type(date(sd)),type(date(ed)))

        date_time_str = sd
        sd = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        sd = sd.date()
        
        date_time_str = ed
        ed = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        ed = ed.date()
        
        obj_data = NseData()
        obj_data.nse_comp = nm
        obj_data.s_d = sd
        obj_data.e_d = ed
        number_of_company = 1
        company_list = [str(nm)]
        numbered = list(company_list)
        stock_data = list(company_list)
        for i in range(number_of_company):
            stock_data[i] = nse.get_history(symbol=company_list[i], start=sd, end=ed)

        for each_stock in stock_data:
            each_stock.drop(['Trades','Volume','%Deliverble','VWAP','Turnover','Last','Prev Close','Series','Symbol'], axis =1,inplace =True)
            
        for each_stock in stock_data:
            each_stock['Change'] = each_stock['Close']-each_stock['Open']   
            
        for each_stock in stock_data:
            each_stock.loc[each_stock.Change >0, 'Gains'] = 1 
            each_stock.loc[each_stock.Change <0, 'Gains'] = -1 
            each_stock.loc[each_stock.Change ==0, 'Gains'] = 0 
        
        for each_stock,number in zip(stock_data,numbered):
            each_stock.plot(y ='Open',color=(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)),figsize=(15,5),title='Open of ' +number+ '  over the years')
            plt.savefig(os.path.join(BASE_DIR,"media/Open"+str(nm)+".png"))
            obj_data.open_img = "Open"+str(nm)+".png"
            
            each_stock.plot(y='Change',color=(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)),figsize=(15,5),title ='Changes in '+ number+'  over the years')
            plt.savefig(os.path.join(BASE_DIR,"media/Change"+str(nm)+".png"))
            obj_data.Change_img = "Change"+str(nm)+".png"
        
        for each_stock,number in zip(stock_data,numbered):
            np.random.seed(7)
            obs = np.arange(1, len(each_stock) + 1, 1)
            OHLC_avg = each_stock.mean(axis = 1)
            HLC_avg = each_stock[['High', 'Low', 'Close']].mean(axis = 1)
            close_val= each_stock[['Close']]
            plt.plot(obs, HLC_avg, color=(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)), label = 'HLC avg')
            plt.plot(obs, close_val, 'g', label = 'Closing price')
            plt.legend(loc = 'upper right')
            plt.xlabel('Number of days')
            print('\n\n\n')
            plt.savefig(os.path.join(BASE_DIR,"media/Data"+str(nm)+".png"))
            obj_data.Data_img = "Data"+str(nm)+".png"
        
        obj_data.save()
        df = stock_data[0].reset_index()
        tables_data = stock_data[0].to_html(classes='mystyle')
        
        # latestData = NseData.objects.order_by('id')[0]
        latestData = NseData.objects.last()
        date, stock = [], []
        df['year'] = pd.DatetimeIndex(df['Date']).year

        df = df.groupby(df['year'])['Change'].agg(['mean']).reset_index()
        date, stock = list(df.year), list(df["mean"])
        print(date)
        if (len(stock) == 0):
            no_date = True
        else:
            no_date = False

        plot_div, data = None, None
        if not no_date:
            data = [[date[i], stock[i]]for i in range(len(stock))]
            model = LinearRegression()
            model.fit(np.array(date).reshape(-1, 1), np.array(stock).reshape(-1, 1))
            year = np.array([[2022],[2023],[2024]]).reshape(-1, 1)
            predicted = model.predict(np.array(year).reshape(-1, 1))
            
            for i in range(3):
                data.append([year[i][0], int(predicted[i][0])])
                date.append(year[i][0])
                stock.append(int(predicted[i][0]))
            plot_div = plot([Scatter(x=date, y=stock,
                                     mode='lines', name='test',
                                     opacity=0.8, marker_color='green')],
                            output_type='div')
            print(date[1])
        return render(request,'Home.html',{'table':tables_data,'data':latestData,'year':year ,'no_data': no_date, 'plot_div': plot_div, 'data1': data})
    return render(request,'Home.html',{'endata':endata,'stock_list':stock_list})


def DashBoard(request):
    data = NseData.objects.all()
    return render(request,'Dashboard.html',{'data':data})

def Show_Data(request,id):
    data = NseData.objects.get(id=id)
    number_of_company = 1
    company_list = [str(data.nse_comp)]
    numbered = list(company_list)
    print(numbered)
    stock_data = list(company_list)
    print(stock_data)

    for i in range(number_of_company):
        stock_data[i] = nse.get_history(symbol=company_list[i], start=data.s_d, end=data.e_d)
        print(stock_data)
   
    for each_stock in stock_data:
        each_stock.drop(['Trades','Volume','%Deliverble','VWAP','Turnover','Last','Prev Close','Series','Symbol'], axis =1,inplace =True)
    print("8", stock_data)    
    for each_stock in stock_data:
        each_stock['Change'] = each_stock['Close']-each_stock['Open']   
    print("9")    
    for each_stock in stock_data:
        each_stock.loc[each_stock.Change >0, 'Gains'] = 1 
        each_stock.loc[each_stock.Change <0, 'Gains'] = -1 
        each_stock.loc[each_stock.Change ==0, 'Gains'] = 0 
    print("10")
    # print(numbered[0])
    # print(stock_data[0])
    tables_data = stock_data[0].to_html(classes='mystyle')
    
    return render(request,'DataSet.html',{'table':tables_data,'data':data})


def redirect_root(request):
    return redirect('/pred_app/index')

def index(request):
	return render(request, 'pred_app/index.html') 

def pred(request):
    return render(request, 'pred_app/prediction.html')

def contact(request):
	return render(request, 'pred_app/contact.html')

def search(request, se, stock_symbol):
	import json
	predicted_result_df = lstm_prediction(se, stock_symbol)
	return render(request, 'pred_app/search.html', {"predicted_result_df": predicted_result_df})
