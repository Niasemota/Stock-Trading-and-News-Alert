import requests
from twilio.rest import Client

stock_name = "TSLA"
company_name = "Tesla Inc"

#endppoints
stock_endpt = "https://www.alphavantage.co/query"
news_endpt = "https://newsapi.org/v2/everything"

#stock + news api keys
stock_api_key = "IKU1J0JYREWJB8R4"
news_api_key = "2c41af5c1e2849cb9fc952f9fe139ac1"
#twilio sid + auth token

# https://www.alphavantage.co/documentation/#daily
# When stock price +/- 5% b/w yesterday and day before --> print("Get News")

stock_params= {
    "function": "TIME_SERIES_DAILY",
    "symbol": stock_name,
    "apikey": stock_api_key,
}
response = requests.get(stock_endpt, params= stock_params )
data = response.json()["Time Series (Daily)"]
data_lst = [value for (key,value) in data.items()]
yesterday_data = data_lst[0]
yesterday_closing_price = yesterday_data["4. close"]
#print(yesterday_closing_price)

#day before yesterday's closing stock price
day_before_yesterday_data = data_lst[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
#print(day_before_yesterday_closing_price)

#find difference
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
#print(difference)

#find percent difference
diff_percent = round( (difference / float(yesterday_closing_price)) * 100)
#print(diff_percent)

#if % > 5% get news articles
if abs(diff_percent) > 5:
    news_params = {
        "apiKey":news_api_key,
        "qInTitle": company_name,
    }

    news_response = requests.get(news_endpt, params=news_params)
    articles = news_response.json()["articles"]
    #print(articles)

    #create list w first 3 articles
    #have headline + description
    three_articles = articles[:3]

    formatted_articles = [f" {stock_name} : {up_down} {diff_percent}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    #twilio to send messages
    #to send a separate message with each article's title and description to your phone number.

    client = Client (twilio_sid , twilio_auth_token)

    for article in formatted_articles:
        message = client.messages.create(
                body= article,
                from_='+14156049457',
                #insert your number here
                to='+11234567890'
            )

