from re import X
from sklearn import tree
import mysql.connector




# input all from data base
cnc = mysql.connector.connect(user='root' , password='' ,host='127.0.0.1' ,database='test')
crsr=cnc.cursor()
crsr.execute('SELECT * FROM CARS ;')
lst_cars = crsr.fetchall()


# extract beands from database
lst=[]
for a in lst_cars:
    if not a[0] in lst:
        lst.append(a[0])
        print(a[0])



# filter list by Brand
brand=input('Input Brand from list of top: ')
lst=[]
for b in lst_cars:
    if brand.lower() in  b[0].lower():
        lst.append(b)



# extract models from list
lst_cars=[]
for c in lst:
    if not c[1] in lst_cars:
        lst_cars.append(c[1])
        print(c[1])



# take information from user
user_input=[
    
    input('\nInput model name from list of top (lower and UPPER doesn\'t matter): '),
    int(input('Input model year: ')),
    int(input('Input mile: '))
    
    ]


# filter list by model's
lst_cars=[]
for d in lst:
    if user_input[0].lower() == d[1].lower():
        lst_cars.append(d)

#lst_cars=list(map(lambda x:[x[0],x[1],x[2],int(x[3]),int(x[4])],lst_cars))


#check inputed information
if len(lst_cars)==0 :
    print ('wrong input,please insert just from list.')
    exit()

# machin learning
    #fit data
x_in=[]
x_out=[]
for e in lst_cars:
    x_in.append([int(e[2]),int(e[3])])
    x_out.append(int(e[4]))


clf=tree.DecisionTreeClassifier().fit(x_in, x_out )

answer=clf.predict([user_input[1:]])
answer=str(answer).strip('[]')
answer=answer[:-3]+','+answer[-3:]

print ('\ni guess price may be $%s'%(answer))

