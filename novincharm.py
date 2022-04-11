import requests
from bs4 import BeautifulSoup
import mysql.connector
from unidecode import unidecode



#-------------------finding how many page's there are--------------------------
shoes = BeautifulSoup(requests.get('https://novinleather.com/fa/product/cat/%D8%A2%D9%82%D8%A7%DB%8C%D8%A7%D9%86/64-%DA%A9%D9%81%D8%B4.html').text,'html.parser').find("div",attrs={"class":"pagination_container"})
pages_number = int(shoes.find_all('li')[-2].find('a').attrs['data-value'])
#-----------------------------------------------------------------------------

list_of_products=[]
count=0


#----------------------------------------------------scraping from pages-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
for i in range(1,pages_number+1):
    main_page=BeautifulSoup(requests.get('https://novinleather.com/fa/product/cat/%D8%A2%D9%82%D8%A7%DB%8C%D8%A7%D9%86/64-%DA%A9%D9%81%D8%B4.html&keyword=&price_from=698000&price_to=2848000&'+'page=%i&order=price'%(i)).text,'html.parser')
    prodocs=main_page.find("div",attrs={"class":"products"}).find_all('li')
    

    for j in prodocs:
        
        model=j.find("a",attrs={"class":"title"}).text.strip()

        old_price=j.find("div",attrs={"class":"old_price"}).text.replace("تومان","").strip()
        old_price=unidecode(old_price)
        old_price=old_price.replace(',','')
        old_price=int(old_price)

        new_price=j.find("div",attrs={"class":"new_price"}).text.replace("تومان","").strip()
        new_price=unidecode(new_price)
        new_price=new_price.replace(',','')
        new_price=int(new_price)

        discount=j.find("div",attrs={"class":"offer_lbl"}).text.replace('تخفیف','').strip()
        discount=discount.replace('%','')
        discount=unidecode(discount)

        list_of_products.append([model,old_price,new_price,discount])
        count+=1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




#--------------------------------------add to data base-------------------------------------------------
cnc = mysql.connector.connect(user='root' , password='' ,host='127.0.0.1' ,database='test')

crsr=cnc.cursor()
crsr.execute('DELETE FROM novincharm ;')
for k in list_of_products:
    crsr.execute('insert into novincharm values( \'%s\',\'%s\',\'%s\',\'%s\');' %(k[0],k[1],k[2],k[3]))
cnc.commit()
#-------------------------------------------------------------------------------------------------------


print("%i products find."%(count))
