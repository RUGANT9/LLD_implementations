from enum import Enum
import uuid

class TradeDirection(Enum):
    BUY = 'Buy'
    SELL = 'Sell'

class Order:
    def __init__(self, symbol: str, quantity: int, direction: TradeDirection):
        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
    

class Trade:
    def __init__(self, order: Order):
      self.order = order
    
    def buy(self, q, s):
        # dummy function that will call and interact with exchange API
        return True
    
    def sell(self, q, s):
        return True

    def execute_trade(self):
        if self.order.direction == TradeDirection.BUY:
            return self.buy(self.order.quantity, self.order.symbol)
        else:
            return self.sell(self.order.quantity, self.order.symbol)


class User:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.app = None

    
    def place_order(self, symbol: str, quantity: int, direction: TradeDirection):
        if self.app:
            ord_obj = Order(symbol=symbol, quantity=quantity, direction=direction)
            print(self.app.accept_order(ord_obj, self.id))
        else:
            print('Not Registered')
    
    def view_trades(self):
        if self.app:
            print(self.app.users[self.id])
        else:
            print('No trades so far')


class TradeApp:
    def __init__(self, users: dict = None):
        self.users = users if users is not None else {}
    
    def add_user(self, user: User):
        self.users[user.id] = []
        user.app = self
    
    def accept_order(self, order, user_id):
        if user_id in self.users:
            trade_obj = Trade(order)
            if trade_obj.execute_trade():
                self.users[user_id].append(f'{order.__dict__}')
                print('Trade executed successfully')
                return True
            else:
                print('Trade was not successfull, refer to order book for details')
                return False



if __name__ == '__main__':
    tradeapp1 = TradeApp()
    us1 = User('user1')
    tradeapp1.add_user(us1)
    us1.place_order('AAPL', 5, TradeDirection.BUY)
    print(tradeapp1.users[us1.id])

            

        
    