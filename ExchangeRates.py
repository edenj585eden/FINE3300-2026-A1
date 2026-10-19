class ExchangeRates:
    def __init__(self, filename): 
        #Using __init__() to initialize 
        self.filename = filename
        self.exchange_rate = self.read_exchange_rate()

    def read_exchange_rate(self):
        #Opening and reading the excel file
        file = open(self.filename, "r")
        data = file.read().split("\n") #Each line return (aka each row) is seperated by \n, so splitting by \n makes each row a new list
        file.close() #Close the file after reading!

        #Removing the empty item that can appear at the end when splitting by "\n".
        if data[-1] == "":
            data.pop()

        headers = data[0].split(",") #Split the 1st spot on the list, which is the header row, into another list by the commas.

        #Find the position of the FXAUSDCAD column using a for loop and if statement.
        rate_column = 0
        column_number = 0

        for heading in headers: #This will loop through each heading in the list of headers until it finds the FXAUSDCAD column.
            if heading == "FXAUSDCAD":
                rate_column = column_number

            column_number = column_number + 1

        #This takes the last row (which is the last index, aka it has an index of -1, on the data list) and makes it a list by splitting at the commas. We need this since we're using the latest rates.
        latest_row = data[-1].split(",")

        #This finds the exchange rate were looking for by looking in the new list we made of the last row for the index of the rate we need (found by the loop earlier).
        exchange_rate = float(latest_row[rate_column]) #We need to add float since it everything is being read as a string

        return exchange_rate #Return the exchange rate we found to use in the convert method.

    def convert(self, amount, fromCurrency, toCurrency): #This method converts an amount from one currency to another.

        #Use if statements to include the different scenarios of conversions
        if fromCurrency == toCurrency:
            return amount #If both currencies are the same, it returns the amount inputted

        elif fromCurrency == "CAD" and toCurrency == "USD":
            return amount / self.exchange_rate #Exchanging from CAD to USD, divides CAD by exchange rate to get USD

        elif fromCurrency == "USD" and toCurrency == "CAD":
            return amount * self.exchange_rate #Exchanging from USD to CAD, multiplys USD by exchange rate to get CAD


# Python 4: Creating an object from the class
exchange = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")

#Prompt the user for the amount and currencies
amount = float(input("Enter the amount: "))
from_currency = input("What is the currency you want to convert from (USD or CAD): ").upper()
to_currency = input("What is the currency you want to convert to (USD or CAD): ").upper()

#Calls the convert method
result = exchange.convert(amount, from_currency, to_currency)

#Formats the output using .format() based on what the user enters and what the convert method calculates.
print("${:.2f} {} = ${:.2f} {}".format(amount, from_currency, result, to_currency))
