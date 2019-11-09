import requests
import asyncio
import json


def stock_lookup(stock):
    url_for_json = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics&corsDomain=finance.yahoo.com".format(
        stock)
    details_from_json = requests.get(url_for_json)
    try:
        importedfile = json.loads(details_from_json.text)
        print(stock + '\'s current price is', end=" $")
        print(importedfile['quoteSummary']['result'][0]['financialData']['currentPrice']['raw'], end="")
        print('USD')
        return str((importedfile['quoteSummary']['result'][0]['financialData']['currentPrice']['raw']))
    except:
        print("Failed to parse json response or incorrect stock symbol")
        return {"error": "Incorrect stock symbol or could not parse json"}


def stock_name(msg):
    url_for_json = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={0}&region=1&lang=en'.format(msg)
    details_from_json = requests.get(url_for_json)
    try:
        importedfile = json.loads(details_from_json.text)
        return str(importedfile["ResultSet"]["Result"][0]["name"])
    except:
        return {"error": "Incorrect stock symbol"}