import logging
import sys
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import time
import os
from dotenv import load_dotenv
load_dotenv()

# logging
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
        # Set the base_url for futures testnet
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
        """Place a futures stop-limit order (Bonus feature)."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price,
                workingType='MARK_PRICE'  # Using mark price for trigger
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

def print_menu():
    """Display the command-line menu."""
    print("\n=== Binance Futures Trading Bot ===")
    print("1. Place Market Order")
    print("2. Place Limit Order")
    print("3. Place Stop-Limit Order")
    print("4. Check Order Status")
    print("5. Get Account Balance")
    print("6. Get Position Information")
    print("7. Exit")

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
    
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    
    bot = BasicBot(API_KEY, API_SECRET, testnet=True)
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            symbol = input("Enter futures symbol (e.g., BTCUSDT): ").upper()
            if not bot.validate_symbol(symbol):
                continue
            side = input("Enter side (BUY/SELL): ").upper()
            if side not in ['BUY', 'SELL']:
                print("Invalid side!")
                continue
            quantity = input("Enter quantity: ")
            try:
                quantity = float(quantity)
                order = bot.place_market_order(symbol, side, quantity)
                if order:
                    print(f"Futures Market Order placed: {order}")
            except ValueError:
                print("Invalid quantity!")
                logger.error("Invalid quantity input: %s", quantity)

        elif choice == '2':
            symbol = input("Enter futures symbol (e.g., BTCUSDT): ").upper()
            if not bot.validate_symbol(symbol):
                continue
            side = input("Enter side (BUY/SELL): ").upper()
            if side not in ['BUY', 'SELL']:
                print("Invalid side!")
                continue
            quantity = input("Enter quantity: ")
            price = input("Enter limit price: ")
            try:
                quantity = float(quantity)
                price = float(price)
                order = bot.place_limit_order(symbol, side, quantity, price)
                if order:
                    print(f"Futures Limit Order placed: {order}")
            except ValueError:
                print("Invalid quantity or price!")
                logger.error("Invalid input - quantity: %s, price: %s", quantity, price)

        elif choice == '3':
            symbol = input("Enter futures symbol (e.g., BTCUSDT): ").upper()
            if not bot.validate_symbol(symbol):
                continue
            side = input("Enter side (BUY/SELL): ").upper()
            if side not in ['BUY', 'SELL']:
                print("Invalid side!")
                continue
            quantity = input("Enter quantity: ")
            stop_price = input("Enter stop price: ")
            limit_price = input("Enter limit price: ")
            try:
                quantity = float(quantity)
                stop_price = float(stop_price)
                limit_price = float(limit_price)
                order = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
                if order:
                    print(f"Futures Stop-Limit Order placed: {order}")
            except ValueError:
                print("Invalid quantity, stop price, or limit price!")
                logger.error("Invalid input - quantity: %s, stop_price: %s, limit_price: %s", 
                           quantity, stop_price, limit_price)

        elif choice == '4':
            symbol = input("Enter futures symbol (e.g., BTCUSDT): ").upper()
            order_id = input("Enter order ID: ")
            try:
                order_id = int(order_id)
                status = bot.get_order_status(symbol, order_id)
                if status:
                    print(f"Futures Order Status: {status}")
            except ValueError:
                print("Invalid order ID!")
                logger.error("Invalid order ID input: %s", order_id)

        elif choice == '5':
            balance = bot.get_account_balance()
            if balance:
                print("Futures Account Balance:")
                print(format_balance(balance))
            else:
                print("Failed to retrieve account balance.")

        elif choice == '6':
            symbol = input("Enter futures symbol (leave empty for all positions): ").upper()
            positions = bot.get_position_info(symbol if symbol else None)
            if positions:
                print("Futures Position Information:")
                print(format_position_info(positions))
            else:
                print("Failed to retrieve position information.")

        elif choice == '7':
            print("Exiting Futures Trading Bot...")
            logger.info("Bot shutdown")
            break

        else:
            print("Invalid choice!")
            logger.warning("Invalid menu choice: %s", choice)

if __name__ == "__main__":
    main()