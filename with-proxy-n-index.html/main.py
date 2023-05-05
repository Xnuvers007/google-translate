import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/translate', methods=['GET'])
def translate():
    from_lang = request.args.get('from', 'en')
    to_lang = request.args.get('to', 'id')
    text = request.args.get('text', '')

    # set up headers and proxy
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'http://translate.google.com/',
        'Origin': 'http://translate.google.com/'
    }
    proxies = {
        'http': 'http://117.54.114.97:80',
        'https': 'http://20.93.42.101:8080'
    }

    # send request to Google Translate API
    url = f'https://translate.google.com/translate_a/single?client=gtx&sl={from_lang}&tl={to_lang}&dt=t&q={text}'
    response = requests.get(url, headers=headers, proxies=proxies)

    # extract translated text from response
    result = response.json()
    if result is not None and len(result) > 0 and len(result[0]) > 0:
        translated_text = result[0][0][0]
    else:
        translated_text = 'Translation failed'

    # return result as JSON
    return jsonify({
        'from': from_lang,
        'to': to_lang,
        'text': text,
        'translated_text': translated_text
    })


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True,
           host='0.0.0.0',
           port=80)

# app.run(host='0.0.0.0', port=81)
