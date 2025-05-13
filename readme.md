# Binance Futures Trading Bot

This project is a simplified trading bot developed as part of the internship application. It interacts with the Binance Futures Testnet to place market, limit, and stop-limit orders for USDT-margined futures (e.g., BTCUSDT). Built using Python and the `python-binance` library, it features both a command-line interface (CLI) and a Streamlit web interface.

---

## Features

- **Order Types**: Supports market, limit, and stop-limit (bonus) orders for both BUY and SELL sides.  
- **Binance Testnet**: Uses the testnet URL (`https://testnet.binancefuture.com`) for safe, simulated trading.  
- **Interfaces**: CLI (`futures_bot.py`) and Streamlit UI (`streamlit_bot.py`) with input validation and clear output.  
- **Logging**: Logs API requests, responses, and errors to `futures_trading_bot.log` and console.  
- **Error Handling**: Handles invalid inputs and API errors gracefully.

---

## Screenshot

Below is a screenshot of the Streamlit UI in action:

![Streamlit UI](bot_ui.png)

---

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Binance Testnet

- Register at [Binance Futures Testnet](https://testnet.binancefuture.com).
- Generate your API key and secret.

### 4. Configure Environment

Create a `.env` file in the project root and add your credentials:

```env
API_KEY=your_testnet_api_key  
API_SECRET=your_testnet_api_secret
```

---

## Run the Bot

### For CLI:

```bash
python futures_bot.py
```

### For Streamlit UI:

```bash
streamlit run streamlit_bot.py
```

---

## Usage

### CLI (`futures_bot.py`):

- Launch and select from options 1–7:
  1. Place a market order  
  2. Place a limit order  
  3. Place a stop-limit order  
  4. Check order status  
  5. View account balance  
  6. View position information  
  7. Exit  

- Follow prompts to enter:
  - Symbol (e.g., BTCUSDT)  
  - Side (BUY/SELL)  
  - Quantity  
  - Prices (if applicable)

### Streamlit UI (`streamlit_bot.py`):

- Open in browser (typically at [http://localhost:8501](http://localhost:8501))  
- Select an operation from the sidebar (e.g., *Place Market Order*)  
- Enter required inputs and click **Submit**  
- View results or errors directly in the interface  
- Logs are saved to `futures_trading_bot.log`

---

## Assignment Compliance

- **Language**: Python  
- **API**: Uses `python-binance` for REST calls to Binance Futures Testnet  
- **Orders**: Supports market and limit orders, with stop-limit as a bonus feature  
- **Interface**: CLI and Streamlit UI with input validation and clear output  
- **Logging**: Comprehensive logging of all actions and errors  
- **Error Handling**: Robust handling of API and user input errors  
- **Bonus**: Includes stop-limit orders and a Streamlit frontend  

---
