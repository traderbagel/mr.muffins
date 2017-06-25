from flask import Flask, request
import json
import requests
import os 

app = Flask(__name__)

# Some python config method :
# https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b


DATABASE_CONFIG = {
	'channel_id':'1521764494', # UserID
    'channel_secret':'74c0cf68a0fd5fd6f1f68ca12c83c2f6', # UserSecrertKey
	'channel_MID':'Z6kGvct04yThOXOacWqg72dqExNO39KmKGmibbAQ2wN2yCbtnR6vx0Qq9MbCdUusC3CAsQSDcqRBEFDmO3qIImfdit5jsFV4CmcqmVViR0kSyR5ZugOB56Rhm1JKUOOkSkgPVncMfwJxBlB9up8qkwdB04t89/1O/w1cDnyilFU=' # MID
}

@app.route('/')
def index():
    return "<p>Hello World!</p>"

@app.route('/callback', methods=['POST'])
def callback():
    json_line = request.get_json()
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    user = decoded['result'][0]['content']['from']
    text = decoded['result'][0]['content']['text']
    #print(json_line)
    print("user:",user)
    print("content:",text)
    sendText(user,text)
    return ''

def sendText(user, text):
    LINE_API = 'https://trialbot-api.line.me/v1/events'
    CHANNEL_ID = DATABASE_CONFIG['channel_id']
    CHANNEL_SECRET = DATABASE_CONFIG['channel_secret']
    MID = DATABASE_CONFIG['channel_MID']

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Line-ChannelID': CHANNEL_ID,
        'X-Line-ChannelSecret': CHANNEL_SECRET,
        'X-Line-Trusted-User-With-ACL': MID
    }

    data = json.dumps({
        "to": [user],
        "toChannel":1383378250,
        "eventType":"138311608800106203",
        "content":{
            "contentType":1,
            "toType":1,
            "text":text
        }
    })

    r = requests.post(LINE_API, headers=headers, data=data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
