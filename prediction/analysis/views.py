# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.views.decorators.csrf import *
from django.shortcuts import render,render_to_response

from django.template import RequestContext
from django.http import HttpResponseNotFound , HttpResponseRedirect
import json
from django.views.decorators.csrf import *
from django.http import HttpResponse
import json
from subprocess import Popen, PIPE
import time 
import csv
# Create your views here.
import os, sys
from copy import deepcopy
import numpy
import pandas
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from pandas.tseries.holiday import Holiday, HolidayCalendarFactory, FR, DateOffset

from multiprocessing import Process, Lock

from operator import itemgetter

import numpy
import pandas

import graphviz

from sklearn.feature_extraction import DictVectorizer

from sklearn import preprocessing

from sklearn.decomposition import PCA

from sklearn.grid_search import RandomizedSearchCV, GridSearchCV
from sklearn import cross_validation


from xgboost.sklearn import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree

testingModels = False
from datetime import datetime as dt
import codecs

import itertools
import md5
import base64
import hashlib
import bencode
import csv

from training_data import training_data
from request import *
import sys
import os 
import pandas as pd
import pymongo
import json
import sklearn.metrics
from labels_map import LabelMapping



@csrf_exempt
def btprojectresponse(request):

    response = {}
    from request import *

    key = hashlib.md5(bencode.bencode(param[index]['dimension'].encode('utf-8')+param[index]['from_date'].encode('utf-8')+param[index]['to_date'].encode('utf-8')+''.join(param[index]['metric']).encode('utf-8')+param[index]['sql'].encode('utf-8')+param[index]['user'].encode('utf-8'))).hexdigest()
    print key 
    mng_client = pymongo.MongoClient().bulk_example
    mng_db = mng_client['prediction'] 
    collection_name = 'result' 
    db_cm = mng_db[collection_name]

    print db_cm.find()
    
    obj =  [obj for obj in db_cm.find() if (obj['column_id'] == key)]
    print obj
         
    if obj :
        
           
        print obj[0]['final_result'] 

        return HttpResponse(response, content_type='application/json')   


    else:
        import csv

        with open('user.csv') as f:
            reader = csv.DictReader(f)
            rows_0 = list(reader)
            
            for row in rows_0:
                
                if param[index]['user'] == 'comcast' or 'bt'or'safetrak' :
                    print "hello"
                    sql = param[index]['sql']
                    
                    results1 = training_data(row['Db_connection'],row['username'],row['password'],row['database'],sql)
                    print results1
                    response['status'] = "success"
                    response['message'] = "Data successfully predicted"
           
            list_row = []
            results = {'column_id':key,'training_data':results1}


        collection_name = 'input'
        
        db_cm = import_content(results,key,collection_name) 
        
        
        for obj in db_cm.find():            
            if obj['column_id'] == key: 
                import csv                  
                keys = obj['training_data'][0].keys()
                with open(key + 'unpickle_train.csv', 'wb') as output_file:
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                    try:                    
                        dict_writer.writerows(obj['training_data'])

                    except:
                        pass


        



        from datetime import date, timedelta,datetime
        
        value1=datetime.strptime(param[index]['from_date'], '%Y-%m-%d').strftime('%Y,%m,%d')
        value2= datetime.strptime(param[index]['to_date'], '%Y-%m-%d').strftime('%Y,%m,%d')
        
        import dateparser
        d1 = dateparser.parse(value1)
        
        d2 = dt = dateparser.parse(value2)
        
        delta = d2 - d1 
        
        date_list =[]
        for i in range(delta.days+1):
            value = (d1+timedelta(days=i))
            date_list.append(value.date())
        
        prob_sum_date_list_0 =[]
        prob_sum_date_list_1 = []
        prob_count =[]
        import csv
        header_row = ",".join(['column_id','date_col'])
        
        column_id = next(itertools.count())
        content_to_write = "%s" % (header_row)
        file_to_write = open("input_con.csv",'w')
        file_to_write.write(content_to_write)
        
        file_to_write.close()
        for indx in range(0,len(date_list)):          
            
            with open('input_con.csv','a') as f:            
                f.write("\n%s,%s"%(column_id,date_list[indx]))
            input_con = 'input_con.csv'    
               
        count  = do_predction_country(key + 'unpickle_train.csv',input_con,key)
        
        response['status'] = "success"
        response['message'] = "Data successfully predicted"
       
                
        
        file_path = "output.json" 
        count = json.dump(count, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) 

        
        
        
        with open('output.json') as fr:
            response['count'] = json.load(fr)


        with open(key+'final_result.csv') as csvfile:
            import csv
            csvreader = csv.reader(csvfile)
            for row in csvreader:                        
                  # 
                response['dict'] = row 


        f = open(key+'final_result.txt','w')
        f.write(json.dumps(response))
        f.close()

        final = {'column_id':key,'final_result':json.dumps(response)}
        collection_name= 'result'
        db_cm1 = import_content(final,key,collection_name)
     
        train = pandas.read_csv(key + 'unpickle_train.csv',parse_dates=['date_col'])
        categories=sorted(train[param[index]['dimension']].unique())
        import os
        files = [x +'prediction1.csv' for x in categories if os.path.isfile(x+'prediction1.csv') ]
        files1 = [x +'out.csv' for x in categories if os.path.isfile(x+'out.csv') ]
        
        # for dex in range (0,len(files)):
        #     try:
        #         os.remove(files[dex].encode('utf-8'))
        #     except:
        #         pass
        
        for d in range (0,len(files1)):
            try:
                os.remove(files1[d].encode('utf-8'))
            except:
                pass





    return HttpResponse(json.dumps(response), content_type='application/json') 









def import_content(results,key,collection_name):
    mng_client = pymongo.MongoClient().bulk_example
    mng_db = mng_client['prediction'] 
    
    db_cm = mng_db[collection_name]
    
    data = results

    if collection_name == 'input':
        data_date = results['training_data']
        from decimal import Decimal  
        
        import datetime
        for d in data_date:
            d['date_col'] = d['date_col'].isoformat()
        for d in data_date :
            for  dex in range(0,len(param[index]['metric'])):
                import decimal
                if isinstance(d[param[index]['metric'][dex]], decimal.Decimal ) :  
                    print  d[param[index]['metric'][dex]]   
                    d[param[index]['metric'][dex]]  = float(d[param[index]['metric'][dex]])


    else:
        pass
            
    data_json = json.loads(json.dumps(results))
    
    
   
    db_cm.update_one(data_json, {'$set': data_json}, upsert = True)
    print "kirti"
    return db_cm





def do_predction_country(unpickle_train,input_con,key):
    import csv
    import pandas as pd 
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')    
    train = pandas.read_csv(key +'unpickle_train.csv', parse_dates=['date_col'],date_parser=dateparse)
    test = pandas.read_csv(input_con, parse_dates=['date_col'])


    
    counts = test.groupby(['date_col']).size()

    numMult = counts.value_counts()

    
    
    counts = pandas.DataFrame(counts)
    counts = counts.reset_index()
    test = test.merge(counts, how='right')
    test.rename(columns={0:'NumMultIncidents'}, inplace=True)
    maxIncidentsTest = max(counts)
    
    counts = train.groupby(['date_col', param[index]['dimension']]).size()
    
    maxIncidentsTrain = max(counts)
    counts = pandas.DataFrame(counts)
    counts = counts.reset_index()
    train = train.merge(counts, how='right')
    train.rename(columns={0:'NumMultIncidents'}, inplace=True)
    maxIncidents = max(0, maxIncidentsTrain)
    del counts 
    train = pandas.read_csv(key + 'unpickle_train.csv',parse_dates=['date_col'])
    categories=sorted(train[param[index]['dimension']].unique())
    print categories
    import sys  

    reload(sys)  
    sys.setdefaultencoding('utf8')
    import re 
    from pandas import Series
    test = Series.from_csv(input_con, header=0)
    test_val = [x for x in test]
    import os.path 



    files = [x +'prediction1.csv' for x in categories if os.path.isfile(x+'prediction1.csv') ]
    
    import os
    for dex in range (0,len(files)):

        os.remove(files[dex].encode('utf-8'))
    





    final_result = []    
    for ind in range(0,len(categories)):       
        
        df = (train.loc[train[param[index]['dimension']] == categories[ind]])      
        df.to_csv(key + 'col_unpickle_train.csv', encoding='utf-8', index=False)
        import csv
        from pandas import Series
        from matplotlib import pyplot
        from statsmodels.tsa.arima_model import ARIMA
        f  = open(key + 'col_unpickle_train.csv','r')
        reader = csv.reader(f)
        thing = param[index]['dimension']
        i = next(reader)
        indux = i.index(param[index]['dimension'])
        try:
            with open(categories[ind].encode('utf-8')+'out.csv', 'wb') as fl: 
                writer = csv.writer(fl)                    
                for row in reader :
                    a = range(0,len(i))  
                    a = [x for x in a if x != indux]                      
                    writer.writerow([row[x] for x  in a])
        except:
            pass





        # try:
        from pandas import Series
        from matplotlib import pyplot

        from statsmodels.tsa.arima_model import ARIMA
        from sklearn.metrics import mean_squared_error
        from math import sqrt
        

        def predict(coef, history):
            yhat = 0.0
            for i in range(1, len(coef)+1):
                yhat += coef[i-1] * history[-i]
            return yhat

        
        
        series = Series.from_csv(categories[ind]+'out.csv')

        X = series.values
        size = len(X) - 10
        def inverse_difference(history, yhat, interval=1):
            return yhat + history[-interval] 

        if len(param[index]['metric']) == 1:
            

            import warnings
            from pandas import read_csv
            from pandas import datetime
            from statsmodels.tsa.arima_model import ARIMA
            from sklearn.metrics import mean_squared_error
             
            
            # def evaluate_arima_model(X, arima_order):
            #     df = pd.read_csv(categories[ind]+'out.csv')
            #     # print df.iloc[:,0].values
            #     from statsmodels.tsa.arima_model import ARIMA
            #     from sklearn.metrics import mean_squared_error

            #     X = df.iloc[:,0].values
            #     # print X 
            #     train_size = int(len(X) * 0.66)
            #     train, test = X[0:train_size], X[train_size:]
            #     history = [x for x in train]
                
            #     predictions = list()
            #     for t in range(len(test)):
            #         model = ARIMA(history, order=arima_order)
            #         model_fit = model.fit(start_params=None, disp=5)
            #         yhat = model_fit.forecast()[0]
            #         predictions.append(yhat)
            #         history.append(test[t])
                
            #     error = mean_squared_error(test, predictions)
            #     return error
             
            
            # def evaluate_models(dataset, p_values, d_values, q_values):
            #     dataset = dataset.astype('float32')
            #     best_score, best_cfg = float("inf"), None
            #     for p in p_values:
            #         for d in d_values:
            #             for q in q_values:
            #                 order = (p,d,q)
            #                 try:
            #                     mse = evaluate_arima_model(dataset, order)
            #                     if mse < best_score:
            #                         best_score, best_cfg = mse, order
            #                     print('ARIMA%s MSE=%.3f' % (order,mse))
            #                 except:
            #                     continue
            #     print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))
            #     return best_cfg
            
            
            # series = Series.from_csv(categories[ind]+'out.csv') 
            
            # p_values = [0, 1, 2, 4, 6, 8, 10]
            # d_values = range(0, 3)
            # q_values = range(0, 3)
            # warnings.filterwarnings("ignore")
            # best_cfg = evaluate_models(df.iloc[:,0].values, p_values, d_values, q_values)
            # df = pd.read_csv(categories[ind]+'out.csv')
            # # print df.iloc[:,0].values
            # from statsmodels.tsa.arima_model import ARIMA
            # from sklearn.metrics import mean_squared_error

            # X = df.iloc[:,0].values
            # # print X 
            # size = len(X) - 7
            # train1, test1 = X[0:size], X[size:len(X)]
            # history1 = [x for x in train1]
            # predictions = list()
            # for t in range(len(test1)):
            #     model = ARIMA(history1, order=(3,1,0))
            #     model_fit = model.fit(start_params=None, disp=5)
            #     output = model_fit.forecast()
            #     yhat = output[0]
            #     predictions.append(yhat)
            #     obs = test1[t]
            #     history1.append(obs)
            #     # print('predicted=%f, expected=%f' % (yhat, obs))
            # error = mean_squared_error(test1, predictions)
            # # print('Test MSE: %.3f' % error)
            
            df = pd.read_csv(categories[ind]+'out.csv')
            # print df.iloc[:,0].values
                
            series = Series.from_csv(categories[ind]+'out.csv') 
            
            
            from pandas import Series
            from matplotlib import pyplot
            from statsmodels.tsa.arima_model import ARIMA
            from sklearn.metrics import mean_squared_error
            from math import sqrt
            import numpy as np 
            
            test = Series.from_csv(input_con, header=0)
            history = [(x) for x in df.iloc[:,0].values]
            
            # print history
            model = ARIMA(history,order = (3,1,0))
            print 'joly'
            model_fit = model.fit()
            print "complete"
    
            
            
            forecast = model_fit.forecast(steps=31)[0]
            
            
            
            for yhat in forecast :
                print yhat
                
                inverted_1 = inverse_difference(history, yhat, interval=1)
                
                final_result1 =  ['%f,%s'.encode('utf-8') % ( inverted_1,categories[ind])]

                import csv

                with open(categories[ind]+'prediction1.csv', 'a') as myfile:
                    wr = csv.writer(myfile)
                    wr.writerow(final_result1)

        
        else:
            import warnings
            from pandas import read_csv
            from pandas import datetime
            from statsmodels.tsa.arima_model import ARIMA
            from sklearn.metrics import mean_squared_error
            df = pd.read_csv(categories[ind]+'out.csv')
            print df.iloc[:,0].values 
            X = df.iloc[:,0].values
            print X 
            def evaluate_arima_model(X, arima_order):
                df = pd.read_csv(categories[ind]+'out.csv')
                print df.iloc[:,0].values
                from statsmodels.tsa.arima_model import ARIMA
                from sklearn.metrics import mean_squared_error

                X = df.iloc[:,0].values
                print X 
                train_size = int(len(X) * 0.66)
                train, test = X[0:train_size], X[train_size:]
                history = [x for x in train]
                
                predictions = list()
                for t in range(len(test)):
                    model = ARIMA(history, order=arima_order)
                    model_fit = model.fit(start_params=None, disp=5)
                    yhat = model_fit.forecast()[0]
                    predictions.append(yhat)
                    history.append(test[t])
                
                error = mean_squared_error(test, predictions)
                return error
             
            
            def evaluate_models(dataset, p_values, d_values, q_values):
                dataset = dataset.astype('float32')
                best_score, best_cfg = float("inf"), None
                for p in p_values:
                    for d in d_values:
                        for q in q_values:
                            order = (p,d,q)
                            try:
                                mse = evaluate_arima_model(dataset, order)
                                if mse < best_score:
                                    best_score, best_cfg = mse, order
                                print('ARIMA%s MSE=%.3f' % (order,mse))
                            except:
                                continue
                print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))
                return best_cfg
            
            
            series = Series.from_csv(categories[ind]+'out.csv') 
            
            p_values = [0, 1, 2, 4, 6, 8, 10]
            d_values = range(0, 3)
            q_values = range(0, 3)
            warnings.filterwarnings("ignore")
            best_cfg = evaluate_models(df.iloc[:,0].values, p_values, d_values, q_values)

            from pandas import Series
            from matplotlib import pyplot
            from statsmodels.tsa.arima_model import ARIMA


            series = Series.from_csv(categories[ind].encode('utf-8')+'out.csv')



            from pandas import Series
            from matplotlib import pyplot

            from statsmodels.tsa.arima_model import ARIMA
            from sklearn.metrics import mean_squared_error
            from math import sqrt

            def predict(coef, history):
                yhat = 0.0
                for i in range(1, len(coef)+1):
                    yhat += coef[i-1] * history[-i]
                return yhat

            df = pd.read_csv(categories[ind]+'out.csv')
            # print df.iloc[:,0:2].values
            from statsmodels.tsa.arima_model import ARIMA
            from sklearn.metrics import mean_squared_error
            
            X = df.iloc[:,0].values
            # print X
            size = len(X) - 7
            train1, test1 = X[0:size], X[size:]
            history1 = [x for x in train1]
            predictions = list()
            for t in range(len(test1)):
                try :
                    model = ARIMA(history1, order=(3,1,0))
                    model_fit = model.fit(start_params=None, disp=5)
                except:
                    model = ARIMA(history1, order= (0,0,0))
                    model_fit = model.fit(start_params=None, disp=5)
                ar_coef = model_fit.arparams
                yhat = predict(ar_coef, history1)
                predictions.append(yhat)
                obs = test1[t]
                history1.append(obs)
                print('>predicted=%.3f, expected=%.3f' % (yhat, obs))
            rmse = sqrt(mean_squared_error(test1, predictions))
            print('Test RMSE: %.3f' % rmse)
        

            history = [float(x) for x in X]
            
            predictions = list()
            
            test = Series.from_csv(input_con, header=0)
            test_val = [x for x in test]
            print history                      
            model = ARIMA(history, order=(3,1,0))
            print "hello"
            model_fit = model.fit()
            predic = model_fit.predict(start='2018-08-09',end= '2018-08-20',dynamic=True)
            print "prediction",predic
            import statsmodels.formula.api as smf
            import statsmodels.tsa.api as smt
            import statsmodels.api as sm
            mod_seasonal = smt.SARIMAX(history, trend='c',order=(1, 1, 2), seasonal_order=(0, 1, 2, 12),simple_differencing=False)
            res_seasonal = mod_seasonal.fit()
            prediction = res_seasonal.get_prediction(start='2018-08-09', dynamic='2018-08-20')
            print "pre", prediction  
            forecast = model_fit.forecast(steps=31)
            
            for inu in range(0,len(forecast)):
                size = forecast[inu]
                print "check"
                
                if size.shape == (len(size),len(param[index]['metric'])):
                    print "check finish "
                
                    forecast = size
                    
                    # for yhat in forecast :
                        
                    #     inverted_0 = inverse_difference(history, yhat[0], interval=1)
                    #     inverted_1 = inverse_difference(history, yhat[1], interval=1)
                        
                    #     final_result1 =  ['%f,%f,%s'.encode('utf-8') % ( inverted_0,inverted_1,categories[ind])]
                    inverted_list = []
                    for inx in range(0,len(forecast)):

                        inverted = inverse_difference(history, forecast[inx], interval=1)
                        inverted_list.append(inverted)
                        # print inverted_list

                        # print inverted_list[0].tolist()
                        # print (str(i) for i in (inverted_list[0].tolist())),end(','),
                        # print (inverted_list[0].tolist()),
                        final_result1 =  [(((inverted_list[0].tolist()),),categories[ind])]         
                                 

                        import csv

                        with open(categories[ind]+'prediction1.csv', 'a') as myfile:
                            wr = csv.writer(myfile)
                            wr.writerow(final_result1)



        # except:
        #     pass


    def read_4th(fn):
        return pd.read_csv(fn)
    import os.path 
    files = [x +'prediction1.csv' for x in categories if os.path.isfile(x +'prediction1.csv') ]

    big_df = pd.concat([read_4th(fn) for fn in files], axis=1)

    big_df.to_csv(key+'final_result.csv')
    files = [x +'prediction1.csv' for x in categories if os.path.isfile(x +'prediction1.csv') ]
    rows =[]
    import os 
    for dex in range (0,len(files)):

        cr = csv.reader(open(files[dex].encode('utf-8'),"rb"))
        
        import csv 
        
        f =open(key+'final_result.csv','wb')
        writer = csv.writer(f)
        
        row_0 = os.path.splitext(files[dex].encode('utf-8'))[0][:-11]
        
        row_1 = sum([float((x[0].split(','))[0]) for x in list(cr)])
        if len(param[index]['metric']) == 2:
        
            cr1 = csv.reader(open(files[dex].encode('utf-8'),"rb"))
            
            row_2 = sum([float((x[0].split(','))[1]) for x in list(cr1)])
            
            rows.append([row_0,row_1,row_2])

        else:
            rows.append([row_0,row_1])
        
        writer.writerow(rows)



    return maxIncidents
    

