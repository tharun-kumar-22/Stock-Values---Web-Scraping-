#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
import linecache
import pandas as pd

with open(r"url.txt", 'r') as fp:
    for count, line in enumerate(fp):
        pass
number_of_entries = count + 2

List=[]
for x in range(1,number_of_entries):
    Link = linecache.getline('url.txt', x)
    url = Link.rstrip("\n")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tag = soup.find_all('li', class_ ="flex flex-space-between")
    m = []
    for i in tag:
        i = i.get_text().replace('\n',"")
        i = i.strip(" ")
        m.append(i)
    data = pd.DataFrame()
    for title in soup.find_all('title'):
        title=title.get_text().replace('financial results and price chart - Screener',"")
    data[title] = m
    df=data.drop([0,5,8])
    df=df.replace(to_replace ={"Current Price","High / Low","Stock P/E","Book Value","ROCE","ROE"}, value ="",regex=True)
    df.index = ['Current_Price in ₹','High/Low in ₹','Stock P/E ratio','Book Value in ₹','ROCE in %','ROE in %']
    List.append(df)
for x in List:
    x

result = pd.concat(List)
dfT=result.T
df1=dfT.groupby(dfT.columns, axis=1).sum()
dff1=df1.drop(['High/Low in ₹'], axis = 1)
dff2=df1['High/Low in ₹'].str.split('/', expand=True)
dff2.columns =['High in ₹','Low in ₹']
dff3= pd.merge(dff1, dff2, left_index=True, right_index=True)
dff4=dff3.replace(to_replace ={"₹",",","%"}, value ="",regex=True)
dff4[['Current_Price in ₹','High in ₹','Low in ₹','Stock P/E ratio','Book Value in ₹','ROCE in %','ROE in %']] = dff4[['Current_Price in ₹','High in ₹','Low in ₹','Stock P/E ratio','Book Value in ₹','ROCE in %','ROE in %']].astype(float)
dff4['High in ₹ - Current_Price in ₹'] = dff4['High in ₹'] - dff4['Current_Price in ₹']
dff4['Percent_change_of_Current_Price_from_High in %']=(dff4['High in ₹ - Current_Price in ₹']/dff4['High in ₹'])*100
dfFinal=dff4.drop(['High in ₹ - Current_Price in ₹'], axis = 1)


file_name = 'StockValues.xlsx'

dfFinal.to_excel(file_name)
print('DataFrame is written to Excel File successfully.')

