import requests
from flask import Flask, request, jsonify, redirect, session
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = 'secret_key_Xnuvers007'
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})

# set up user agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

@app.route('/translate', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def translate():
    from_lang = request.args.get('from', 'en')
    to_lang = request.args.get('to', 'id')
    text = request.args.get('text', '')

    # set up headers
    headers = {
        'User-Agent': user_agent,
        'Referer': 'http://translate.google.com/',
        'Origin': 'http://translate.google.com/'
    }

    # send request to Google Translate API
    url = f'https://translate.google.com/translate_a/single?client=gtx&sl={from_lang}&tl={to_lang}&dt=t&q={text}'
    response = requests.get(url, headers=headers, cookies=session.get('cookies'))

    # extract cookies from response and store it in session
    if 'Set-Cookie' in response.headers:
        cookies = {}
        for cookie in response.headers.get('Set-Cookie').split(','):
            cookie_name = cookie.split('=')[0]
            cookie_value = cookie.split('=')[1].split(';')[0]
            cookies[cookie_name] = cookie_value
        session['cookies'] = cookies

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
