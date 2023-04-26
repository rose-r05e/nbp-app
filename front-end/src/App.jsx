import React, { useState } from 'react';

export function App(props) {

  const currencyCodes = [
    'USD', 'EUR', 'GBP', 'CHF', 'JPY', 'CZK', 'DKK', 'NOK', 'SEK', 'HUF', 'AUD', 'CAD'
  ];

  const currencyOptions = currencyCodes.map(code => <option value={code}>{code}</option>);

  const [currencyCode, setCurrencyCode] = useState('EUR');
  const [functionType, setFunctionType] = useState('exchangeRate');
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));
  const [numQuotations, setNumQuotations] = useState(30);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      let data;
      if (functionType === 'exchangeRate') {
        data = await getExchangeRate(currencyCode, date);
      } else if (functionType === 'maxMin') {
        data = await getMaxMin(currencyCode, numQuotations);
      } else if (functionType === 'majorDifference') {
        data = await getMajorDifference(currencyCode, numQuotations);
      }
      setResult(data);
      setError(null);
    } catch (error) {
      setError(error.message);
      setResult(null);
    }
  }

  return (
    <div>
      <h1>NBP API Client</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Currency Code:
          <select value={currencyCode} onChange={(e) => setCurrencyCode(e.target.value)}>
            { currencyOptions }
          </select>
        </label>
        <br />
        <label>
          Function Type:
          <select value={functionType} onChange={(e) => setFunctionType(e.target.value)}>
            <option value="exchangeRate">Exchange Rate</option>
            <option value="maxMinExchangeRate">Max/Min Exchange Rate</option>
            <option value="majorDifference">Major Difference</option>
          </select>
        </label>
        <br />
        {functionType === 'exchangeRate' ? (
          <label>
            Date:
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </label>
        ) : (
          <label>
            Number of Quotations:
            <input
              type="number"
              value={numQuotations}
              onChange={(e) => setNumQuotations(parseInt(e.target.value))}
              min={1}
              max={255}
            />
          </label>
        )}
        <br />
        <button type="submit">Submit</button>
      </form>
      {result && (
        <div>
          <h2>Result:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      {error && (
        <div>
          <h2>Error:</h2>
          <pre>{error}</pre>
        </div>
      )}
    </div>
  );
}

// Function to get average exchange rate for a given currency code and date
async function getExchangeRate(currencyCode, date) {
  const response = await fetch(`http://localhost:5000/average_exchange_rate?currency_code=${currencyCode}&date=${date}`);
  const data = await response.json();
  if (response.ok) {
    return data.exchangeRate;
  } else {
    throw new Error(data.error);
  }
}

// Function to get max and min average for a given currency code and number of quotations
async function getMaxMin(currencyCode, numQuotations) {
  const response = await fetch(`http://localhost:5000/max_min_average?currency_code=${currencyCode}&count=${numQuotations}`);
  const data = await response.json();
  if (response.ok) {
    return data;
  } else {
    throw new Error(data.error);
  }
}

// Function to get the major difference between buy and ask rates for a given currency code and number of quotations
async function getMajorDifference(currencyCode, numQuotations) {
  const response = await fetch(`http://localhost:5000/major_difference?currency_code=${currencyCode}&count=${numQuotations}`);
  const data = await response.json();
  if (response.ok) {
    return data;
  } else {
    throw new Error(data.error);
  }
}

// Log to console
console.log('Hello console')