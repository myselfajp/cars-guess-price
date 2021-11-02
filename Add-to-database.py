import requests
from bs4 import BeautifulSoup
import mysql.connector


# take list of car's name from "truecar" site 

cars_page = BeautifulSoup(requests.get('https://www.truecar.com/used-cars-for-sale').text,'html.parser').find('select',attrs={"aria-label":"Make"})
cars = cars_page.find_all("option")


for i in cars:
    print(i.text)

# take car name from user and get his site

while  True:

    selected_car = input('\n input a car name from list of top :(lower and UPPER doesn\'t matter) ').strip().replace(' ','-').lower()

    for i in cars:
        if selected_car in i.text.lower():
            selected_car=i.text.lower()
            break

    if selected_car!=i.text.lower():
        print('can\'t find this car,chek you\'r inputed name ' )
    else:
        break



# extract Name,Model,Year,Miles,Price from 
page_counter=1
lst_cars=[]

    #extract number of page's and take from user ,how mach want to add
number_of_pages=BeautifulSoup(requests.get('https://www.truecar.com/used-cars-for-sale/listings/%s/location-birmingham-al/?page=%i&searchRadius=5000' %(selected_car,page_counter)).text,'html.parser')
number_of_pages=number_of_pages.find('li',attrs={"data-test":"mobilePageRange"})
number_of_pages=int(input('\n there is %s page\'s , how many page you want to add? '%(number_of_pages.text.split()[3])))

    # extract Name,Model,Year,Miles,Price
while page_counter<=number_of_pages:
    try:
        
        main_page=BeautifulSoup(requests.get('https://www.truecar.com/used-cars-for-sale/listings/%s/location-birmingham-al/?page=%i&searchRadius=5000' %(selected_car,page_counter)).text,'html.parser')
        list_of_cars=main_page.find_all('li',attrs={"data-qa":"Listings"})
        for j in list_of_cars:

            if ("No accidents" in j.text) and (not "No Price" in j.text):

                name=j.find('span',attrs={"class":"vehicle-header-make-model text-truncate"}).text.split()[0]
                model=j.find('span',attrs={"class":"vehicle-header-make-model text-truncate"}).text.replace(name,'').strip()
                year=int(j.find('span',attrs={"class":"vehicle-card-year font-size-1"}).text)
                miles=int(j.find('div',attrs={"data-test":"vehicleMileage"}).text.strip(' miles').replace(',',''))
                price=int(j.find('div',attrs={"class":"heading-3 margin-y-1 font-weight-bold"}).text.strip('$').replace(',',''))

                if not [name,model,year,miles,price] in lst_cars:
                    lst_cars.append([name,model,year,miles,price])



        print("page %i added" %(page_counter))
        page_counter+=1
        
    except:
        print('connection problem. try again :(')
        exit()



cnc = mysql.connector.connect(user='root' , password='' ,host='127.0.0.1' ,database='test')
crsr=cnc.cursor()
lst_databases=crsr.execute('SELECT * FROM CARS ;')
lst_databases=crsr.fetchall()     

#check repetitious value's and add new's to database
add_counter=0
for k in lst_cars:
    if not tuple(k) in lst_databases:
        crsr.execute('insert into cars value(\'%s\',\'%s\',\'%i\',\'%i\',\'%f\');' %(k[0],k[1],k[2],k[3],k[4]))
        add_counter+=1
cnc.commit()


print("\n %i new car\'s added to data base "%(add_counter))