# [Ethernance](https://ethernance.onrender.com/)

Ethernance is a blockchain explorer tool that allows users to explore transactions and balances for Ethereum and Binance wallet addresses. It provides a comprehensive view of transactions, including search functionalities and export options. Users can only request the most recent 10,000 transactions per wallet address.

## Features

- **Blockchain Exploration**: View transaction details and wallet balances for Ethereum and Binance.
- **Search Functionality**: Search transactions by hash, block number, transfer type, date, from address, and to address.
- **Export Options**: Download transaction data as CSV files.
- **Responsive Design**: User-friendly interface for both desktop and mobile devices.
- **Clipboard Copy**: Easily copy wallet addresses to clipboard.
- **Pagination**: Navigate through large datasets with pagination controls.

## Technology Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3
- **Data Extraction**: JSON API data
- **Hosting**: Render

## Installation

To set up the Ethernance project locally, follow these steps:

1. **Clone the Repository**

    ```bash
    git clone https://github.com/mthavarajah/ethernance.git
    cd ethernance
    ```

2. **Install Dependencies**

    Ensure you have Python installed. Create a virtual environment and install the required packages.

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Set Up the Database**

    The application uses SQLite3 to store API data. Initialize the database by running the following code in app.py:

    ```
    db = sqlite3.connect('transactions.db')
    cursor = db.cursor()
    ```

4. **Run the Application**

    Start the Flask application with:

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Deployment

The Ethernance application is hosted on Render. For deployment and hosting on Render, follow these steps:

1. **Sign Up/Log In to Render**

   Go to [Render](https://render.com) and create an account or log in.

2. **Create a New Web Service**

   - Choose to deploy a new web service.
   - Connect your GitHub repository where the Ethernance code is hosted.
   - Configure build and deploy settings according to your project needs.

3. **Set Up Environment Variables**

   Ensure to configure any necessary environment variables such as `FLASK_ENV` and database configurations.

4. **Deploy**

   Render will build and deploy your application. You can monitor the deployment process on the Render dashboard.

## Usage

### Home Page (`home.html`)

- **Logo**: Displays the Ethernance logo.
- **Titles and Card**: Provides an overview of the platform and displays current price information for Ethereum and Binance Coin.
- **Address Input Form**: Enter wallet addresses and select blockchain type (Ethereum or Binance) for exploration.
- **Social Media Links**: Connect with the developer on LinkedIn, GitHub, or via email.

### Info Page (`info.html`)

- **Logo**: Navigate back to the home page.
- **Address Input Form**: Allows users to input wallet addresses and select blockchain types for searching transactions.
- **Overview Details**: Shows wallet balance, value in USD, and provides options to copy the address or download transaction data as CSV.
- **Search Box**: Filter transactions based on various criteria such as transaction hash, block number, and date.
- **Table**: Displays transaction details with links to transaction and block information.
- **Pagination**: Navigate through search results with pagination controls.
- **Social Media Links**: Connect with the developer on LinkedIn, GitHub, or via email.

## Data Handling

- **Database**: The application uses SQLite3 to store API data for efficient querying and management.
- **Data Extraction**: API data is extracted in JSON format and processed for storage and display.

## Development

To contribute to the development of Ethernance, follow these guidelines:

1. **Fork the Repository**

2. **Initialize a new Git repository**

    ```bash
    git init
    ```

3. **Make Changes and Commit**

    ```bash
    git add *
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/mthavarajah/ethernance.git
    ```

4. **Push Changes**

    ```bash
    git push -u origin main
    ```

5. **Open a Pull Request**

## Contact

For any inquiries or issues, please reach out to [Mathu Thavarajah](mthavarajah10@gmail.com).

---

**Ethernance** | Explore transactions and balances for Ethereum and Binance wallet addresses.
