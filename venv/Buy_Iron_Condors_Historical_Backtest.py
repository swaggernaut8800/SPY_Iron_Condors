import pandas as pd
import xlsxwriter
import datetime
import os

class Week:
    def __init__(self, open, close, beginning_date, ending_date):
        self.open = open
        self.close = close
        self.beginning_date = beginning_date
        self.ending_date = ending_date
        self.buy_put_strike = open * (1 - testing_rate)
        self.sell_put_strike = self.buy_put_strike - testing_width
        self.buy_call_strike = open * (1 + testing_rate)
        self.sell_call_strike = self.buy_call_strike + testing_width

        if close >= self.buy_put_strike and close <= self.buy_call_strike:
            self.profit = -testing_premium  * 100 * num_contracts
        elif close > self.buy_call_strike and close < self.sell_call_strike:
            self.profit = ((close - self.buy_call_strike) - testing_premium) * 100 * num_contracts
        elif close < self.buy_put_strike and close > self.sell_put_strike:
            self.profit = ((self.buy_put_strike - close) - testing_premium) * 100 * num_contracts
        elif close > self.sell_call_strike or close < self.sell_put_strike:
            self.profit = (testing_width - testing_premium) * 100 * num_contracts
        else:
            raise Exception("Something went horribly wrong...")



first_year = int(input("Enter the beginning year: "))
last_year = int(input("Enter the last year: "))
testing_years = range(first_year, last_year + 1)
testing_rate = float(input("Enter the testing percentage: "))
testing_premium = float(input("Enter the testing premium: "))
testing_width = float(input("Enter the testing width: "))
num_contracts = int(input("Enter the number of contracts: "))

weeks_list = []
for file in os.listdir('data'):
    df = pd.read_csv(f'data/{file}')
    new_week = True
    for i in range(1, len(df.index)):
        if int(df['Date'][i].split('-')[0]) in testing_years:
            current_date = datetime.date(int(df['Date'][i].split('-')[0]), int(df['Date'][i].split('-')[1]),
                                         int(df['Date'][i].split('-')[2]))
            next_date = datetime.date(int(df['Date'][i + 1].split('-')[0]), int(df['Date'][i + 1].split('-')[1]),
                                         int(df['Date'][i + 1].split('-')[2]))
            if new_week == True:
                new_week = False
                first_open = float(df['Open'][i])
                beginning_date = current_date
            elif next_date - current_date >= datetime.timedelta(days=3):
                weeks_list.append(Week(first_open, float(df['Close'][i]), beginning_date, current_date))
                new_week = True

total_profit = 0
print('Buisness Weeks\n')
for week in weeks_list:
    total_profit += week.profit
    print(f'Beginning Date: {week.beginning_date}')
    print(f'Ending Date: {week.ending_date}\n')

print(f'${total_profit:,.2f}')