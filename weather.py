# Download the helper library from https://www.twilio.com/docs/python/install
import requests
import datetime
from twilio.rest import Client

account_sid = "AC4f9352b42cc8e58c70178c4b1a053399"
auth_token = "3fd87896a2b7e047bdb2f30a5f899d20"


endpoint = "https://api.openweathermap.org/data/3.0/onecall?"
api_key = '86e96866ad99c4279b5cbcfeca0e368e'
exclude = '&units=imperial&exclude=minutely,hourly'
applyid = '&appid='+api_key
parameters = {'Boston':'lat=42.36&lon=-71.18', 'Okemo': 'lat=43.397240&lon=-72.709969', 'MountSnow':'lat=42.967030&lon=-72.921402','Stowe':'lat=44.465340&lon=-72.684303', 'Sunapee': 'lat=43.321190&lon=-72.036340'}
weekday_name ={0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}

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
