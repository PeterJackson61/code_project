from re import sub
from socket import socket
import cx_Oracle as cxo
import pandas as pd 
import time
import subprocess
import numpy as np
# def choose_name():
import time 
import seaborn as sns
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.worksheet import dimensions
import matplotlib.pyplot as plt


connection = cxo.connect(user = "", password = "", dsn = "add here:port here/user here")
cursor = connection.cursor()
start = time.time()
def get_lot_fail():
    c = cursor.execute(r"SELECT * FROM TB_LAS_LOT_UDT WHERE MODEL='Y840' and WORK_DATE in ('20220703') fetch first 10 rows only")
    data = pd.DataFrame(c.fetchall(),columns = [row[0] for row in c.description])
    # data.to_csv('barcode_failed.csv')
    # data = data.drop_duplicates(subset = ['LOT'])
    data = data[data['LOT'].str.contains('VSY')]
    data.to_csv('checking_bc_header.csv')
    print(f'Time is {time.time()-start}:.2f')
    return data
get_lot_fail()
def get_bc_fail():
    wd = "20220711"
    c = cursor.execute("SELECT TIME,BARCODE_ID,LOT,VAR16,SITE,EQP FROM TB_LAS_LOT_UDT WHERE MODEL='Y842' and WORK_DATE = :wd", wd=wd)
    data = pd.DataFrame(c.fetchall(),columns = [row[0] for row in c.description])
    print(data)
    # data.to_csv('barcode_failed.csv')
    # data = data.drop_duplicates(subset = ['LOT'])
    data = data[data['LOT'].str.contains('VSY')]
    data.to_csv('barcode_PVT_GENIUS.csv')

    return data
# print(get_bc_fail())
def get_lot(df):
    return df[['LOT','EQP']]
# print(get_lot(get_lot_fail()))
def Preprocessing(df_):
    dict = {'VAR16':'FAIL MODE'}
    df_= df_.sort_values(by = 'TIME', ascending = False)
    df_=df_.drop_duplicates(subset = ['BARCODE_ID'])
    df_.rename(columns = dict, inplace = True)
    return df_

data_test = Preprocessing(get_bc_fail())
fm = set(data_test['FAIL MODE'])
# print(fm)
qty = len(data_test) 
Pivot = data_test.pivot_table(index=['FAIL MODE'], values=['BARCODE_ID'], aggfunc='count')
Pivot = Pivot.sort_values(by = 'BARCODE_ID', ascending= False)
Pivot['FAIL RATE'] = Pivot['BARCODE_ID']/qty*100
list_top_10 = Pivot.index[1:11]

wb = Workbook()
ws = wb.active
Pivot_all = data_test.pivot_table(index = ['EQP','SITE'], values = ['BARCODE_ID'], aggfunc= 'count')
pivot_2 = data_test.pivot_table(index = ['EQP','SITE'], values = ['BARCODE_ID'], columns =['FAIL MODE'],aggfunc= 'count', fill_value =0).reset_index()
pivot_2 = pivot_2.set_axis([y for x,y in pivot_2.columns], axis=1)
pivot_2.columns.values[0] = "MACHINE"
pivot_2.columns.values[1] = "SOCKET"
# pivot_2['MACHINE'] = pivot_2['MACHINE'][5:9]
# for fail_mode in fm:
    # df_ = 
# pivot_2['MACHINE_2'] = pivot_2['MACHINE'][5:9]
headers_tosum = pivot_2.columns
header_loc = list(headers_tosum[2:len(headers_tosum)])
pivot_2['sum'] = pivot_2[header_loc].sum(axis = 1)
# print(headers_tosum)

for col in header_loc:
    pivot_2[col] = pivot_2[col]/pivot_2['sum']*100
pivot_2.to_csv('./testing_data/testing_pyvot_2.csv')
print(header_loc)
# print(Pivot_)
for fail_mode in list_top_10:
    
    print(fail_mode)
    x = 1
    y = 0.5
    sns.set(style='white', font_scale = 2)
    plt.figure(figsize=(12,7), dpi= 150)
    chart = sns.barplot(x='MACHINE', y=fail_mode,data=pivot_2,hue='SOCKET') 
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.gcf().set_size_inches(50,10)
    plt.title(label = f'{fail_mode}',fontsize = 20, color = "black")
    plt.xlabel('Machine',fontsize = 24)
    plt.ylabel('Fail rate', fontsize = 24)
    # plt.figsize = (20,6)
    # plt.legend(bbox_to_anchor=(x,y) ,title_fontsize = 12, loc='center left')
    plt.savefig(f'./Plot/{fail_mode}.png')
    print(f'finishing {fail_mode}')
    # plt.show()

get_lot(get_bc_fail()).to_csv('./testing_data/lot_for_downloading.csv')
print(f'Finished, time is {time.time()-start}:.2f')
# print(list_top_10)
# print(list_fm)
# for fail_mode in list_fm:
#     # data
#     PV_FM = data_test.pivot_table(index = ['EQP','SITE'],values )
# print(Pivot)
# str_bc = '(' + "'" + get_barcode()['BARCODE_ID'][0] + "'"
# for barcode in get_barcode()['BARCODE_ID'][1::]:
#     str_bc = str_bc +','+ "'" + barcode +"'" 
# str_bc = str_bc + ')'
# def get_data():
#     c = cursor.execute(f"SELECT BARCODE_ID,TIME,WORK_DATE,VAR14,VAR16 FROM TB_LAS_LOT_UDT WHERE MODEL='Y840' AND WORK_DATE IN ('20220703') AND BARCODE_ID IN {str_bc}")
#     data = pd.DataFrame(c.fetchall(),columns = [row[0] for row in c.description])
#     data.to_csv('barcode_failed.csv')
    # data = data.drop_duplicates(subset = ['BARCODE_ID'])

    # return data
# print(get_data()
# str_bc = str_bc[0]
# print(str_bc)
# for i in range(5):
# pd_bc = pd.DataFrame()
# barcode_first = get_csv()['BARCODE_ID'][1]
# c = cursor.execute(f"SELECT BARCODE_ID,TIME,VAR14 FROM TB_LAS_LOT_UDT WHERE MODEL='Y840' and BARCODE_ID = '{barcode_first}'")
# data_first = pd.DataFrame(c.fetchall(),columns = [row[0] for row in c.description])
# print(data_first)
    # return data_first
# data_bc_ini = 
# for barcode in get_barcode()['BARCODE_ID']:
#         # print(barcode)
#         # i += 1

#     c = cursor.execute(f"SELECT BARCODE_ID,TIME,VAR14 FROM TB_LAS_LOT_UDT WHERE MODEL='Y840' and BARCODE_ID = '{barcode}'")
#     data_bc = pd.DataFrame(c.fetchall(),columns = [row[0] for row in c.description])
    # merge = pd.concat([data_first,data_bc])
# print(merge)    
def Preprocessing():
    df_ = pd.read_csv('barcode_failed.csv')
    # df_ =df_[df_['LOT'].str.contains('VSY')]
    # df_ = df_.sort_values(by = 'TIME', ascending=False)
    df_ = df_.drop_duplicates(subset = ['BARCODE_ID'])
    df_.to_csv('.csv')
    print(df_.info())

# df_veri = pd.read_csv('./Verify/LOT_TIME.csv')
# # Preprocessing(df_veri)
# df_veri = df_veri.sort_values(by = 'time',ascending= False)
# df_veri = df_veri.drop_duplicates(subset=['barcode'])
# df_veri.to_csv('./Verify/barcode_for_very.csv')
# print(df_veri)
# get_csv()
# Preprocessing()
# c = cursor.execute(r"SELECT count(*) FROM TB_LAS_PRO_TXT")
# list_null= []
# list_zero = list(np.zeros(441-251))
# list_zero = [str(ele) for ele in list_zero]
# # print(list_zero)
# for r in c:
#     list_null.append(str(r))
# list_total = list_null + list_zero
# df['name_null'] = list_total
# # print(list_total)
# # for ele in df['name_null']:
# #     while ele !=0: 
# #         ele = ele.str.strip().str[2:-3]
# df['name_null'] = df['name_null'].str[2:-3]
# # print(df['name_null_2'].info())
# # print(df['name_null_2'])
# print(df)
# df.to_csv('loc_zero.csv')





