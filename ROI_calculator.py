#Regex for commas in price, etch
#Edge cases (make sure no matter what user inputs it takes them somewhere)
#Method just for printing responses

import re
import pip._vendor.requests as requests

class ROI():

    def __init__(self, name, value, square_feet, units):
        self.name = name
        self.value = value 
        self.square_feet = square_feet
        self.units = units
        self.income = 0
        self.taxes = 0
        self.income = 0
        self.expense = 0
        self.a_cash_flow = 0
        self.mortgage_payment = 0
        self.hoa_value = 0
        self.roi = 0

    def income_value(self):
        
        rent_dict = {1.6: ['HI','CA'],
                    1.4: ['MD','NJ','MA','NY','CO','WA','AK',],
                    1: ['NH','CT','DE','VA','GA','FL','TX','IL','MN','AZ','UT','NV','OR','VT','RI','PA','NC',],
                    .8: ['ME','OH','MI','IN','SC','TN','WV','KY','AL','MS','AR','LA','OK','KS','MO','IA','WI','SD','NE','NM',
                        'WY', 'ND','MT','ID']}

        pattern = re.compile('[0-9]{5}')
        while True:
            address = input("What is the address of the property (city & zipcode)? ")
            zipcode = pattern.findall(address)
            if zipcode:
                zipcode = int(''.join(zipcode))
                r = requests.get(f"http://api.zippopotam.us/us/{zipcode}")
                if r.status_code == 200:
                    data = r.json()
                    break
                else:
                    print(f"Not a valid zipcode....please try again.")
                    continue
            else:
                print(f"Not a valid zipcode....please try again.")
                continue

        state_abr = data['places'][0]['state abbreviation']

        for rent, list in rent_dict.items():
            for state in list:
                if state == state_abr:
                    x = rent

    
        self.income = x * self.square_feet 
        print(self.income)
        
    def expense_value(self):
        self.taxes = (self.value * .08 * .045) / 12
        self.insurance = ((self.value * .96) * .01) / 12
        
        
        while True:
            hoa = input('Will you have Home Owners Insurance (y/n)? ')
            if hoa.lower() == 'y':
                if self.value <= 150000:
                    hoa_value = 808 /12
                    break
                elif self.value <= 300000:
                    hoa_value = 1015 /12
                    break
                else:
                    hoa_value = 1650 / 12
                    break
            elif hoa.lower() == 'n':
                hoa_value = 0
                break
            else:
                print("Not a valid response...please try again.")
                continue

        self.hoa_value = hoa_value

        vacancy = (self.value * .01) / 12
        repairs = self.units * 100 
        capex = 100
        pm = input('Will there be a Propery Manager (y/n)? ')
        pm_value = 0
        while True:
            pm = input('Will there be a Propery Manager (y/n)? ')
            if pm.lower() == 'y':
                pm_value = self.income * .1 
                break
            elif pm.lower() == 'n':
                pm_value = 0
                break
            else:
                print("Not a valid response...please try again.")
                continue

        pattern = re.compile('[\W]+')

        while True:
            loan_y = input('How many years are you looking to loan for (i.e 15, 30, etc)? ')
            loan_y = float(re.sub(pattern, '', loan_y))

            if loan_y > 0.0 and loan_y <= 30.0:
                break
            else:
                print('Not a valid input....please try again.')
                continue

        loan_m = loan_y * 12
        mortage = 1.0033**(0 - loan_m)
        self.mortage_payment = (.0033 / (1 - mortage)) * self.value
    
        self.expense = self.taxes + self.insurance + hoa_value + vacancy + repairs + capex + pm_value + self.mortage_payment
        
    def cash_on_cash(self):
        self.a_cash_flow = (self.income - self.expense) * 12
        pattern = re.compile('[\W]+')
        while True:
            dp = input('How much down payment will you be putting on the property (i.e. 20%, 30%)? ')
            dp = float(re.sub(pattern, '', dp))
            if dp > 0.0 and dp <= 100.0:
                break
            else:
                print('Not a valid input....please try again.')
                continue

        down_payment = (dp/100) * self.value
        closing = self.value * .05
        
        while True:
            response = input('Are you anticating any rehab of the property (y/n)? ')
            if response.lower() == 'y':
                rehab = input('Will it be light rehab (l), medium rehab (m), or heavy rehab(h) or not quite sure (n)? ')
                if rehab.lower() == 'l':
                    rehab_value = self.value * .05
                    break
                elif rehab.lower() == 'm' or rehab.lower() == 'n':
                    rehab_value = self.value * .1
                    break
                elif rehab.lower() == 'h':
                    rehab_value = self.value * .15
                    break
                else:
                    print("Not a valid response...please try again.")
                    continue
                
            if response.lower() == 'n':
                rehab_value = 0
                break

            else: 
                print("Not a valid response...please try again.")
                continue


        investment = down_payment + closing + rehab_value
        self.roi = (self.a_cash_flow / investment) * 100

    def printInfo(self):

        format_roi = "{:.2f}".format(self.roi)
        format_mortage = "{:.2f}".format(self.mortage_payment) 
        format_income = "{:.2f}".format(self.income)
        format_taxes = "{:.2f}".format(self.taxes)
        format_insurance = "{:.2f}".format(self.insurance)
        format_expense = "{:.2f}".format(self.expense)
        format_cashflow = "{:.2f}".format(self.a_cash_flow)
        format_hoa = "{:.2f}".format(self.hoa_value)

        print(f"Thank you {self.name.title()} for your input. We are finished calculating your ROI.") 
        print("Based on our calculations here's what we got for you:")
        print(f"""\n\tTotal Monthly Income............${format_income}
        Total Monthly Expenses..........${format_expense}
        Total Annual Cashflow...........${format_cashflow}
        TOTAL ROI.......................{format_roi}%""")

        print("\nBased on your inputs & location we've calculated some other rough estimates for you:")
        print(f"""\n\tMonthly Mortgage Payment........${format_mortage}
        Monthly HOA Payment.............${format_hoa}
        Monthly Tax Payment.............${format_taxes}
        Monthly Insurance Payment.......${format_insurance}
        **mortage based on a 4.5% interest rate**""")

        print("\n\t*These calculations are based on averages for your area. Please consult with a professional.")

alex_property = ROI('alex', 50000, 1000, 1)

def run():
    print("""\nHi! We are here to help you calculate your properties potential ROI (Return on Investment)!
We're also here to help give you some insights into other monthly/annual costs like mortage & HOA!
Let's get started with some questions...""")
    name = input('\nWhat is your name? ')
    print(f"Hi {name.title()}")

    pattern = re.compile('[0-9]+[\.]?[0-9]{2}?')
    while True:
        value = input("\nWhat is the value of the property you are looking at? ")
        value = value.replace('$','').replace(',','')
        match_v = pattern.search(value)
        if not match_v:
            print("Not a valid entry...try again.")
            continue
        else:
            break
        
    while True:
        square_feet = input("What is the square footage of the property? ")
        square_feet = square_feet.replace('$','').replace(',','')
        match_r = pattern.search(square_feet)
        if not match_r:
            print("Not a valid entry...try again.")
            continue
        else:
            break
    
    units = int(input("How many rental units will the property have? "))
    alex_property = ROI(name,float(value), float(square_feet), units)
    alex_property.income_value()
    alex_property.expense_value()
    alex_property.cash_on_cash()
    alex_property.printInfo()


run()