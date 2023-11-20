# Download the helper library from https://www.twilio.com/docs/python/install
import requests
import datetime
from twilio.rest import Client


def get_weather_daily():
    try:
        message_body =""
        for key, value in parameters.items():
            url = endpoint + value + exclude + applyid
            #print(url)
            response = requests.get(url)
            message_body += '\n' + key +': \n' 
            if response.status_code == 200:
                data = response.json() 
                for i in range(3):
                    
                    this_day = data["daily"][i]
                    unix_time = this_day["dt"]
                    utc_time = datetime.datetime.fromtimestamp(unix_time).replace(tzinfo=datetime.timezone.utc)
                    date = utc_time.date()
                    weekday = utc_time.weekday()
                    temp = this_day["temp"]["day"]
                    summary = this_day["summary"]
                    weather = this_day["weather"][0]["main"]
                    rain = ''
                    snow = ''
                    if "rain" in this_day:
                        rain = str(this_day["rain"]) + ' mm'
                    if "snow" in this_day:
                        snow = str(this_day["snow"]) + ' mm'

                    text = date.strftime('%Y-%m-%d') + ' ' + weekday_name[weekday] + ":" + weather + ' ' + str(temp) + "F, Summary: " + summary
                    if len(rain) > 0:
                        text += ", Rain: " + rain
                    if len(snow) > 0:
                        text += ", Snow: " + snow

                
                    print(text)
                    message_body += text + '\n'
                        
            else: 
                print("Request failed")

        #send message
        send_SMS(message_body)

    except Exception as e:
        print(e)
        print("something is wrong!")

def send_SMS(msg_body):
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                    body=msg_body,
                    from_='+18556205219',
                    to='+14126166276'
                )
    message = client.messages \
                .create(
                    body=msg_body,
                    from_='+18556205219',
                    to='+12182820248'
                )
    print(message.sid)

if __name__ == "__main__":
    get_weather_daily()
