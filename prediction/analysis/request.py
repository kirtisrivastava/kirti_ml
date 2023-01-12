#!/usr/bin/python
import requests
from random import randint

param = [
        {'dimension':'Product Name','from_date':'2018-01-01','to_date':'2018-01-31','metric':('Ad Spend',),'filter':'Ad Spend','sql':'SELECT date_col,IFNULL(product_name_col,"Un-Mapped") as `Product Name`, sum(spend_col) as `Ad Spend` FROM dim_daily_direct_metric_details LEFT JOIN product_master ON product_master.product_code_col = dim_daily_direct_metric_details.product_code_col WHERE date_col BETWEEN "2017-06-01" AND "2017-06-10" GROUP BY date_col,product_name_col ','user':'comcast','model':'','refresh':'false'}
        # {'dimension':'Product Name','from_date':'2018-01-01','to_date':'2018-01-31','metric':('Campaign Name','Creative Name'),'filter':'Ad Spend','sql':'SELECT date_col,IFNULL(product_name_col,"Un-Mapped") as `Product Name`, count( DISTINCT campaign_name_col) as `Campaign Name`, count( DISTINCT creative_name_col) as `Creative Name` FROM dim_daily_direct_metric_details LEFT JOIN campaign_master ON campaign_master.campaign_id_col = dim_daily_direct_metric_details.campaign_id_col AND campaign_master.product_code_col = dim_daily_direct_metric_details.product_code_col LEFT JOIN product_master ON product_master.product_code_col = dim_daily_direct_metric_details.product_code_col LEFT JOIN creative_master ON creative_master.creative_id_col = dim_daily_direct_metric_details.creative_id_col WHERE date_col BETWEEN "2017-06-01" AND "2017-06-10" GROUP BY date_col, product_name_col','user':'comcast','model':'','refresh':'false'},
        # {'dimension':'Site Name','from_date':'2018-01-01','to_date':'2018-01-31','metric':('Ad Spend','CTR'),'filter':'Product Name,CTR','sql':'SELECT date_col,IFNULL(site_name_col,"Un-Mapped") as `Site Name`, sum(spend_col) as `Ad Spend`, (SUM(clicks_col)/SUM(impressions_col))*100 as `CTR` FROM dim_daily_direct_metric_details LEFT JOIN site_master ON site_master.site_id_col = dim_daily_direct_metric_details.site_id_col LEFT JOIN product_master ON product_master.product_code_col=dim_daily_direct_metric_details.product_code_col WHERE date_col BETWEEN "2017-06-01" AND "2017-06-10" AND product_name_col="Xfinity Home Security" GROUP BY site_name_col,date_col','user':'comcast','model':'','refresh':'false'}
        ]
        
index = 0 #randint(0, 2)
try :
	requests.post('http://127.0.0.1:8000/analysis/btprojectresponse/', json = param[index]) 


except requests.exceptions.RequestException as e:
        print('exception caught', e) 
