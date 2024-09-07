# Ethernance

Ethernance is a blockchain explorer tool that allows users to explore transactions and balances for Ethereum and Binance wallet addresses. It provides a comprehensive view of transactions, including search functionalities and export options.

## Features

- **Blockchain Exploration**: View transaction details and wallet balances for Ethereum and Binance.
- **Search Functionality**: Search transactions by hash, block number, transfer type, date, from address, and to address.
- **Export Options**: Download transaction data as CSV files.
- **Responsive Design**: User-friendly interface for both desktop and mobile devices.
- **Clipboard Copy**: Easily copy wallet addresses to clipboard.
- **Pagination**: Navigate through large datasets with pagination controls.

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

3. **Run the Application**

    Start the application with:

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

### Home Page (`home.html`)

- **Logo**: Displays the Ethernance logo.
- **Titles and Card**: Provides an overview of the platform and displays current price information for Ethereum and Binance Coin (hover cursor to view card flip).
- **Address Input Form**: Enter wallet addresses and select blockchain type (Ethereum or Binance) for exploration.

### Info Page (`info.html`)

- **Logo**: Navigate back to the home page.
- **Address Input Form**: Allows users to input wallet addresses and select blockchain types for searching transactions.
- **Overview Details**: Shows wallet balance, value in USD, and provides options to copy the address or download transaction data as CSV.
- **Search Box**: Filter transactions based on various criteria such as transaction hash, block number, and date.
- **Table**: Displays transaction details with links to transaction and block information.
- **Pagination**: Navigate through search results with pagination controls.

## Development

To contribute to the development of Ethernance, follow these guidelines:

1. **Fork the Repository**

2. **Create a New Branch**

    ```bash
    git checkout -b feature/new-feature
    ```

3. **Make Changes and Commit**

    ```bash
    git add .
    git commit -m "Add new feature"
    ```

4. **Push Changes**

    ```bash
    git push origin feature/new-feature
    ```

5. **Open a Pull Request**

## Contact

For any inquiries or issues, please reach out to [Mathumaran Thavarajah](m6thavar@uwaterloo.ca).

---

**Ethernance** | Explore transactions and balances for Ethereum and Binance wallet addresses.
