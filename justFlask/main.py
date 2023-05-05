import requests, random
from flask import Flask, request, jsonify, redirect
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})

# read user agents from file and cache it
@cache.memoize()
def get_user_agents():
    with open('user_agents.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

@app.route('/translate', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def translate():
    from_lang = request.args.get('from', 'en')
    to_lang = request.args.get('to', 'id')
    text = request.args.get('text', '')

    # set up headers
    headers = {
        'User-Agent': random.choice(get_user_agents()),
        'Referer': 'http://translate.google.com/',
        'Origin': 'http://translate.google.com/'
    }

    # send request to Google Translate API
    url = f'https://translate.google.com/translate_a/single?client=gtx&sl={from_lang}&tl={to_lang}&dt=t&q={text}'
    response = requests.get(url, headers=headers)

    # extract translated text from response
    result = response.json()
    if result is not None and len(result) > 0 and len(result[0]) > 0:
        translated_text = result[0][0][0]
    else:
        translated_text = 'Translation failed'

    # return result as JSON
    return jsonify({
        'code/status': response.status_code,
        'from': from_lang,
        'to': to_lang,
        'text': text,
        'user_agent': headers['User-Agent'],
        'translated_text': translated_text,
        'credits': 'Xnuvers007 ( https://github.com/xnuvers007 )'
    })

@app.errorhandler(404)
@app.errorhandler(500)
def handle_errors(error):
    return redirect('/translate?from=en&to=id&text=hello, im Xnuvers007, Im the developer')

@app.route('/')
def index():
    return redirect('/translate?from=en&to=id&text=hello, im Xnuvers007, Im the developer')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
