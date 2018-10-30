import argparse
import json
import sys
import requests
from flask import Flask, request, abort, jsonify

with open(".config.json") as _:
    secrets = json.loads(_.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Should set the {} enviroment variable".format(setting)
        print(error_msg)
        sys.exit(1)

VERIFY_TOKEN = get_secret('VERIFY_TOKEN')
PAGE_TOKEN = get_secret('PAGE_TOKEN')

app = Flask(__name__)
app.config['ENV'] = 'development'
send_api = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=PAGE_TOKEN)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        mode = request.args['hub.mode']
        token = request.args['hub.verify_token']
        challenge = request.args['hub.challenge']
        if mode and token:
            if mode == 'subscribe' and  token == VERIFY_TOKEN:
                return (challenge, 200)
        else:
            abort(403)
    if request.method == 'POST':
        req_data = request.get_json()
        if req_data['object'] == 'page':
            for entry in req_data['entry']:
                for message in entry['messaging']:
                    if message.get('message', '') == '':
                        continue
                    res_msg = {
                        'recipient': {
                            'id': message['sender']['id']
                        },
                        'message': {
                            "text": message['message']['text']
                        },
                        'messaging_type': 'RESPONSE'
                    }
                    req = requests.post(send_api,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(res_msg)
                    )
                    return 'OK'
            abort(403)
        else:
            abort(404)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=8000, type=int)
    parser.add_argument('--debug', default=False, action='store_true')
    args = parser.parse_args()
    app.run(debug=args.debug,port=args.port)
