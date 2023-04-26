# nbp-app

This is a simple exchange rate analysis tool that allows you to perform various operations on exchange rates using a Python server and a React front-end. In this README, you will find instructions on how to start the server, run tests, make query operations using curl or a web browser, and launch the React front-end.

## Getting Started

### 1. Start the Server
To start the server, open a terminal and navigate to the back-end directory. Then, run the following command:
```
python server.py
```
### 2. Run Tests (optional)
To run the tests, open another terminal and navigate to the back-end directory. Then, run the following command:
```
python tests.py
```

## Query Operations

### Using curl
You can perform query operations using the curl command in the terminal. Here are some examples:

-Get the average exchange rate for a specific currency and date:
```
curl "http://localhost:5000/average_exchange_rate?currency_code={currencyCode}&date={date}"
```

-Get the max, min, and average exchange rate for a specific currency and a number of recent quotations:
```
curl "http://localhost:5000/max_min_average?currency_code={currencyCode}&count={numQuotations}"
```
-Get the major difference in exchange rates for a specific currency and a number of recent quotations:
```
curl "http://localhost:5000/major_difference?currency_code={currencyCode}&count={numQuotations}"
```

Replace {currencyCode}, {date}, and {numQuotations} with appropriate values.
Alternatively, you can make query operations by entering the addresses above in your web browser.

## Launching the React Front-end

To launch the React front-end, simply navigate to /front-end/dist directory and then open the index.html file in a web browser. This should display the user interface, where you can interact with the server and perform various operations on exchange rates.
