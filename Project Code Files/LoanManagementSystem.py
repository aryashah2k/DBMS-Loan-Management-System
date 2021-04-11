import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import datetime
from datetime import date

HEIGHT = 400
WIDTH = 400


#create database or commit to one
conn = sqlite3.connect('LoanManager.db')

#create cursor
c = conn.cursor()


class main(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        canvas = tk.Canvas(self, height = HEIGHT, width = WIDTH)
        canvas.pack()
        self.frames = {}

        for F in (StartPage, AddLoan, ViewLoan, AddCustomer, AssignLoan, LoanRepayment):

            frame = F(canvas, self)

            self.frames[F] = frame

            frame.place(relx = 0.1, rely = 0.05, relwidth = 0.8, relheight = 0.89)

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise() 

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent, bg='#80c1ff')


        label = tk.Label(self, text="Loan Management System")

        label.place(relx = 0.11, rely = 0.05, relwidth = 0.8, relheight = 0.05)

        label = tk.Label(self, text="Home Page")

        label.place(relx = 0.3, rely = 0.15, relwidth = 0.4, relheight = 0.05)

        button = tk.Button(self, text="Add New Loan Product",
                            command=lambda: controller.show_frame(AddLoan))
        button.place(relx = 0.26, rely = 0.25, relwidth = 0.5, relheight = 0.1)

        button2 = tk.Button(self, text="Search Loan Product",
                            command=lambda: controller.show_frame(ViewLoan))
        button2.place(relx = 0.26, rely = 0.37, relwidth = 0.5, relheight = 0.1)

        button3 = tk.Button(self, text="Add New Customer",
                            command=lambda: controller.show_frame(AddCustomer))
        button3.place(relx = 0.26, rely = 0.49, relwidth = 0.5, relheight = 0.1)

        button4 = tk.Button(self, text="Assign Loan to Customer",
                            command=lambda: controller.show_frame(AssignLoan))
        button4.place(relx = 0.26, rely = 0.61, relwidth = 0.5, relheight = 0.1)

        button4 = tk.Button(self, text="Loan Repayment",
                            command=lambda: controller.show_frame(LoanRepayment))
        button4.place(relx = 0.26, rely = 0.73, relwidth = 0.5, relheight = 0.1)

        #quit button
        quit_btn = tk.Button(self, text ="Quit", command= self.quit)
        quit_btn.place(relx = 0.31, rely = 0.87, relwidth = 0.4, relheight = 0.1)


class AddLoan(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent, bg='#80c1ff')

        label = tk.Label(self, text="Add Loan Product to Database")

        label.place(relx = 0.11, rely = 0.02, relwidth = 0.8, relheight = 0.05)

        #Create table
        
        c.execute("""CREATE TABLE IF NOT EXISTS AddLoanProduct (
                       LoanTypeID integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                       LoanType varchar,
                       FixedInterestRate float,
                       FloatingInterestRate float,
                       Eligibility integer, 
                       PreClosureFine float,
                       LateEMIFine float
                            )""")
        

        #Create Submit function
        def submit():

            #Check if all fields are filled and show error message if not filled
            tablelist = [LoanType,FixedInterestRate, FloatingInterestRate,Eligibility,PreClosureFine,LateEMIFine]
            for i in tablelist:
                if len(i.get()) == 0:
                    messagebox.showerror("Error", "Enter all fields")
                    return

            #Create database or commit to one
            conn = sqlite3.connect('LoanManager.db')

            #Create cursor
            c = conn.cursor()

            #Insert into table
            c.execute("INSERT INTO AddLoanProduct VALUES(:LoanTypeID, :LoanType, :FixedInterestRate, :FloatingInterestRate, :Eligibility, :PreClosureFine, :LateEMIFine)",
                {'LoanTypeID': None, 'LoanType': LoanType.get(), 'FixedInterestRate': FixedInterestRate.get(), 'FloatingInterestRate': FloatingInterestRate.get(), 'Eligibility': Eligibility.get(), 'PreClosureFine': PreClosureFine.get(), 'LateEMIFine': LateEMIFine.get()}

                )

            #Commit changes
            conn.commit()

            #Close connection
            conn.close()

            #Clear text boxes
            LoanType.delete(0, tk.END)
            FixedInterestRate.delete(0, tk.END)
            FloatingInterestRate.delete(0, tk.END)
            Eligibility.delete(0, tk.END)
            PreClosureFine.delete(0, tk.END)
            LateEMIFine.delete(0, tk.END)


        #Validation functions
        def correct(inp):
            if inp.isdigit():
                return True
            elif inp == "":
                return True
            else:
                return False

        def floatcorrect(inp):
            if inp.isdigit():
                return True
            elif '.' in inp:
                return True
            elif inp == "":
                return True
            else:
                return False

        #Registering validation variables with functions
        reg = self.register(correct)
        reg1 = self.register(floatcorrect)


        #Create Text Boxes
        LoanType = tk.Entry(self, bg = "grey")
        LoanType.place(relx = 0.48, rely = 0.15, relwidth = 0.5, relheight = 0.05)

        FixedInterestRate = tk.Entry(self, bg = "grey")
        FixedInterestRate.place(relx = 0.48, rely = 0.25, relwidth = 0.5, relheight = 0.05)

        FloatingInterestRate = tk.Entry(self, bg = "grey")
        FloatingInterestRate.place(relx = 0.48, rely = 0.35, relwidth = 0.5, relheight = 0.05)

        Eligibility = tk.Entry(self, bg="grey")
        Eligibility.place(relx = 0.48, rely = 0.45, relwidth = 0.5, relheight = 0.05)

        PreClosureFine = tk.Entry(self, bg="grey")
        PreClosureFine.place(relx = 0.48, rely = 0.55, relwidth = 0.5, relheight = 0.05)

        LateEMIFine = tk.Entry(self, bg = "grey")
        LateEMIFine.place(relx = 0.48, rely = 0.65, relwidth = 0.5, relheight = 0.05)

        #Create Labels
        LoanTypeLabel = tk.Label(self, text = "Loan Type:")
        LoanTypeLabel.place(relx = 0.05, rely = 0.15, relwidth = 0.4, relheight = 0.05)

        FixedInterestRateLabel = tk.Label(self, text = "Fixed Interest Rate(%):")
        FixedInterestRateLabel.place(relx = 0.05, rely = 0.25, relwidth = 0.4, relheight = 0.05)

        FloatingInterestLabel = tk.Label(self, text = "Floating Interest Rate(%):")
        FloatingInterestLabel.place(relx = 0.05, rely = 0.35, relwidth = 0.4, relheight = 0.05)

        EligibilityLabel = tk.Label(self, text = "Eligibility:")
        EligibilityLabel.place(relx = 0.05, rely = 0.45, relwidth = 0.4, relheight = 0.05)

        PreClosureFineLabel = tk.Label(self, text = "Pre Closure Fine(%):")
        PreClosureFineLabel.place(relx = 0.05, rely = 0.55, relwidth = 0.4, relheight = 0.05)

        LateEMIFineLabel = tk.Label(self, text = "Late EMI Fine:")
        LateEMIFineLabel.place(relx = 0.05, rely = 0.65, relwidth = 0.4, relheight = 0.05)

        #Assigining validation to entry boxes
        FixedInterestRate.config(validate = 'key', validatecommand = (reg1, '%P'))
        FloatingInterestRate.config(validate = 'key', validatecommand = (reg1, '%P'))
        Eligibility.config(validate = 'key', validatecommand = (reg, '%P'))
        PreClosureFine.config(validate = 'key', validatecommand = (reg1, '%P'))
        LateEMIFine.config(validate = 'key', validatecommand = (reg1, '%P'))


        #Create submit button
        submit_btn = tk.Button(self, text = "Add Loan to Database", bg = "grey", command = submit)
        submit_btn.place(relx = 0.1, rely = 0.78, relwidth = 0.5, relheight = 0.08)

        #Create Back Button
        back_btn = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        back_btn.place(relx = 0.67, rely = 0.78, relwidth = 0.25, relheight = 0.08)


class ViewLoan(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent, bg='#80c1ff')

        label = tk.Label(self, text="Search Loan using Loan Product")

        label.place(relx = 0.11, rely = 0.02, relwidth = 0.8, relheight = 0.05)

        #Create query function
        def query():

            #Create database or commit to one
            conn = sqlite3.connect('LoanManager.db')

            #Create cursor
            c = conn.cursor()

            #Query the database
            c.execute("SELECT * FROM LoanAssign WHERE LoanType = ?", (variable.get(),) )

            #Commit changes
            conn.commit()

            #Fetch details from table
            details = c.fetchall()

            #Create an empty string to store the fetched details
            print_details = ''

            #Remove Formatting and add details to empty string
            for j in details:
                print_details += "\n" + "Customer ID: " + str(j[0]) + "\n" + "Loan Amount: " + str(j[2]) + "\n" "Loan Tenure: " + str(j[5]) + "\n" + "Interest Rate(%): " + str(j[6]) + "\n"

            #Create Query Label to print the loan details
            query_label = tk.Label(self, text= print_details)
            query_label.place(relx = 0.32, rely = 0.25, relwidth = 0.4, relheight = 0.6)

            #Close connection
            conn.close()

        #Create database or commit to one
        conn = sqlite3.connect('LoanManager.db')

        #Create cursor
        c = conn.cursor()

        #Query the database
        c.execute("SELECT LoanType FROM AddLoanProduct")

        #Commit changes
        conn.commit()

        #Fetch details from table
        records = c.fetchall()
        
        #Check if there are records in the table
        if records != []:

            #Create an empty list to store details of loan and remove formatting to add to newly creaed list
            loanproducts= []

            for i in records:
                loanproducts.append(i[0])

            #Create a variable and set it to default value of loanproducts list
            variable = tk.StringVar(self)
            variable.set(loanproducts[0]) 

            #Create Drop Down widget 
            DropDown = tk.OptionMenu(self, variable, *loanproducts)
            DropDown.place(relx = 0.28, rely = 0.15, relwidth = 0.5, relheight = 0.05)

        #Show Error if no loan products are created
        else:
            errorlabel = tk.Label(self, text = "Add Loan products first!!")
            errorlabel.place(relx = 0.28, rely = 0.15, relwidth = 0.5, relheight = 0.05)
        
        #Create Query Button
        query_btn = tk.Button(self, text= "Search", command= query)
        query_btn.place(relx = 0.1, rely = 0.87, relwidth = 0.5, relheight = 0.08)

        #Create Quit Button
        back_btn = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        back_btn.place(relx = 0.67, rely = 0.87, relwidth = 0.25, relheight = 0.08)


class AddCustomer(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#80c1ff')

        label = tk.Label(self, text="Add Customer Details to Database")

        label.place(relx = 0.11, rely = 0.02, relwidth = 0.8, relheight = 0.05)

        #Create table
        c.execute("""CREATE TABLE IF NOT EXISTS AddNewCustomer (
                    CustomerID integer,
                    CustomerName varchar,
                    Address varchar,
                    Phonenum integer,
                    Email varchar,
                    DOB date
                        )""")
        

        #Create submit function
        def submit():

            #Check if all fields are filled and show error message if not filled
            tablelist = [CustomerID, CustomerName, Address, Phonenum, Email, DOB]
            for i in tablelist:
                if len(i.get()) == 0:
                    messagebox.showerror("Error", "Enter all fields")
                    return

            #regular expression to check email format
            emailre = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

            #Check email format and show error message if invalid
            if (emailre.match(Email.get()) == None):
                messagebox.showerror("Error", "Invalid Email")
                return

            #Check phone number format and show error message if invalid
            if (len(Phonenum.get()) != 10):
                messagebox.showerror("Error","Invalid Number")
                return

            #Check date format and show error message if invalid
            form_date = DOB.get()
            try:
                day,month,year = map(int,form_date.split('/'))
                date = datetime.date(year,month,day)
            except:
                messagebox.showerror("Format Error","Must enter in DD/MM/YYYY format")
                return


            #Create database or commit to one
            conn = sqlite3.connect('LoanManager.db')

            #Create cursor
            c = conn.cursor()

            #Insert into table
            c.execute("INSERT INTO AddNewCustomer VALUES(:CustomerID, :CustomerName, :Address, :Phonenum, :Email, :DOB)",
                {'CustomerID': CustomerID.get(), 'CustomerName': CustomerName.get(), 'Address': Address.get(), 'Phonenum': Phonenum.get(), 'Email': Email.get(), 'DOB': DOB.get() }

                )
            #Commit changes
            conn.commit()

            #Close connection
            conn.close()

            #Clear text boxes
            CustomerID.delete(0, tk.END)
            CustomerName.delete(0, tk.END)
            Address.delete(0, tk.END)
            Phonenum.delete(0, tk.END)
            Email.delete(0, tk.END)
            DOB.delete(0, tk.END)


        #Validation functions
        def correct(inp):
            if inp.isdigit():
                return True
            elif inp == "":
                return True
            else:
                return False


        #Registering validation variables with functions
        reg = self.register(correct)

        #Create Text Boxes
        CustomerID = tk.Entry(self, bg = "grey")
        CustomerID.place(relx = 0.48, rely = 0.15, relwidth = 0.5, relheight = 0.05)

        CustomerName = tk.Entry(self, bg = "grey")
        CustomerName.place(relx = 0.48, rely = 0.25, relwidth = 0.5, relheight = 0.05)

        Address = tk.Entry(self, bg="grey")
        Address.place(relx = 0.48, rely = 0.35, relwidth = 0.5, relheight = 0.05)

        Phonenum = tk.Entry(self, bg="grey")
        Phonenum.place(relx = 0.48, rely = 0.45, relwidth = 0.5, relheight = 0.05)

        Email = tk.Entry(self, bg="grey")
        Email.place(relx = 0.48, rely = 0.55, relwidth = 0.5, relheight = 0.05)

        DOB = tk.Entry(self, bg="grey")
        DOB.place(relx = 0.48, rely = 0.65, relwidth = 0.5, relheight = 0.05)

        #Create Labels
        CustomerIDLabel = tk.Label(self, text = "Customer ID:")
        CustomerIDLabel.place(relx = 0.05, rely = 0.15, relwidth = 0.4, relheight = 0.05)

        CustomerNameLabel = tk.Label(self, text = "Customer Name:")
        CustomerNameLabel.place(relx = 0.05, rely = 0.25, relwidth = 0.4, relheight = 0.05)

        AddressLabel = tk.Label(self, text = "Address:")
        AddressLabel.place(relx = 0.05, rely = 0.35, relwidth = 0.4, relheight = 0.05)

        PhonenumLabel = tk.Label(self, text = "Phone number:")
        PhonenumLabel.place(relx = 0.05, rely = 0.45, relwidth = 0.4, relheight = 0.05)

        EmailLabel = tk.Label(self, text = "Email")
        EmailLabel.place(relx = 0.05, rely = 0.55, relwidth = 0.4, relheight = 0.05)

        DOBLabel = tk.Label(self, text = "DOB")
        DOBLabel.place(relx = 0.05, rely = 0.65, relwidth = 0.4, relheight = 0.05)

                
        #Assigining validation to entry boxes
        CustomerID.config(validate = 'key', validatecommand = (reg, '%P'))
        Phonenum.config(validate = 'key', validatecommand = (reg, '%P'))

        #Create submit button
        submit_btn = tk.Button(self, text = "Add Customer to Database", bg = "grey", command = submit)
        submit_btn.place(relx = 0.1, rely = 0.87, relwidth = 0.5, relheight = 0.08)

        #create Quit Button
        back_btn = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        back_btn.place(relx = 0.67, rely = 0.87, relwidth = 0.25, relheight = 0.08)


class LoanRepayment(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent, bg='#80c1ff')

        label = tk.Label(self, text="Loan Repayment")

        label.place(relx = 0.11, rely = 0.02, relwidth = 0.8, relheight = 0.05)

        #Create table 
        c.execute("""CREATE TABLE IF NOT EXISTS RepayLoan (
                       CustomerID integer,
                       LoanType varchar,
                       EMIAmount float,
                       LateEMIFine float,
                       RepaymentDate float
                            )""")
        
        #Create variables to get data from entry box
        z= tk.StringVar()
        y = tk.StringVar()
    
        #Create submit function
        def submit():

            #Check if all fields are filled and show error message if not filled
            tablelist = [CustomerID, LoanType, LateEMIFine, RepaymentDate]
            for i in tablelist:
                if len(i.get()) == 0:
                    messagebox.showerror("Error", "Enter all fields")
                    return

            #Create database or commit to one
            conn = sqlite3.connect('LoanManager.db')

            #Create cursor
            c = conn.cursor()
            emi=0
            #Insert into table
            c.execute("INSERT INTO RepayLoan VALUES(:CustomerID, :LoanType, :EMIamount, :LateEMIFine, :RepaymentDate)",
                {'CustomerID': CustomerID.get(), 'LoanType': LoanType.get(), 'EMIamount': emi, 'LateEMIFine': LateEMIFine.get(), 'RepaymentDate': RepaymentDate.get()}

                )
            #Commit changes
            conn.commit()

            #Close connection
            conn.close()

            #Clear text boxes
            CustomerID.delete(0, tk.END)
            LoanType.delete(0, tk.END)
            LateEMIFine.delete(0, tk.END)
            RepaymentDate.delete(0, tk.END)

        #Create query function
        def query():

            #Create database or commit to one
            conn = sqlite3.connect('LoanManager.db')

            #Create cursor
            c = conn.cursor()

            #Query the database
            c.execute("SELECT CustomerName FROM AddNewCustomer WHERE CustomerID = ?", (z.get(),))

            #Fetch details from table
            name = c.fetchone()
            
            #create label to display Customer Name as fetched from table
            CustomerNameLabel = tk.Label(self, text= name)
            CustomerNameLabel.place(relx = 0.48, rely = 0.35, relwidth = 0.4, relheight = 0.05)

            #Query the database
            c.execute("SELECT * FROM LoanAssign WHERE CustomerID = ? AND LoanType = ?", ( z.get(), y.get() ))
            
            #Commit changes
            conn.commit()

            #Fetch details from table
            details = c.fetchall()
            
            #Seperate out the Principal(p), Number of monthly installments or tenure(n) and Annual Interest Rate(annual)
            p = int(details[0][2])
            n = int(details[0][5])
            annual = int(details[0][6])

            #Determine monthly interest rate (r)
            r = (annual /12) / 100

            #Create label to display interest rate as fetched from table 
            InterestRateLabel = tk.Label(self, text= annual)
            InterestRateLabel.place(relx = 0.48, rely = 0.45, relwidth = 0.4, relheight = 0.05)

            #Calculate the EMI Amount
            q = (1+r)**n 
            emi =  p * r * ( q / (q -1) ) 

            #Create Label to display EMI amount as calculated
            EMIamountLabel = tk.Label(self, text= "{0:.2f}".format(emi))
            EMIamountLabel.place(relx = 0.48, rely = 0.55, relwidth = 0.4, relheight = 0.05)


            #Commit changes
            conn.commit()

            #Close connection
            conn.close()

        
        #create Text Boxes
        CustomerID = tk.Entry(self, bg = "grey",  textvariable = z)
        CustomerID.place(relx = 0.48, rely = 0.15, relwidth = 0.5, relheight = 0.05)

        LoanType = tk.Entry(self, bg = "grey", textvariable = y)
        LoanType.place(relx = 0.48, rely = 0.25, relwidth = 0.5, relheight = 0.05)

        LateEMIFine = tk.Entry(self, bg = "grey")
        LateEMIFine.place(relx = 0.48, rely = 0.65, relwidth = 0.5, relheight = 0.05)

        RepaymentDate = tk.Entry(self, bg = "grey")
        RepaymentDate.place(relx = 0.48, rely = 0.75, relwidth = 0.5, relheight = 0.05)

        #Create Labels
        CustomerIDLabel = tk.Label(self, text = "Customer ID:")
        CustomerIDLabel.place(relx = 0.05, rely = 0.15, relwidth = 0.4, relheight = 0.05)

        LoanTypeLabel = tk.Label(self, text = "Loan Type:")
        LoanTypeLabel.place(relx = 0.05, rely = 0.25, relwidth = 0.4, relheight = 0.05)


        #Create Query Button
        query_btn = tk.Button(self, text= "Get Details", command= query)
        query_btn.place(relx = 0.05 , rely = 0.87, relwidth = 0.3, relheight = 0.08)


        #Create Labels 
        CustomerNameLabel = tk.Label(self, text = "Customer Name:")
        CustomerNameLabel.place(relx = 0.05, rely = 0.35, relwidth = 0.4, relheight = 0.05)

        InterestRateLabel = tk.Label(self, text = "Interest Rate:")
        InterestRateLabel.place(relx = 0.05, rely = 0.45, relwidth = 0.4, relheight = 0.05)

        EMIamountLabel = tk.Label(self, text = "EMI Amount:")
        EMIamountLabel.place(relx = 0.05, rely = 0.55, relwidth = 0.4, relheight = 0.05)

        LateEMIFineLabel = tk.Label(self, text = "Late EMI Fine:")
        LateEMIFineLabel.place(relx = 0.05, rely = 0.65, relwidth = 0.4, relheight = 0.05)

        RepaymentDateLabel = tk.Label(self, text = "Repayment Date:")
        RepaymentDateLabel.place(relx = 0.05, rely = 0.75, relwidth = 0.4, relheight = 0.05)

 
        #Create submit button
        submit_btn = tk.Button(self, text = "Submit", bg = "grey", command = submit)
        submit_btn.place(relx = 0.37, rely = 0.87, relwidth = 0.3, relheight = 0.08)


        #Create Quit Button
        back_btn = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        back_btn.place(relx = 0.69, rely = 0.87, relwidth = 0.25, relheight = 0.08)


class AssignLoan(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent, bg='#80c1ff')

        label = tk.Label(self, text="Assign Loan to Customer")

        label.place(relx = 0.11, rely = 0.02, relwidth = 0.8, relheight = 0.05)


        #Create table
        c.execute("""CREATE TABLE IF NOT EXISTS LoanAssign (
                       CustomerID integer,
                       LoanType varchar,
                       LoanAmount float,
                       Salary float,
                       FixedObligations float,
                       LoanTenure int,
                       InterestRate float
                            )""")
        
        #Create submit function
        def submit():

            #Check if all entries all filled if not show error message
            tablelist = [CustomerID, LoanType,LoanAmount, Salary, FixedObligations, LoanTenure, InterestRate]
            for i in tablelist:
                if len(i.get()) == 0:
                    messagebox.showerror("Error", "Enter all fields")
                    return

            #Check if customer is eligible for loan if not show error message
            if(self.eligibility == "Not Eligible"):
                messagebox.showerror("Error", "Customer not eligible. Can not submit")
                return

            #Create database or commit to one
            conn = sqlite3.connect('LoanManager.db')

            #Create cursor
            c = conn.cursor()

            #Insert into table
            c.execute("INSERT INTO LoanAssign VALUES(:CustomerID, :LoanType, :LoanAmount, :Salary, :FixedObligations, :LoanTenure,:InterestRate)",
                {'CustomerID': CustomerID.get(), 'LoanType': LoanType.get(), 'LoanAmount': LoanAmount.get(), 'Salary': Salary.get(), 'FixedObligations': FixedObligations.get(), 'LoanTenure': LoanTenure.get(),'InterestRate': InterestRate.get()}
                )
            #Commit changes
            conn.commit()

            #Close connection
            conn.close()

            #Clear text boxes
            CustomerID.delete(0, tk.END)
            LoanType.delete(0, tk.END)
            LoanAmount.delete(0, tk.END)
            Salary.delete(0, tk.END)
            FixedObligations.delete(0, tk.END)
            LoanTenure.delete(0, tk.END)
            InterestRate.delete(0, tk.END)

        
        #Validation function
        def correct(inp):
            if inp.isdigit():
                return True
            elif inp == "":
                return True
            else:
                return False

        #Registering validation variables with functions
        reg = self.register(correct)

        #Create query function
        def query():

            #Create database or commit to one
            conn = sqlite3.connect('LoanManager.db')

            #Create cursor
            c = conn.cursor()

            #Query the database
            c.execute("SELECT Eligibility FROM AddLoanProduct WHERE LoanType = ?", (z.get(),) )
            
            #Commit changes
            conn.commit()

            #Fetch details from database
            fior = c.fetchone()

            #Set default eligibility value
            self.eligibility = "Eligible"

            #Get the details from entry boxes
            salary = int(Salary.get())
            
            loanamount = int(LoanAmount.get())

            extraamount = int(FixedObligations.get())

            tenure = int(LoanTenure.get())

            #Check Eligibility
            if(extraamount > 0):
                calculatedfior = (extraamount / salary) * 100 
                if (calculatedfior > int(fior[0])):
                    self.eligibility = "Not Eligible"

            calculatedamount = ( (int(fior[0])/100) * salary ) * tenure 
            if(calculatedamount < loanamount):
                self.eligibility = "Not Eligible"

            
            #Create Query label to display the eligibility value
            query_label = tk.Label(self, text= self.eligibility)
            query_label.place(relx = 0.51 , rely = 0.76, relwidth = 0.42, relheight = 0.05)


            #Commit changes
            conn.commit()

            #Close connection
            conn.close()

        #Create variable
        z = tk.StringVar()

        #Create Entry boxes
        CustomerID = tk.Entry(self, bg="grey")
        CustomerID.place(relx = 0.51, rely = 0.12, relwidth = 0.42, relheight = 0.05)

        LoanType = tk.Entry(self, bg = "grey", textvariable=z)
        LoanType.place(relx = 0.51, rely = 0.21, relwidth = 0.42, relheight = 0.05)

        LoanAmount = tk.Entry(self, bg = "grey")
        LoanAmount.place(relx = 0.51, rely = 0.3, relwidth = 0.42, relheight = 0.05)

        Salary = tk.Entry(self, bg="grey")
        Salary.place(relx = 0.51, rely = 0.39, relwidth = 0.42, relheight = 0.05)

        FixedObligations = tk.Entry(self, bg="grey")
        FixedObligations.place(relx = 0.51, rely = 0.48, relwidth = 0.42, relheight = 0.05)

        LoanTenure = tk.Entry(self, bg="grey")
        LoanTenure.place(relx = 0.51, rely = 0.57, relwidth = 0.42, relheight = 0.05)

        InterestRate = tk.Entry(self, bg="grey")
        InterestRate.place(relx = 0.51, rely = 0.66, relwidth = 0.42, relheight = 0.05)

        #Create Labels
        CustomerIDLabel = tk.Label(self, text = "Customer ID:")
        CustomerIDLabel.place(relx = 0.05 , rely = 0.12, relwidth = 0.42, relheight = 0.05)

        LoanTypeLabel = tk.Label(self, text = "Loan Type:")
        LoanTypeLabel.place(relx = 0.05 , rely = 0.21, relwidth = 0.42, relheight = 0.05)

        LoanAmountLabel = tk.Label(self, text = "Loan Amount:")
        LoanAmountLabel.place(relx = 0.05 , rely = 0.3, relwidth = 0.42, relheight = 0.05)

        SalaryLabel = tk.Label(self, text = "Salary:")
        SalaryLabel.place(relx = 0.05 , rely = 0.39, relwidth = 0.42, relheight = 0.05)

        FixedObligationsLabel = tk.Label(self, text = "Fixed Obligations:")
        FixedObligationsLabel.place(relx = 0.05 , rely = 0.48, relwidth = 0.42, relheight = 0.05)

        LoanTenureLabel = tk.Label(self, text = "Loan Tenure (Months):")
        LoanTenureLabel.place(relx = 0.05 , rely = 0.57, relwidth = 0.42, relheight = 0.05)

        InterestRateLabel = tk.Label(self, text = "Interest Rate(%):")
        InterestRateLabel.place(relx = 0.05 , rely = 0.66, relwidth = 0.42, relheight = 0.05)

        #Assigining validation to entry boxes 
        CustomerID.config(validate = 'key', validatecommand = (reg, '%P'))
        LoanAmount.config(validate = 'key', validatecommand = (reg, '%P'))
        Salary.config(validate = 'key', validatecommand = (reg, '%P'))
        FixedObligations.config(validate = 'key', validatecommand = (reg, '%P'))
        LoanTenure.config(validate = 'key', validatecommand = (reg, '%P'))
        InterestRate.config(validate = 'key', validatecommand = (reg, '%P'))

        #Create Query Button
        query_btn = tk.Button(self, text= "Check", command= query)
        query_btn.place(relx = 0.05 , rely = 0.76, relwidth = 0.42, relheight = 0.05)


        #Create Submit Button
        submit_btn = tk.Button(self, text = "Assign Loan to Customer", bg = "grey", command = submit)
        submit_btn.place(relx = 0.05 , rely = 0.87, relwidth = 0.5, relheight = 0.1)

        
        #Create Quit Button
        back_btn = tk.Button(self, text="Home", 
                            command=lambda: controller.show_frame(StartPage))
        back_btn.place(relx = 0.65 , rely = 0.87, relwidth = 0.3, relheight = 0.1)

app = main()

#commit changes
conn.commit()


#close connection
conn.close()
 
app.mainloop()