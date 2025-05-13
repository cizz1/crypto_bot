import logging
import sys
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('futures_trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """Initialize the futures trading bot with Binance API credentials."""
        self.client = Client(api_key, api_secret, testnet=testnet)
        if testnet:
            self.client.API_URL = 'https://testnet.binancefuture.com/api'
        logger.info("Futures Bot initialized with Testnet: %s", testnet)
        
    def get_account_balance(self):
        """Get futures account balance."""
        try:
            balance = self.client.futures_account_balance()
            logger.info("Account balance retrieved successfully")
            return balance
        except BinanceAPIException as e:
            logger.error("Failed to get account balance: %s", str(e))
            return None

    def validate_symbol(self, symbol):
        """Validate if the futures trading symbol exists."""
        try:
            exchange_info = self.client.futures_exchange_info()
            symbols = [info['symbol'] for info in exchange_info['symbols']]
            if symbol in symbols:
                logger.info("Symbol %s validated for futures trading", symbol)
                return True
            logger.error("Invalid futures symbol: %s", symbol)
            return False
        except BinanceAPIException as e:
            logger.error("Symbol validation error: %s", str(e))
            return False

    def place_market_order(self, symbol, side, quantity):
        """Place a futures market order."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logger.info("Futures market order placed: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Futures market order error: %s", str(e))
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        """Place a futures limit order."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logger.info("Futures limit order placed: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Futures limit order error: %s", str(e))
            return None

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """Place a futures stop-limit order."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price,
                workingType='MARK_PRICE'
            )
            logger.info("Futures stop-limit order placed: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Futures stop-limit order error: %s", str(e))
            return None

    def get_order_status(self, symbol, order_id):
        """Check the status of a futures order."""
        try:
            status = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            logger.info("Futures order status: %s", status)
            return status
        except BinanceAPIException as e:
            logger.error("Futures order status error: %s", str(e))
            return None
            
    def get_position_info(self, symbol=None):
        """Get current position information."""
        try:
            if symbol:
                positions = [p for p in self.client.futures_position_information() if p['symbol'] == symbol]
            else:
                positions = self.client.futures_position_information()
            logger.info("Position information retrieved")
            return positions
        except BinanceAPIException as e:
            logger.error("Position information error: %s", str(e))
            return None

def format_balance(balance_list):
    """Format balance information for display."""
    formatted = ""
    for item in balance_list:
        if float(item['balance']) > 0:
            formatted += f"Asset: {item['asset']}, Balance: {item['balance']}\n"
    return formatted

def format_position_info(positions):
    """Format position information for display."""
    formatted = ""
    for position in positions:
        if float(position['positionAmt']) != 0:
            formatted += f"Symbol: {position['symbol']}\n"
            formatted += f"Position Amount: {position['positionAmt']}\n"
            formatted += f"Entry Price: {position['entryPrice']}\n"
            formatted += f"Unrealized PnL: {position['unRealizedProfit']}\n"    
            formatted += "-----------------------\n"
    if not formatted:
        formatted = "No open positions found."
    return formatted

def main():
    st.title("Binance Futures Trading Bot")
    st.markdown("Interact with Binance Futures Testnet to place orders and view account details.")

    # Initialize bot
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    if not API_KEY or not API_SECRET:
        st.error("API Key or Secret not found in .env file!")
        return
    
    bot = BasicBot(API_KEY, API_SECRET, testnet=True)

    # Sidebar for operation selection
    operation = st.sidebar.selectbox(
        "Select Operation",
        [
            "Place Market Order",
            "Place Limit Order",
            "Place Stop-Limit Order",
            "Check Order Status",
            "Get Account Balance",
            "Get Position Information"
        ]
    )

    # Operation forms
    if operation == "Place Market Order":
        st.subheader("Place Market Order")
        symbol = st.text_input("Futures Symbol (e.g., BTCUSDT)", value="BTCUSDT").upper()
        side = st.selectbox("Side", ["BUY", "SELL"])
        quantity = st.text_input("Quantity (e.g., 0.001)")
        
        if st.button("Submit Market Order"):
            if not bot.validate_symbol(symbol):
                st.error("Invalid futures symbol!")
            else:
                try:
                    quantity = float(quantity)
                    order = bot.place_market_order(symbol, side, quantity)
                    if order:
                        st.success(f"Futures Market Order placed: {order}")
                    else:
                        st.error("Failed to place market order. Check logs for details.")
                except ValueError:
                    st.error("Invalid quantity!")
                    logger.error("Invalid quantity input: %s", quantity)

    elif operation == "Place Limit Order":
        st.subheader("Place Limit Order")
        symbol = st.text_input("Futures Symbol (e.g., BTCUSDT)", value="BTCUSDT").upper()
        side = st.selectbox("Side", ["BUY", "SELL"])
        quantity = st.text_input("Quantity (e.g., 0.001)")
        price = st.text_input("Limit Price (e.g., 80000)")
        
        if st.button("Submit Limit Order"):
            if not bot.validate_symbol(symbol):
                st.error("Invalid futures symbol!")
            else:
                try:
                    quantity = float(quantity)
                    price = float(price)
                    order = bot.place_limit_order(symbol, side, quantity, price)
                    if order:
                        st.success(f"Futures Limit Order placed: {order}")
                    else:
                        st.error("Failed to place limit order. Check logs for details.")
                except ValueError:
                    st.error("Invalid quantity or price!")
                    logger.error("Invalid input - quantity: %s, price: %s", quantity, price)

    elif operation == "Place Stop-Limit Order":
        st.subheader("Place Stop-Limit Order")
        symbol = st.text_input("Futures Symbol (e.g., BTCUSDT)", value="BTCUSDT").upper()
        side = st.selectbox("Side", ["BUY", "SELL"])
        quantity = st.text_input("Quantity (e.g., 0.001)")
        stop_price = st.text_input("Stop Price (e.g., 81000)")
        limit_price = st.text_input("Limit Price (e.g., 81200)")
        
        if st.button("Submit Stop-Limit Order"):
            if not bot.validate_symbol(symbol):
                st.error("Invalid futures symbol!")
            else:
                try:
                    quantity = float(quantity)
                    stop_price = float(stop_price)
                    limit_price = float(limit_price)
                    order = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
                    if order:
                        st.success(f"Futures Stop-Limit Order placed: {order}")
                    else:
                        st.error("Failed to place stop-limit order. Check logs for details.")
                except ValueError:
                    st.error("Invalid quantity, stop price, or limit price!")
                    logger.error("Invalid input - quantity: %s, stop_price: %s, limit_price: %s",
                                quantity, stop_price, limit_price)

    elif operation == "Check Order Status":
        st.subheader("Check Order Status")
        symbol = st.text_input("Futures Symbol (e.g., BTCUSDT)", value="BTCUSDT").upper()
        order_id = st.text_input("Order ID")
        
        if st.button("Check Status"):
            try:
                order_id = int(order_id)
                status = bot.get_order_status(symbol, order_id)
                if status:
                    st.success(f"Futures Order Status: {status}")
                else:
                    st.error("Failed to retrieve order status. Check logs for details.")
            except ValueError:
                st.error("Invalid order ID!")
                logger.error("Invalid order ID input: %s", order_id)

    elif operation == "Get Account Balance":
        st.subheader("Account Balance")
        if st.button("Fetch Balance"):
            balance = bot.get_account_balance()
            if balance:
                st.success("Futures Account Balance:")
                st.text(format_balance(balance))
            else:
                st.error("Failed to retrieve account balance. Check logs for details.")

    elif operation == "Get Position Information":
        st.subheader("Position Information")
        symbol = st.text_input("Futures Symbol (leave empty for all positions)", value="").upper()
        if st.button("Fetch Positions"):
            positions = bot.get_position_info(symbol if symbol else None)
            if positions:
                st.success("Futures Position Information:")
                st.text(format_position_info(positions))
            else:
                st.error("Failed to retrieve position information. Check logs for details.")

if __name__ == "__main__":
    main()
