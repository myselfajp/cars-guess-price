import mysql.connector
cnc = mysql.connector.connect(user='root' , password='' ,host='127.0.0.1' ,database='test')


filter_type=input('filter by => price(p) or discount(d) ?')

match filter_type:
    case 'd':
        crsr=cnc.cursor()
        crsr.execute(' SELECT * from novincharm where discount>0 ')
        products=crsr.fetchall()
    case 'p':
        price_filter=input('input price between ex(100000-200000)')
        a=price_filter.split('-')[0]
        b=price_filter.split('-')[1]

        crsr=cnc.cursor()
        crsr.execute(' SELECT * from novincharm where new_price BETWEEN %s AND %s; '%(a,b))
        products=crsr.fetchall()

print(products)
print('%i prodocts find.'%(len(products)))


