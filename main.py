from flask import Flask, render_template, request, send_file
from openai_logic import process_headings, input_keywords

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text1 = request.form['textarea1']
        text2 = request.form['textarea2']
        
        return send_file(process_headings(text1, input_keywords(text2)))

    return render_template('form.html')


if __name__ == "__main__":
    app.run(debug=True)
