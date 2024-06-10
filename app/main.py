from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from models import Quote

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

API_URL = 'http://api_server:8000/quotes'

@app.route('/')
def index():
    response = requests.get(API_URL)
    if response.ok:
        quotes = response.json()
    else:
        quotes = []
    return render_template('index.html', quotes=quotes)

@app.route('/add_quote', methods=['GET', 'POST'])
def add_quote():
    if request.method == 'POST':
        text = request.form['text']
        author = request.form['author']
        quote = Quote(text=text, author=author)
        response = requests.post(API_URL, json=quote.dict())
        if response.ok:
            flash('Quote added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to add quote.', 'danger')
    return render_template('quote_form.html')

@app.route('/delete_quote/<quote_id>')
def delete_quote(quote_id):
    response = requests.delete(f'{API_URL}/{quote_id}')
    if response.ok:
        flash('Quote deleted successfully!', 'success')
    else:
        flash('Failed to delete quote.', 'danger')
    return redirect(url_for('index'))

@app.route('/delete_quotes', methods=['POST'])
def delete_quotes():
    quote_ids = request.form.getlist('quote_ids')
    if not quote_ids:
        flash('No quotes selected for deletion.', 'warning')
    else:
        for quote_id in quote_ids:
            response = requests.delete(f'{API_URL}/{quote_id}')
            if not response.ok:
                flash('Failed to delete some quotes.', 'danger')
                break
        else:
            flash('Selected quotes deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
