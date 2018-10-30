# Facebook-simple-bot

## requirements
- python3.6
- ngrok

## how to set up

### install packages
- in your python virtualenv

```sh
$ python install -r requirements.txt
```

###  generate random verify token

- in your python interactive interpretor
```python
import secrets
secrets.token_hex(nbytes=16)
```

- crate a json file name `.config.json`, and follow up the format below (you should fill up the value)
```
{
    "VERIFY_TOKEN": "",
    "PAGE_TOKEN": ""
}
```

### webhook with facebook

- run this application, default setting is binding the port `8000`
```sh
$ python app.py --debug
```

- use ngrok to get SSL, here set to bind the port `8000`
```sh
$ ./ngrok http 8000
```

- enter the verify token and SSL URL
    - note that `回呼網址` should enter the webhook router `https://ngrok.***.io/webhook`
- can check facebook [doc](https://developers.facebook.com/docs/messenger-platform/webhook)

### Subscribe your facebook page
- select your facebook page and generate page token

## LICENSE
MIT @ Kuoteng, 2018
