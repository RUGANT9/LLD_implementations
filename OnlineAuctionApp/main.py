from enum import Enum
from datetime import datetime
import uuid


class ItemStatus(Enum):
    BIDDING = 'Bidding'
    SOLD = 'Sold'

class User:
    def __init__(self, name, owner_app):
        self.name = name
        self.id = uuid.uuid4()
        self.orders = []
        self.owner_app = owner_app

    def list_item(self, item):
        self.owner_app.add_item(item)
    
    def place_bid(self, item_id, bid_price):
        bid_status = False
        if item_id in self.owner_app.items:
            item = self.owner_app.items[item_id]
            if item.status == ItemStatus.BIDDING and bid_price > item.bid_price:
                bid_obj = Bid(self.id, item_id, bid_price)
                bid_status = self.owner_app.process_bids(bid_obj)
        if bid_status:
            print('Bid placed successfully')
        else:
            print('Bid could not be placed')
        return
                
    def close_item(self, item_id):
        if item_id in self.owner_app.items:
            item = self.owner_app.items[item_id]
            if item.seller_id == self.id and item.status == ItemStatus.BIDDING:
                self.owner_app.close_auction(item)

class Bid:
    def __init__(self, user_id, item_id, bid_price):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.item_id = item_id
        self.bid_price = bid_price
    
class Item:
    def __init__(self, title, base_price, user_id):
        self.title = title
        self.base_price = base_price
        self.bid_price = base_price
        self.status = ItemStatus.BIDDING
        self.seller_id = user_id
        self.buyer_id = None
        self.id = uuid.uuid4()

    
class OnlineAuctionApp:
    def __init__(self):
        self.items = {}
        self.users = {}
        self.bids = []

    def add_user(self, user: User):
        self.users[user.id] = user
        user.owner_app = self
    
    def add_item(self, item: Item):
        self.items[item.id] = item

    def process_bids(self, bid):
        # can expand logic later to handle multiple concurrent bids being placed using semaphore and mutex or other logics
        self.bids.append(bid)
        self.items[bid.item_id].bid_price = bid.bid_price
        return True

    def close_auction(self, item):
        item.status = ItemStatus.SOLD
        return True

if __name__ == '__main__':
    onlineaucapp = OnlineAuctionApp()
    u1 = User('u1', onlineaucapp)
    it1 = Item('it1', 30, u1.id)
    print(onlineaucapp.items)
    u1.list_item(it1)
    print(onlineaucapp.items)
    u2 = User('u2', onlineaucapp)
    u2.place_bid(it1.id, 40)
    u1.close_item(it1.id)
    print(onlineaucapp.bids)
    print(onlineaucapp.users)
