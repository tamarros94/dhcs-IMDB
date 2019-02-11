import pandas as pd
import regex as regex
import PyCurrency_Converter
from currency_converter import CurrencyConverter

c = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')


def convert_currency(budget):
    currency = regex.findall(r'\p{Sc}', budget)
    if len(currency) == 0:
        if budget == "Unknown":
            return "Unknown"
        currency = budget.split(' ')[0]
    else:
        if currency[0] == '$':
            currency = 'USD'
        if currency[0] == '€':
            currency = 'EUR'
        if currency[0] == '£':
            currency = 'GBP'
    amount = ''.join(i for i in budget if i.isdigit())
    print(budget)
    print(currency)
    print(amount)
    if currency != 'USD' and currency != 'FRF' and currency != 'DEM':
        new_amount = c.convert(int(amount), currency, 'USD')
        print("converted amount: " + str(new_amount) + "\n")
        return new_amount
    else:
        print("\n")
        if currency == 'USD':
            return amount
        else:
            return budget
