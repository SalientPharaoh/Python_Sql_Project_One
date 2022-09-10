import mysql.connector as sql
from tabulate import tabulate
db=sql.connect(host="localhost",user="root",password="****")
cursor=db.cursor()


def Admin(g):
  """Creating the main database and sub-ordinate table of the user"""
  global cursor
  cursor.execute("SHOW DATABASES")
  data=cursor.fetchall()
  inp=(g.lower(),)
  if inp in data: #checking whether database already exists or not
    a="USE "+g
    cursor.execute(a)
    print("SIGNED IN TO ",g)
  else:
    a="USE "+g
    b="CREATE DATABASE "+g
    cursor.execute(b)
    cursor.execute(a)
    cursor.execute("CREATE TABLE Stock (Seller_Gst VARCHAR(200) NOT NULL,City VARCHAR(20),Item INT(25),Bill_No VARCHAR(20) NOT NULL,Amount FLOAT(30),CGST FLOAT(30),SGST FLOAT(30),IGST FLOAT(30),TOTAL FLOAT(30))")
    cursor.execute("CREATE TABLE Sales (Customer_Gst VARCHAR(200) NOT NULL,City VARCHAR(20),Item INT(25),Bill_No VARCHAR(20) NOT NULL,Amount FLOAT(30),CGST FLOAT(30),SGST FLOAT(30),IGST FLOAT(30),TOTAL FLOAT(30))")
    cursor.execute("CREATE TABLE MyPayments (Seller_Gst VARCHAR(200) NOT NULL,Amount_Deposit FLOAT(30),Date_of_Payment VARCHAR(10),Mode VARCHAR(20),cheque_no VARCHAR(30))")
    cursor.execute("CREATE TABLE CPayments (Customer_Gst VARCHAR(200) NOT NULL,Amount_Deposit FLOAT(30),Date_of_Payment VARCHAR(10),Mode VARCHAR(20),cheque_no VARCHAR(30))")
    db.commit()
    print("SIGNED UP TO ",g)

def Stock_update():
  """Inserting data of purchases into stock table"""
  global cursor
  global G
  p="USE "+G
  cursor.execute(p)
  q1=input("Enter seller's GSTIN Please:-\n")
  w=input("Enter the City Please:-\n")
  e=int(input("Enter the Number of items Purchased:-\n"))
  r=input("Enter the Bill Number Please:-\n")
  t=float(input("Enter the Bill Amount Here:-\n"))
  y=float(input("Enter the GST Rate for Taxation Calculation :-\n"))
  s=0.01*y*t
  value=(q1,w,e,r,t,s,s,s,t+3*s)
  cursor.execute("INSERT INTO Stock(Seller_Gst,City,Item,Bill_No,Amount,CGST,SGST,IGST,TOTAL)Values(%s,%s,%s,%s,%s, %s,%s,%s,%s)",value)
  db.commit()
  print(cursor.rowcount,"Data inserted successfully!\n\n")

def Sales_update():
  """Inserting data of sales into sales table"""
  global cursor
  global G
  p="USE "+G
  cursor.execute(p)
  q1=input("Enter customer's GSTIN Please:-\n")
  w=input("Enter the City Please:-\n")
  e=int(input("Enter the Number of items Purchased:-\n"))
  r=input("Enter the Bill Number Please:-\n")
  t=float(input("Enter the Bill Amount Here:-\n"))
  y=int(input("Enter the GST Rate for Taxation Calculation :-\n"))
  s=0.01*y*t
  value=(q1,w,e,r,t,s,s,s,t+3*s)
  cursor.execute("INSERT INTO Sales(Customer_Gst,City,Item,Bill_No,Amount,CGST,SGST,IGST,TOTAL) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",value)
  db.commit()
  print(cursor.rowcount,"Data on hold:-")

  cursor.execute("SELECT SUM(Item)FROM Stock")
  d=cursor.fetchall()
  Amt_b=d[0][0]
  cursor.execute("SELECT SUM(Item)FROM Sales")
  a=cursor.fetchall()
  Amt_s=a[0][0]
  if Amt_b>=Amt_s:
    print("Data Entered successfully!\n\n")
  else:
    print("Insufficient Stock!\n\n")
    dele="DELETE FROM Sales WHERE Bill_No="+r
    cursor.execute(dele)
    db.commit()

def stock():
  """Generating the current stock present with the user"""
  global cursor
  global G
  a="USE "+G
  cursor.execute(a)
  cursor.execute("SELECT SUM(Item)FROM Stock")
  d=cursor.fetchall()
  Amt_b=d[0][0]
  cursor.execute("SELECT SUM(Item)FROM Sales")
  a=cursor.fetchall()
  Amt_s=a[0][0]
  if Amt_s==None:
    stck=Amt_b
  else:
    stck=Amt_b-Amt_s
    print("Current Stock in Hand is:-\n",stck)
    print("\n\n\n\n")
  
def SALES():
  """Generating the report of all the sales of the user"""
  global cursor
  global G
  a="USE "+G
  cursor.execute(a)
  cursor.execute("SELECT * FROM Sales")
  dsale=cursor.fetchall()
  print(tabulate(dsale,headers=["Customer Gst","City","Item","Bill_No","Amount","CGST","SGST","IGST","TOTAL"],tablefmt="fancy_g rid"))
  print("\n\n")

def PURCHASE():
  """Generating the report of all the purchases of he user"""
  global cursor
  global G
  a="USE "+G
  cursor.execute(a)
  cursor.execute("SELECT * FROM Stock")
  dpur=cursor.fetchall()
  print(tabulate(dpur,headers=["Seller Gst","City","Item","Bill_No","Amount","CGST","SGST","IGST","TOTAL"],tablefmt="fancy_g rid"))
  print("\n\n")

def CPAY():
  global cursor
  global G
  exe="USE "+G
  cursor.execute(exe)
  cpay1=input("Enter the Customer GSTIN:-\n")
  amt=float(input("Enter the Amount Accepted:-\n"))
  date=input("Enter the Date of Payment[YYYY-MM-DD]:-\n")
  print("Enter 1 For Cash and 2 For Cheque:-\n")
  mod=int(input("Enter Mode of Payment Please:-"))
  if mod==1:
    mode="CASH"
    cno="----"
    valcc=(cpay1,amt,date,mode,cno)
    cursor.execute("INSERT INTO CPayments(Customer_Gst,Amount_Deposit,Date_of_Payment,Mode,cheque_no) values(%s,%s,%s,%s,%s)",valcc)
    db.commit()
    print(" Cash Pay Updated!")
  elif mod==2:
    mode="CHEQUE"
    cno=input("Enter the Cheque Number Please:-\n")
    valcc=(cpay1,amt,date,mode,cno)
    cursor.execute("INSERT INTO CPayments(Customer_Gst,Amount_Deposit,Date_of_Payment,Mode,cheque_no) values(%s,%s,%s,%s,%s)",valcc)
    db.commit()
    print("CHEQUE Pay Updated!")
  else:
    print("No valid option entered .Repeat the proces!")

def SPAY():
  global cursor
  global G
  exe="USE "+G
  cursor.execute(exe)
  spay1=input("Enter the Seller GSTIN:-\n ")
  amt=float(input("Enter the Amount Accepted:-\n"))
  date=input("Enter the Date of Payment[YYYY-MM-DD]:-\n")
  print("Enter 1 For Cash and 2 For Cheque:-\n")
  mod=int(input("Enter Mode of Payment Please:-"))
  if mod==1:
    mode="CASH"
    cno="----"
    vals=(spay1,amt,date,mode,cno)
    cursor.execute("INSERT INTO MyPayments(Seller_Gst,Amount_Deposit,Date_of_Payment,Mode,cheque_no) values(%s,%s,%s,%s,%s)",vals)
    db.commit()
    print("CASH Pay Updated!\n")
  elif mod==2:
    mode="CHEQUE"
    cno=input("Enter the Cheque Number Please:-\n")
    vals=(spay1,amt,date,mode,cno)
    cursor.execute("INSERT INTO MyPayments(Seller_Gst,Amount_Deposit,Date_of_Payment,Mode,cheque_no) values(%s,%s,%s,%s,%s)",vals)
    db.commit()
    print("CHEQUE Pay Updated!\n")
  else:
    print("Valid Option not entered!\n")

def RCPAY(ls):
  global cursor
  global G
  l=ls
  exe="USE "+G
  cursor.execute(exe)
  ee="SELECT * FROM CPayments WHERE Customer_Gst="+"\'"+l+"\'"
  cursor.execute(ee)
  dd=cursor.fetchall()
  if dd==None:
    print("NO TRANSACTIONS DONE WITH ",l)
  else:
    print("Payments Details of ",l," are as follows:-\n")
    print(tabulate(dd,headers=["Customer Gst","Amount Paid","Date of Payment","Mode of Payment","Cheque Number"],tablefmt="fancy_grid"))
  p="SELECT SUM(TOTAL) FROM Sales WHERE Customer_Gst="+"\'"+l+"\'" cursor.execute(p) payable=cursor.fetchall()
  q="SELECT SUM(Amount_Deposit) FROM CPayments WHERE Customer_Gst="+"\'"+l+"\'"
  cursor.execute(q)
  due=cursor.fetchall()
  try:
    left=payable[0][0]-due[0][0]
    print("Amount Due is :-\n")
    print("RS.",left)
  except:
    print("Amount Due Is:-\n")
    print("RS.",payable[0][0])


def RSPAY(ms):
  global cursor
  global G
  m=ms
  exe="USE "+G
  cursor.execute(exe)
  ee1="SELECT * FROM MyPayments WHERE Seller_Gst="+"\'"+m+"\'"
  cursor.execute(ee1)
  dd1=cursor.fetchall()
  if dd1==None:
    print("NO TRANSACTIONS WITH ",m)
  else:
    print("Payments made to ",m," are as follows:-\n")
    print(tabulate(dd1,headers=["Seller Gst","Amount Paid","Date of Payment","Mode of Payment","Cheque Number"],tablefmt="fancy_grid"))
  p="SELECT SUM(TOTAL) FROM Stock WHERE Seller_Gst="+"\'"+m+"\'" cursor.execute(p) payable=cursor.fetchall()
  q="SELECT SUM(Amount_Deposit) FROM MyPayments WHERE Seller_Gst="+"\'"+m+"\'"
  cursor.execute(q)
  due=cursor.fetchall()
  try:
    left=payable[0][0]-due[0][0]
    print("Amount Due is :-\n")
    print("RS.",left)
  except:
    print("Amount Due Is:-\n")
    print("RS.",payable[0][0])

    
def customer_report(customergst):
  """Generating the data of particular customer"""
  global cursor
  global G
  a="USE "+G
  cursor.execute(a)
  crep="SELECT * FROM Sales WHERE Customer_Gst="+"\'"+customergst+"\'"
  cursor.execute(crep)
  cdrep=cursor.fetchall()
  print("Printing all the Purchases of ",customergst)
  print(tabulate(cdrep,headers=["Customer Gst","City","Item","Bill_No","Amount","CGST","SGST","IGST","TOTAL"],tablefmt="fancy_g rid")) print("\n Printing the Payments made by ",customergst)
  RCPAY(customergst)
  print("\n\n")

  
def seller_report(sellergst):
  """Generating the data of particular seller"""
  global cursor
  global G
  a="USE "+G
  cursor.execute(a)
  srep="SELECT * FROM Stock WHERE Seller_Gst="+"\'"+sellergst+"\'"
  cursor.execute(srep)
  sdrep=cursor.fetchall()
  print("Printing all the Purchases from ",sellergst)
  print(tabulate(sdrep,headers=["Seller Gst","City","Item","Bill_No","Amount","CGST","SGST","IGST","TOTAL"],tablefmt="fancy_g rid")) print("\n Printing the Payments made to ",sellergst)
  RSPAY(sellergst)
  print("\n\n")

  
def Report():
  """Generating the reports required from the table"""
  global cursor
  global G
  print("1.Generate the report of a customer\n2.Generate the report of a seller\n3.Current stock\n4.All sales\n5.All purchases")
  v=int(input("Enter the desired number to generate the report:-"))
  print()
  if v==1:
    cust=input("Enter the GSTIN number of the customer:-")
    print("Fetching Customer details:-\n")
    customer_report(cust)
  elif v==2:
    sel=input("Enter the GSTIN number of the customer:-")
    print("Fetching Seller details:-\n")
    seller_report(sel)
  elif v==3:
    print("Fetching the current stock in hand:-")
    stock()
  elif v==4:
    print("Printing all your sales :-")
    SALES()
  elif v==5:
    print("Printing all your purchases:-")
    PURCHASE()
  else:
    print("Enter a valid command to execute!")
    print("\n\n")


def payments():
  print("Welcome to the Payment Update Section:-\n")
  print("1.Enter a Payment made by Customer:-\n2.Enter a payment made to Seller:-\n")
  pay=int(input("Choose the corresponding Number:-"))
  if pay==1:
    print("Customer Payments Section Accessed:-")
    CPAY()
  elif pay==2:
    print("Seller Payements Section Accessed:-")
    SPAY()
  else:
    print("Enter a Valid Option Please:-!")


def over():
  """Closing the database connection"""
  db.commit()
  db.close()
  print("Thank you for using Business managment system!\n")

#main program
G=input("Enter your GSTIN Please:-\n")
Admin(G)
print("\n Enter the Number corresponding to the required function:-")
while(1):
  mast=int(input("1.Entering a purchase\n2.Entering a sale\n3.Generating a Report\n4.Payment Update and Reports\n5.Exit\n"))
  if mast==1:
    print("Purchase Register Accessed\n")
    Stock_update()
  elif mast==2:
    print("Sales Register Accessed\n")
    Sales_update()
  elif mast==3:
    Report()
  elif mast==4:
    payments()
  elif mast==5:
    over()
    break
  else:
    print("Enter a Valid Command Please!\n")




