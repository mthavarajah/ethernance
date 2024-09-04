from flask import Flask, Response, render_template, request, redirect, url_for, send_file
import requests
import sqlite3
import csv
import io
from sqlite3 import OperationalError
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)

# Custom error handler for OperationalError
# @app.errorhandler(OperationalError)
# def handle_operational_error(error):
#     return render_template('error.html', error_message="A database error occurred."), 500

# General error handler for any unhandled exceptions
# @app.errorhandler(Exception)
# def handle_exception(error):
#     return render_template('error.html', error_message="An unexpected error occurred."), 500

# Homepage
@app.route('/')
def home():
    # ETH to USD
    usd_json_eth = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    usd_response_eth = requests.get(usd_json_eth)
    usd_data_eth = usd_response_eth.json()
    usd_price_eth = float(usd_data_eth['price'])

    # BNB to USD
    usd_json_bnb = "https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT"
    usd_response_bnb = requests.get(usd_json_bnb)
    usd_data_bnb = usd_response_bnb.json()
    usd_price_bnb = float(usd_data_bnb['price'])

    # Formatting
    eth_formatted = "${:,.2f}".format(usd_price_eth)
    bnb_formatted = "${:,.2f}".format(usd_price_bnb)

    # HTML Rendering
    return render_template('home.html', 
                           eth_formatted=eth_formatted,
                           bnb_formatted=bnb_formatted)

# Handle Form
@app.route('/handle_form', methods=['GET'])
def handle_form():
    address = request.args.get('address')
    blockchain = request.args.get('blockchain')

    if blockchain == 'ethereum':
        return redirect(url_for('ethereum', address=address))
    elif blockchain == 'binance':
        return redirect(url_for('binance', address=address))
    else:
        return redirect(url_for('home'))

# Ethereum
@app.route('/ethereum')
def ethereum():

    name = 'ethereum'
    symbol = 'ETH'
    link = 'https://etherscan.io/'
    api_key = 'PTRS8TGA5V4CXNACUGEBB5FC3RQZ28WBPG'
    address = request.args.get('address').lower()

    if not address:
        return "Wallet address is required.", 400

    '''
    BALANCE
    '''
    url1 = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}'

    # Extract data via API
    response1 = requests.get(url1)
    balance_json = response1.json()

    # Invalid input error message
    if balance_json['status'] != '1':
        return render_template('error.html')

    # ETH to USD
    usd_json = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    usd_response = requests.get(usd_json)
    usd_data = usd_response.json()
    usd_price = float(usd_data['price'])

    # Balance Values
    balance = float(balance_json['result'])*(10**(-18))
    usd_balance = balance*usd_price
    balance_formatted = "{:,f} ETH".format(balance)
    usd_balance_formatted = "{:,.2f} USD".format(usd_balance)


    '''
    TRANSACTIONS
    '''
    url2 = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=desc&apikey={api_key}'

    # Extract data via API
    response2 = requests.get(url2)
    data = response2.json()

    # Fetch data
    if data['status'] == '1':
        transactions = data['result']
    else:
        return render_template('error.html')

    # Connecting to SQLite3 Database
    db = sqlite3.connect('transactions.db')
    cursor = db.cursor()

    # Read transactions.sql
    cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS eth_{address}_transactions (
                    hash TEXT,
                    blockNumber TEXT,
                    transferType TEXT,
                    date DATE,
                    fromAddress TEXT,
                    toAddress TEXT,
                    value FLOAT,
                    usdvalue FLOAT
                    )
                    ''')

    # Delete data from table to avoid duplicates
    cursor.execute(f'DELETE FROM eth_{address}_transactions')

    # Add transactions to table
    for tx in transactions:
        if tx['from'] == address:
            transferType = 'Out'
        elif tx['to'] == address:
            transferType = 'In'
        else:
            transferType = 'N/A'
        
        hash = tx['hash']
        blocknumber = tx['blockNumber']
        date = datetime.fromtimestamp(int(tx['timeStamp']))
        fromAddress = tx['from']
        toAddress = tx['to']
        cursor.execute(f'''
                        INSERT INTO eth_{address}_transactions (
                            hash, 
                            blockNumber, 
                            transferType, 
                            date, 
                            fromAddress,
                            toAddress, 
                            value, 
                            usdvalue
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''',
            (
                hash,
                blocknumber,
                transferType,
                date,
                fromAddress, 
                toAddress,
                float(tx['value'])*(10**(-18)),
                float(tx['value'])*(10**(-18))*float(usd_price)
            )
        )
    db.commit()
    
    # Filter results based on search query and selected column
    search_query = request.args.get('search', '').lower()
    search_column = request.args.get('column', '')
    search_transferType = request.args.get('in-out', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    query = f'SELECT * FROM eth_{address}_transactions'
    params = ()

    if search_column == 'transferType' and search_transferType:
        query += ' WHERE transferType LIKE ?'
        params = (search_transferType,)
    elif search_column == 'date' and start_date and end_date:
        query += ' WHERE date BETWEEN ? AND ?'
        params = (start_date, end_date)
    elif search_query:
        query += f' WHERE {search_column} LIKE ?'
        params = (f'%{search_query}%',)

    cursor.execute(query, params)
    results = cursor.fetchall()

    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = 100
    start_row = (page - 1) * per_page

    # Pagination logic
    total_rows = len(results)
    total_pages = (total_rows + per_page - 1) // per_page
    paginated_results = results[start_row:start_row + per_page]

    # Pagination Rotation
    start_page = 1
    end_page = total_pages

    if total_pages > 5:
        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)

        if end_page - start_page < 4:
            if start_page == 1:
                end_page = min(5, total_pages)
            else:
                start_page = max(1, end_page - 4)

    visible_pages = range(start_page, end_page + 1)
    previous_set = max(1, start_page - 5)
    next_set = min(total_pages, end_page + 1)

    db.close()

    # HTML Rendering
    return render_template('info.html',
                           name=name,
                           symbol=symbol,
                           link=link,
                           address=address,
                           results=paginated_results, 
                           balance_formatted=balance_formatted, 
                           usd_balance_formatted=usd_balance_formatted,
                           hash=hash,
                           blocknumber=blocknumber,
                           date=date,
                           fromAddress=fromAddress,
                           toAddress=toAddress,
                           search_column=search_column,
                           search_query=search_query,
                           search_transferType=search_transferType,
                           start_date=start_date,
                           end_date=end_date,
                           current_page=page,
                           total_pages=total_pages,
                           total_rows=total_rows,
                           visible_pages=visible_pages,
                           previous_set=previous_set,
                           next_set=next_set)

# Binance
@app.route('/binance')
def binance():

    name = 'binance'
    symbol = 'BNB'
    link = 'https://bscscan.com/'
    api_key = 'K7Y216JCF2ZI399V8TQJSCWPPESIVP8AYP'
    address = request.args.get('address').lower()

    if not address:
        return "Wallet address is required.", 400

    '''
    BALANCE
    '''
    url1 = f'https://api.bscscan.com/api?module=account&action=balance&address={address}&apikey={api_key}'

    # Extract data via API
    response1 = requests.get(url1)
    balance_json = response1.json()
    
    # Invalid input error message
    if balance_json['status'] != '1':
        return render_template('error.html')

    # BNB to USD
    usd_json = "https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT"
    usd_response = requests.get(usd_json)
    usd_data = usd_response.json()
    usd_price = float(usd_data['price'])

    # Balance Values
    balance = float(balance_json['result'])*(10**(-18))
    usd_balance = balance*usd_price
    balance_formatted = "{:,f} BNB".format(balance)
    usd_balance_formatted = "{:,.2f} USD".format(usd_balance)


    '''
    TRANSACTIONS
    '''
    url2 = f'https://api.bscscan.com/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=desc&apikey={api_key}'

    # Extract data via API
    response2 = requests.get(url2)
    data = response2.json()

    # Fetch data
    if data['status'] == '1':
        transactions = data['result']
    else:
        return render_template('error.html')

    # Connecting to SQLite3 Database
    db = sqlite3.connect('transactions.db')
    cursor = db.cursor()

    # Read transactions.sql
    cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS bnb_{address}_transactions (
                    hash TEXT,
                    blockNumber TEXT,
                    transferType TEXT,
                    date DATE,
                    fromAddress TEXT,
                    toAddress TEXT,
                    value FLOAT,
                    usdvalue FLOAT
                    )
                    ''')

    # Delete data from table to avoid duplicates
    cursor.execute(f'DELETE FROM bnb_{address}_transactions')

    # Add transactions to table
    for tx in transactions:
        if tx['from'] == address:
            transferType = 'Out'
        elif tx['to'] == address:
            transferType = 'In'
        else:
            transferType = 'N/A'
        
        hash = tx['hash']
        blocknumber = tx['blockNumber']
        date = datetime.fromtimestamp(int(tx['timeStamp']))
        fromAddress = tx['from']
        toAddress = tx['to']
        cursor.execute(f'''
                        INSERT INTO bnb_{address}_transactions (
                            hash, 
                            blockNumber, 
                            transferType, 
                            date, 
                            fromAddress,
                            toAddress, 
                            value, 
                            usdvalue
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''',
            (
                hash,
                blocknumber,
                transferType,
                date,
                fromAddress, 
                toAddress,
                float(tx['value'])*(10**(-18)),
                float(tx['value'])*(10**(-18))*float(usd_price)
            )
        )
    db.commit()
    
    # Filter results based on search query and selected column
    search_query = request.args.get('search', '').lower()
    search_column = request.args.get('column', '')
    search_transferType = request.args.get('in-out', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    query = f'SELECT * FROM bnb_{address}_transactions'
    params = ()

    if search_column == 'transferType' and search_transferType:
        query += ' WHERE transferType LIKE ?'
        params = (search_transferType,)
    elif search_column == 'date' and start_date and end_date:
        query += ' WHERE date BETWEEN ? AND ?'
        params = (start_date, end_date)
    elif search_query:
        query += f' WHERE {search_column} LIKE ?'
        params = (f'%{search_query}%',)

    cursor.execute(query, params)
    results = cursor.fetchall()

    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = 100
    start_row = (page - 1) * per_page

    # Pagination logic
    total_rows = len(results)
    total_pages = (total_rows + per_page - 1) // per_page
    paginated_results = results[start_row:start_row + per_page]

    # Pagination Rotation
    start_page = 1
    end_page = total_pages

    if total_pages > 5:
        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)

        if end_page - start_page < 4:
            if start_page == 1:
                end_page = min(5, total_pages)
            else:
                start_page = max(1, end_page - 4)

    visible_pages = range(start_page, end_page + 1)
    previous_set = max(1, start_page - 5)
    next_set = min(total_pages, end_page + 1)

    db.close()

    # HTML Rendering
    return render_template('info.html',
                           name=name,
                           symbol=symbol,
                           link=link, 
                           address=address,
                           results=paginated_results, 
                           balance_formatted=balance_formatted, 
                           usd_balance_formatted=usd_balance_formatted,
                           hash=hash,
                           blocknumber=blocknumber,
                           date=date,
                           fromAddress=fromAddress,
                           toAddress=toAddress,
                           search_column=search_column,
                           search_query=search_query,
                           search_transferType=search_transferType,
                           start_date=start_date,
                           end_date=end_date,
                           current_page=page,
                           total_pages=total_pages,
                           total_rows=total_rows,
                           visible_pages=visible_pages,
                           previous_set=previous_set,
                           next_set=next_set)


# Download CSV
@app.route('/download_csv')
def download_csv():
    
    address = request.args.get('address').lower()
    blockchain = request.args.get('blockchain')

    if blockchain == 'ethereum':
        symbol = 'eth'
    elif blockchain == 'binance':
        symbol = 'bnb'

    # Connecting to SQLite3 Database
    db = sqlite3.connect('transactions.db')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM {symbol}_{address}_transactions')
    results = cursor.fetchall()

    # Convert to CSV File
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([f'{blockchain[0].upper()}{blockchain[1:]} Address: {address}'])
    
    if len(results) < 10000:
        writer.writerow([f'Transactions: {"{:,.0f}".format(len(results))}'])
    else:
        writer.writerow(['Transactions: 10,000+'])
    writer.writerow([])
    writer.writerow(['Transaction Hash', 'Block Number', 'Transfer Type', 'Date', 'From', 'To', f'Amount ({symbol.upper()})', 'Amount (USD)'])
    for row in results:
        writer.writerow(row)

    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={symbol}_{address}.csv"}
    )


if __name__ == '__main__':
    app.run(debg=True)
