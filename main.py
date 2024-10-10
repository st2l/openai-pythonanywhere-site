from flask import Flask, render_template, request, send_file
from openai_logic import process_headings, input_keywords, input_headers

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        headers = request.form['headers']
        keywords = request.form['keywords']
        
        return send_file(process_headings(input_headers(headers), input_keywords(keywords)))

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
