# Author Jason Hellums
# 20 Aug 2022
# adapted from previous weeks to report investor information, stock 
# and bond profolio, Reads .csv to collect bond and stock data and creates 
# a database of the investors holdings. Display graph of invsetor stock history. 

import random
import sqlite3
import string
from tkinter import Tk, filedialog

# Investor Class responsible for reporting investor information.
class Investor:
    newId = ''.join(random.choice(string.digits) for _ in range(8))
    def __init__(self, firstName, lastName, address, phoneNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.phoneNumber = phoneNumber
        self.investorId =str(Investor.newId)
    
    def CreateInvestorTable(db):
        # connect to Db
        dbExists = os.path.exists(db)
        if dbExists == False:    
            conn = sqlite3.connect(db)

            c = conn.cursor()

            # create table
            c.execute("""CREATE TABLE IF NOT EXISTS investorTable (
                firstName TEXT, 
                lastName TEXT, 
                address TEXT,
                phoneNumber TEXT,
                investorId TEXT
                )""")
            
            # Commit out command
            conn.commit()

            # close the connection 
            conn.close()
        else:
            print("Database already exists")


    def WriteToInvestorTable(self, db):
        # connect to Db
        conn = sqlite3.connect(db)

        # write to table
        c = conn.cursor()

        c.execute("INSERT INTO investorTable VALUES (?, ?, ?, ?, ?)",(self.firstName, 
            self.lastName,
            self.address,
            self.phoneNumber,
            self.investorId)
            )

        # Commit out command
        conn.commit()

        # close the connection 
        conn.close()

    # write investor header to file
    def InvestorHeaderFile(fileName):
        fileName.write(('-' * 97) + '\n')
        fileName.write('\tInvestor \tID number \tPhone Number \t\tAddress\n')
        fileName.write(('-' * 97) + '\n')
    # write investor data to file
    def InvestorDataFile(self, fileName):
        fileName.write('\t' + self.firstName + ' ' + self.lastName + '\t' + self.investorId + '\t' + self.phoneNumber + '\t' + self.address + '\n')

    # write investor header to terminal
    def InvestorHeader():
        print(('-' * 100) + '\n')
        print('| Investor \tID number \tPhone Number \t\tAddress\n')
        print(('-' * 100) + '\n')

    # write investor data to terminal
    def InvestorData(self, db, tableName):
        # connect to db
        conn = sqlite3.connect(db)

        # create cursor
        c = conn.cursor()

        # Query
        c.execute(f"SELECT * FROM {tableName} WHERE investorId =?", (self.investorId,))
        items = c.fetchall()
        for row in items:
            print(' ' + row[0] + ' ' + row[1] + '\t' + str(row[4]) + '\t' + str(row[3]) + '\t\t' + str(row[2]) + '\n')    
            print(('-' * 100) + '\n')
        # commit command
        conn.commit()

        # close connection
        conn.close()


# Stock Class responsible for storing and calculating stock information as well as outputs
class Stock:
    newId = ''.join(random.choice(string.digits) for _ in range(8))
    def __init__(self, symbol, quanity, purchasePrice, currentPrice, purchaseDate):
        self.symbol = symbol
        self.quanity = int(quanity)
        self.purchasePrice = float(purchasePrice)
        self.currentPrice = float(currentPrice)
        self.purchaseDate = purchaseDate
        self.purchaseId = str(Stock.newId)
    
    def CreateStockTable(db):
        # connect to Db
        conn = sqlite3.connect(db)

        c = conn.cursor()

        # create table
        c.execute("""CREATE TABLE IF NOT EXISTS stockTable (
            symbol DATATYPE, 
            quanity DATATYPE, 
            purchasePrice DATATYPE,
            currentPrice DATATYPE,
            purchaseDate DATATYPE,
            calcEarn DATATYPE,
            calcYearlyEarning DATATYPE,
            purchaseId DATATYPE,
            investorId DATATYPE
         )""")

        # Commit command 
        conn.commit()

        # Close connection 
        conn.close()


    def GetStockData(stockFile):
        import datetime as dt
        
        stockList = []
        try:
            with open(stockFile, 'r') as ReadFile:
                lines = ReadFile.readlines()
        except:
            print('File did not open or does not exist ' + stockFile)
            sys.exit()

        try:
            for line in lines:
                if line.split(',')[0].upper() == 'SYMBOL':
                    continue
                else:
                    date1 = dt.datetime.today()
                    date2 = dt.datetime.strptime(line.split(',')[4].replace('\n', ''), '%m/%d/%Y')
                    days = int((date1 - date2).days)
                    stockList.append([line.split(',')[0],
                    line.split(',')[1],
                    line.split(',')[2],
                    line.split(',')[3],
                    line.split(',')[4].replace('\n', ''),
                    round((float(line.split(',')[3]) - float(line.split(',')[2])) * float(line.split(',')[1]), 2),
                    round(((float(line.split(',')[3]) - float(line.split(',')[2]))/float(line.split(',')[2])/days)*100, 2)
                    ])
            
            return stockList

        except:
            print('Data could not be read from ' + stockFile)
            sys.exit()


    def calcYearlyEarning(self):
        import datetime as dt
        date1 = dt.datetime.today()
        date2 = dt.datetime.strptime(self.purchaseDate, '%m/%d/%Y')
        days = int((date1 - date2).days)
        CalcYear = ((self.currentPrice - self.purchasePrice)/self.purchasePrice/days)*100
        return str(round(CalcYear, 2)) + "%"

    def calcEarn(self):
        calcEarning = (self.currentPrice - self.purchasePrice) * self.quanity
        return round(calcEarning, 2)

    def StockHeaderFile(fileName):
        fileName.write(('-' * 89) + '\n')
        fileName.write('|\tStock Symb \t\tShares \t\tEarnings \tYearly Earnings \t|\n')
        fileName.write(('-' * 89) + '\n')

    def StockReportFile(self, fileName):
        fileName.write(('-' * 89) + '\n')
        fileName.write('|\t' + self.symbol + '\t\t\t' + str(self.quanity) + '\t\t$' + str("{:.2f}".format(Stock.calcEarn(self))) + '\t\t' + str(Stock.calcYearlyEarning(self)) + '\t\t|\n')
        fileName.write(('-' * 89) + '\n')

    def StockHeader():
        print(('-' * 89) + '\n')
        print('| Stock Symb \tShares \t\tEarnings \tYearly Earnings \n')
        print(('-' * 89) + '\n')

    def StockWriteToDb(stockList, db, tableName, investor):
        # connect to Db
        conn = sqlite3.connect(db)

        c = conn.cursor()

        # add in investor ID
        for item in stockList:
            newId = ''.join(random.choice(string.digits) for _ in range(8))
            item.append(newId)
            item.append(investor.investorId)

        # add list to bond DB table
        c.executemany(f"INSERT INTO {tableName} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", stockList)

        # commit command
        conn.commit()
        
        # close Db 
        conn.close()


    def StockReport(db, tableName, investor):
        # connect to db
        conn = sqlite3.connect(db)

        # create cursor
        c = conn.cursor()

        # Query
        c.execute(f"SELECT * FROM {tableName} WHERE investorId=?", (investor.investorId,))
        items = c.fetchall()
        for row in items:
            # print(('-' * 89) + '\n')
            if len(str(row[5])) >= 7:
                print(' ' + row[0] +  '\t\t' + str(row[1]) + '\t\t$' + str(row[5]) + '\t\t' + str(row[6]) + '\n')
            else:
                print(' ' + row[0] +  '\t\t' + str(row[1]) + '\t\t$' + str(row[5]) + '\t\t\t' + str(row[6]) + '\n')    
            print(('-' * 89) + '\n')
        # commit command
        conn.commit()

        # close connection
        conn.close()
        

    def IndividualStockInfo(db, tableName, investor, symbol):
        # connect to db
        conn = sqlite3.connect(db)

        # create cursor
        c = conn.cursor()

        # Query
        try:
            c.execute(f"SELECT * FROM {tableName} WHERE investorId=? AND symbol=?", (investor.investorId, symbol))
            items = c.fetchall()
            for row in items:
                return row[1]
            # commit command
            conn.commit()

            # close connection
            conn.close()
        except:
            print('Failed to find record')

    def StockGraph(db, tableName, investor, dataFile, output):
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        from matplotlib import rcParams
        import json
        import datetime as dt

        with open(dataFile,'r') as graphFile:
            data = json.load(graphFile)

        DateList = [x['Date'] for x in data]
        uniqueDateList = []
        for date in DateList:
            if str(date) in uniqueDateList:
                continue
            else:
                uniqueDateList.append(date)

        stockList = [x["Symbol"] for x in data]

        uniqueStockList = []
        for stock in stockList:
            if stock in uniqueStockList:
                continue
            else:
                uniqueStockList.append(stock) 

        StockDic = {}
        for i in range(0, len(uniqueStockList)):
            StockDic.update({uniqueStockList[i] :
                {"Close" : [],
                "OwnerValue" : [],
                "Quantity": Stock.IndividualStockInfo(db, tableName, investor, uniqueStockList[i]), 
                "DateList" : []}})
            DateCount = []
            for y in uniqueDateList:
                DateCount.append(y)
                for x in data:
                    if str(x["Symbol"]) == str(uniqueStockList[i]):
                        StockDic[uniqueStockList[i]]["name"] = x["Symbol"]
                        if str(y) == str(x["Date"]):
                            StockDic[uniqueStockList[i]]["Close"].append(x["Close"])
                            StockDic[uniqueStockList[i]]["OwnerValue"].append(x["Close"] * StockDic[uniqueStockList[i]]["Quantity"])
                            StockDic[uniqueStockList[i]]["DateList"].append(dt.datetime.strptime(x["Date"], '%d-%b-%y'))
                        else:
                            continue
                    else:
                        continue               
        plt.figure(figsize=(9.0, 5.0))               
        for st in uniqueStockList:
            plt.plot(StockDic[st]["DateList"], StockDic[st]["OwnerValue"], label= StockDic[st])
        plt.legend(uniqueStockList)
        
        plt.title('Invertor Stock History')
        plt.xlabel('Date')
        plt.ylabel('Stock Value')
        plt.savefig(output) 
        plt.show()               


# Bond Class responsible for storing and presenting outputs. Inherits from Stocks
class Bond(Stock):
    newId = ''.join(random.choice(string.digits) for _ in range(8))

    def __init__(self, symbol, quantity, purchasePrice, currentPrice, purchaseDate, coupon, bondYield):
        super().__init__(symbol, quantity, purchasePrice, currentPrice, purchaseDate)
        self.coupon = coupon
        self.bondYield = bondYield
        self.purchaseId = str(Bond.newId)

    def GetBondData(bondFile):
        bondList = []
        try:
            with open(bondFile, 'r') as ReadFile:
                lines = ReadFile.readlines()
        except:
            print('File did not open or does not exist')
            sys.exit()

        try:
            for line in lines:
                if line.split(',')[0].upper() == 'SYMBOL':
                    continue
                else:
                    bondList.append([line.split(',')[0],
                    line.split(',')[1],
                    line.split(',')[2],
                    line.split(',')[3],
                    line.split(',')[4],
                    line.split(',')[5],
                    line.split(',')[6].replace('\n', '')])
            
            return bondList

        except:
            print('Data could not be read')
            sys.exit()

    def CreateBondTable(db):
        # connect to Db
        conn = sqlite3.connect(db)

        c = conn.cursor()

        # create table
        c.execute("""CREATE TABLE IF NOT EXISTS bondTable (
            symbol DATATYPE, 
            quanity DATATYPE, 
            purchasePrice DATATYPE,
            currentPrice DATATYPE,
            purchaseDate DATATYPE,
            coupon DATATYPE,
            bondYield DATATYPE,
            purchaceId DATATYPE,
            investorId DATATYPE
         )""")

        # Commit command 
        conn.commit()

        # Close connection 
        conn.close()

    def writeToDb(db, tableName, bondList, investor):
        # connect to Db
        conn = sqlite3.connect(db)

        c = conn.cursor()

        # add in investor ID
        for item in bondList:
            item.append(Bond.newId)
            item.append(investor.investorId)

        # add list to bond DB table
        c.executemany(f"INSERT INTO {tableName} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", bondList)

        # commit command
        conn.commit()
        
        # close Db 
        conn.close()

    def BondHeaderFile(fileName):
        fileName.write(('-' * 113) + '\n')
        fileName.write('|\tBond Symb \tQuantity \tPurchase Price \tCurrent Price \tPurchase Date \tCoupon \tYield \tBond Id\t|\n')
        fileName.write(('-' * 113) + '\n')

    def BondDataFile(self, fileName):
        fileName.write(('-' * 113) + '\n')
        fileName.write('|\t' + self.symbol + '\t\t' + str(self.quanity) + '\t\t' + str(self.purchasePrice) + '\t\t' + str(self.currentPrice) + '\t\t' + str(self.purchaseDate) + '\t' + str(self.coupon) + '\t' + str(self.bondYield) + '\t' + str(self.purchaseId) + '|\n')
        fileName.write(('-' * 113) + '\n')

    def BondHeader():
        print(('-' * 113) + '\n')
        print('| Bond Symb   Quantity   Purchase Price  Current Price   Purchase Date   Coupon   Yield   Bond Id\n')
        print(('-' * 113) + '\n')

    def BondData(db, tableName, investor):
        # connect to db
        conn = sqlite3.connect(db)

        # create cursor
        c = conn.cursor()

        # Query
        c.execute(f"SELECT * FROM {tableName} WHERE investorId=?", (investor.investorId,))
        items = c.fetchall()
        for row in items:
            #print('{0}.ljust(14) + {1}.ljust(24) + {2}.ljust{3:39}{4:54}{5:69}{6:77}{7:84}'.format(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7])))
            print(row[0].ljust(14) + str(row[1]).ljust(11) + str(row[2]).ljust(16)  + str(row[3]).ljust(16) + str(row[4]).ljust(16) + str(row[5]).ljust(9) + str(row[6]).ljust(8) + str(row[7])  + '\n')    
            print(('-' * 113) + '\n')
        # commit command
        conn.commit()

        # close connection
        conn.close()

    

def lineBreakFile(number, fileName):
    fileName.write(('-' * number) + '\n')

def lineBreak(number):
    print(('-' * number) + '\n')


def GUI():

    def getStockFile(entry, fileType, fileExtention):
        filename =filedialog.askopenfilename(filetypes=((fileType + " files","*." + fileExtention),))
        entry.insert(END, filename)
        
    def to_raw(string):
        return fr"{string}"

    def execution(firtNameInput, LastNameInput, AddressInput, CityInput, StateInput, zipInput, phoneInput, stockFileInput, stockJsonInput, dbLocOutputInput, stockGraphInput):
        # execution outputs
        db = str(dbLocOutputInput)
        output = str(stockGraphInput)
        # Stock inputs
        stocks = stockFileInput
        dataFile = str(stockJsonInput)

            
        # Investor inputs
        investor1 = Investor(firtNameInput, LastNameInput, str(AddressInput) + ', ' + str(CityInput) + ", " + str(StateInput) + " " +  str(zipInput), str(phoneInput))

        # Create Investor table
        Investor.CreateInvestorTable(db)
        # Investor heading and outputs
        investor1.WriteToInvestorTable(db)
        # investor1.InvestorData(db, 'investorTable')


        # Stock
        Stock.CreateStockTable(db)

        stockList = Stock.GetStockData(to_raw(stocks))

        Stock.StockWriteToDb(stockList, db, 'stockTable', investor1)

        Stock.StockGraph(db, 'stockTable', investor1, dataFile, output)


        sys.exit()



    root = Tk()
    root.geometry("700x500")
    firstNameLabel = Label(root, text="First Name:", justify=LEFT)
    firstNameLabel.grid(sticky= 'w', row=1, column=0)
    firstNameInput = Entry(root, width=50, borderwidth=5, justify=LEFT)
    firstNameInput.grid(sticky= 'w', row=1, column=1)
    lastNameLabel = Label(root, text="Last Name:", justify=LEFT)
    lastNameLabel.grid(sticky= 'w', row=2, column=0)
    lastNameInput = Entry(root, width=50, borderwidth=5, justify=LEFT)
    lastNameInput.grid(sticky= 'w', row=2, column=1)
    streetAddressLabel = Label(root, text="Street Address: ", justify=LEFT)
    streetAddressLabel.grid(sticky= 'w', row=3, column=0)
    streetAddressInput = Entry(root, width=50, borderwidth=5, justify=LEFT)
    streetAddressInput.grid(sticky= 'w', row=3, column=1)
    cityLabel = Label(root, text="City:", justify=LEFT)
    cityLabel.grid(sticky= 'w', row=4, column=0)
    cityInput = Entry(root, width=50, borderwidth=5, justify=LEFT)
    cityInput.grid(sticky= 'w', row=4, column=1)
    stateLabel = Label(root, text="ST:", justify=LEFT)
    stateLabel.grid(sticky= 'w', row=5, column=0)
    stateInput = Entry(root, width=5, borderwidth=5, justify=LEFT)
    stateInput.grid(sticky= 'w', row=5, column=1)
    zipLabel = Label(root, text="zipcode:", justify=LEFT)
    zipLabel.grid(sticky= 'w', row=6, column=0)
    zipInput = Entry(root, width=10, borderwidth=5, justify=LEFT)
    zipInput.grid(sticky= 'w', row=6, column=1, )
    phoneNumLabel = Label(root, text="Phone Number:", justify=LEFT)
    phoneNumLabel.grid(sticky= 'w', row=7, column=0)
    phoneNumInput = Entry(root, width=12, borderwidth=5, justify=LEFT)
    phoneNumInput.grid(sticky= 'w', row=7, column=1)
    

    stockFileLabel = Label(root, text="Stock File:", justify=LEFT)
    stockFileLabel.grid(sticky= 'w', row=8, column=0)
    stockFileInputB = Button(root, text="Browse Stock File", command=lambda: getStockFile(stockFileInput,
                                                                                                'text',
                                                                                                'csv'))
    stockFileInputB.grid(sticky= 'w', row=8, column=2)
    stockFileInput = Entry(root, width= 50, borderwidth= 5, justify=LEFT)
    stockFileInput.grid(sticky= 'w', row=8, column=1)
    
    stockJsonLabel = Label(root, text="Stock JSON File:", justify=LEFT)
    stockJsonLabel.grid(sticky= 'w', row=9, column=0)
    stockJsonInput = Entry(root, width=50, borderwidth=5, justify=LEFT)
    stockJsonInput.grid(sticky= 'w', row=9, column=1)
    stockJsonInputB = Button(root, text="Browse Stock JSON File", command=lambda: getStockFile(stockJsonInput,
                                                                                                'All',
                                                                                                'json'))
    stockJsonInputB.grid(sticky= 'w', row=9, column=2)

    dbLocOutputLabel = Label(root, text="Database Name:", justify=LEFT)
    dbLocOutputLabel.grid(sticky= 'w', row=10, column=0)
    dbLocOutputInput = Entry(root, width=50, borderwidth=5, justify=LEFT)
    dbLocOutputInput.grid(sticky= 'w', row=10, column=1)
    dbLocOutputInputB = Button(root, text="Browse database File", command=lambda: getStockFile(dbLocOutputInput,
                                                                                                'All',
                                                                                                'db'))
    dbLocOutputInputB.grid(sticky= 'w', row=10, column=2)

    
    stockGraphLabel = Label(root, text="Stock Graph Path:", justify=LEFT)
    stockGraphLabel.grid(sticky= 'w', row=11, column=0)
    stockGraphInput = Entry(root, width=50, borderwidth=5, justify=LEFT)
    stockGraphInput.grid(sticky= 'w', row=11, column=1)



    submitButton = Button(root, text="Submit", width=25, height=3, background="green", font=18, fg="white", 
    command=lambda: execution(firstNameInput.get(), 
                    lastNameInput.get(), 
                    streetAddressInput.get(), 
                    cityInput.get(), 
                    stateInput.get(), 
                    zipInput.get(),
                    phoneNumInput.get(), 
                    stockFileInput.get(), 
                    stockJsonInput.get(), 
                    dbLocOutputInput.get(), 
                    stockGraphInput.get()))
    submitButton.grid(row=20, column=1)
    closeButton = Button(root, text="Close", width=25, height=3, background="Red", font=18, command= root.destroy)
    closeButton.grid(row=21, column=1)
    root.mainloop()



# Main body 
# imports 
import sqlite3
import sys, os
import matplotlib
from tkinter import *


GUI()