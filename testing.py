# import requests
# bitcoin_api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
# response = requests.get(bitcoin_api_url)
# response_json = response.json()
# print(response_json)
#
# print(response_json['time'])
# print(response_json['disclaimer'])
# print(response_json['chartName'])
# print(response_json['bpi']['USD']['rate'])
#
#
# print(type(response_json))  # The API returns a list

previous_price = 40000
price = 35000

print( str(round((1 - previous_price/price), 3)*100) + ' : percent change')



