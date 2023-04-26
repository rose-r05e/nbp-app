from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Endpoint to get the average exchange rate for a currency and date
@app.route('/average_exchange_rate')
def average_exchange_rate():
    currency_code = request.args.get('currency_code')
    date_str = request.args.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d')
    # Check if date is a weekend or holiday
    while True:
        if date.weekday() >= 5:  # Saturday or Sunday
            return jsonify({'error': 'Weekend dates do not return data.'}), 400
        url = f'http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{date.date()}/'
        response = requests.get(url)
        if response.status_code == 200:
            rate = response.json()['rates'][0]['mid']
            return jsonify({'average_exchange_rate': rate})
        else:
            date -= timedelta(days=1)
            if date_str == date.date().strftime('%Y-%m-%d'):
                return jsonify({'error': 'Could not get average exchange rate.'}), 500

# Endpoint to get the max and min average value for a currency and number of last quotations
@app.route('/max_min_average')
def max_min_average():
    currency_code = request.args.get('currency_code')
    count = request.args.get('count')
    try:
        count = int(count)
    except ValueError:
        return jsonify({'error': 'Invalid count value. Please provide an integer between 1 and 255.'}), 400
    if not 1 <= count <= 255:
        return jsonify({'error': 'Invalid count value. Please provide an integer between 1 and 255.'}), 400
    url = f'http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/last/{count}/'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Could not get max and min average.'}), 500
    rates = [rate['mid'] for rate in response.json()['rates']]
    max_rate = max(rates)
    min_rate = min(rates)
    return jsonify({'max_average': max_rate, 'min_average': min_rate})

# Endpoint to get the major difference between the buy and ask rate for a currency and number of last quotations
@app.route('/major_difference')
def major_difference():
    currency_code = request.args.get('currency_code')
    count = request.args.get('count')
    try:
        count = int(count)
    except ValueError:
        return jsonify({'error': 'Invalid count value. Please provide an integer between 1 and 255.'}), 400
    if not 1 <= count <= 255:
        return jsonify({'error': 'Invalid count value. Please provide an integer between 1 and 255.'}), 400
    url = f'http://api.nbp.pl/api/exchangerates/rates/c/{currency_code}/last/{count}/'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Could not get major difference.'}), 500
    rates = [rate['bid'] - rate['ask'] for rate in response.json()['rates']]
    major_difference = max(rates)
    return jsonify({'major_difference': major_difference})

if __name__ == '__main__':
    app.run()
