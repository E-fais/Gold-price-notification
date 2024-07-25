import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from bs4 import BeautifulSoup
import requests
from tkinter import messagebox
import pandas as pd

root=ttk.Window(themename='solar')
frame=ttk.LabelFrame(padding=(20,30))
frame.pack()

old_rate_dict={
   'dates':[],
   'rates':[]
}


#beautiful soup
url = 'https://goldrate.com/gold-rate-today/kerala/#google_vignette'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def fetch_rate():
    gram_rate_label.config(text='loading price...')
    date_label.config(text='')
    try:
     response = requests.get(url, headers=headers)
     if response.status_code==200:
       soup=BeautifulSoup(response.content,'lxml')
       update_time=soup.find_all('p',class_='gr-update-time')[1].text
       price=soup.find('p',class_='gr-price-rate').strong.text

       date_label.config(text=update_time)
       gram_rate_label.config(text=f'One gram : ₹{price}')


       old_rates_table=soup.findAll('tbody',class_='ranges')
      
       for table in old_rates_table:
         old_rate_datas=table.find_all('tr')
         for rate_data in old_rate_datas:
             date=rate_data.find_all('td')[0].text
             old_rate=rate_data.find_all('td')[1].text

             old_rate_dict['dates'].append(date)
             old_rate_dict['rates'].append(old_rate)
       df=pd.DataFrame(old_rate_dict)  
       df.to_csv('gold_rates.csv',index=False) 
     else:
       messagebox.showerror('Network Error','Cannot connect to server try again later')
    except Exception as err: 
        print(err)
 



old=pd.read_csv('gold_rates.csv')





header_label=ttk.Label(frame,text="F-RateGold",bootstyle='light',font=('helvetica',18))
date_label=ttk.Label(frame,text='loading rate...',font=('helvetice',10))
gram_rate_label=ttk.Label(frame,text='899',bootstyle='primary',font=('helvetica',18),padding=(5,10))


header_label.grid(row=0,column=0)
date_label.grid(row=1,column=0)
gram_rate_label.grid(row=2,column=0)


fetch_rate()
root.mainloop()