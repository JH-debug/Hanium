import pandas as pd
import pymysql
from datetime import datetime

print('start-time: ', str(datetime.now())[:19])

conn = pymysql.connect(host='54.180.17.157', user='chatbot', password='chatbot', db='medgroup', charset='utf8')
query = 'select * from medchat_app_tbl_medicine_info'

df = pd.read_sql_query(query, conn)
df.to_csv(r'backup.csv', index=False)
print('end-time: ', str(datetime.now())[:19])
