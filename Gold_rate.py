import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from bs4 import BeautifulSoup
import requests
from tkinter import messagebox
import pandas as pd

root=ttk.Window(themename='solar')
root.iconbitmap('icon.ico')
root.title('F-RateGold')
frame=ttk.LabelFrame(padding=(20,30))
frame.pack(padx=30,pady=30)

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
 

def get_old_rates():
    old_rates_df=pd.read_csv('gold_rates.csv')
    old_rate_window=ttk.Toplevel()
    old_rate_window.title('Old rates')
    old_rate_window.iconbitmap('icon.ico')
    old_rates_frame=ttk.Frame(old_rate_window)
    old_rates_frame.pack(padx=30,pady=30)
    
    date=ttk.Label(old_rates_frame,text='Date',font=('helvetica',18),bootstyle='primary-inverse',padding=(18,2))
    rate=ttk.Label(old_rates_frame,text='Rate',font=('helvetica',18),bootstyle='primary-inverse',padding=(18,2))
    for index,row in old_rates_df.iterrows():
        custom_bootstyle='light'
        #highlite lowest price
        lowest_price=old_rates_df['rates'].min()
        if row['rates']==lowest_price:
           custom_bootstyle='primary'

        old_date=ttk.Label(old_rates_frame,text=row['dates'],font=('helvetica',14),padding=(20,10))
        old_rate=ttk.Label(old_rates_frame,text=row['rates'],font=('helvetice',14),padding=(20,10),bootstyle=custom_bootstyle)
        
        old_date.grid(row=index+1,column=0)
        old_rate.grid(row=index+1,column=1)

    date.grid(row=0,column=0,padx=20)
    rate.grid(row=0,column=1,padx=20)

    back_btn=ttk.Button(old_rates_frame,bootstyle='outline',text='Back',width=30,command=old_rate_window.destroy)
    back_btn_row=int(old_rates_df.index[-1])+2
    back_btn.grid(row=back_btn_row,column=0,columnspan=2,)







header_label=ttk.Label(frame,text="F-RateGold",bootstyle='info',font=('helvetica',18))
date_label=ttk.Label(frame,text='loading rate...',font=('helvetice',10))
gram_rate_label=ttk.Label(frame,text=f'One gram : ₹',bootstyle='primary',font=('helvetica',18),padding=(5,10))
old_rates_btn=ttk.Button(frame,text='Show Old Rates',padding=(13,3),bootstyle='light-outline',command=get_old_rates)


header_label.grid(row=0,column=0)
date_label.grid(row=1,column=0)
gram_rate_label.grid(row=2,column=0)
old_rates_btn.grid(row=3,column=0)


fetch_rate()
root.mainloop()