from flask import Flask, render_template, request, send_file
from openai_logic import process_headings, input_keywords, input_headers, unique_text

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        headers = request.form['headers']
        keywords = request.form['keywords']
        print(headers, keywords)
        exit(0)
        return send_file(process_headings(input_headers(headers), input_keywords(keywords)))

    return render_template('index.html')


@app.route('/uniq', methods=['GET', 'POST'])
def uniq():
    if request.method == 'POST':
        user_text = request.form['user-text']
        return render_template('result.html', result=unique_text(user_text))

    return render_template('uniq.html')


if __name__ == "__main__":
    app.run(debug=True)
