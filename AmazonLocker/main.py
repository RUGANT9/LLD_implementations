'''
Docstring for AmazonLocker.main

Core Entities:
-> User
-> Item
-> Locker
'''

from enum import Enum
import uuid
import datetime


class CompartmentSize(Enum):
    SMALL = 'Small'
    MEDIUM = 'Medium'
    LARGE = 'Large'

class Utils:
    @staticmethod
    def generate_access_code():
        return (uuid.uuid4(), datetime.datetime.now() + datetime.timedelta(hours=24))
    
class User:
    def __init__(self):
        self.user_id = uuid.uuid4()
        self.access_codes = []  # List of (code, locker_id) tuples

class Item:
    def __init__(self, item_size: CompartmentSize, item_owner: User = None):
        self.item_id = uuid.uuid4()
        self.item_size = item_size
        self.item_owner = item_owner

class Locker:
    def __init__(self):
        self.locker_id = uuid.uuid4()
        self.compartments = {
            CompartmentSize.SMALL: 0,
            CompartmentSize.MEDIUM: 0,
            CompartmentSize.LARGE: 0
        }
        self.codes_in_use = {}

    def place_item(self, item: Item):
        if self.compartments[item.item_size] > 0:
            self.compartments[item.item_size] -= 1
            code = Utils.generate_access_code()
            item.item_owner.access_codes.append((code[0], self.locker_id))
            self.codes_in_use[code[0]] = (item, code[1])
            print(f'Item placed in locker. Retrieval code: {code[0]} with expiry {code[1]}')
            return True
        else:
            print('No available compartment for the item size.')
            return False

    def retrieve_item(self, code):
        if code in self.codes_in_use and self.codes_in_use[code][1] > datetime.datetime.now():
            item = self.codes_in_use[code][0]
            del self.codes_in_use[code]
            self.compartments[item.item_size] += 1
            print('Item retrieved successfully.')
            return item
        else:
            print('Access denied. This code does not belong to the user.')
            return None

if __name__ == '__main__':
    # Example usage
    locker = Locker()
    locker.compartments[CompartmentSize.SMALL] = 2  # Adding compartments for testing

    user = User()
    item = Item(CompartmentSize.SMALL, user)

    # Place item in locker
    locker.place_item(item)

    # Retrieve item using the access code
    access_code = user.access_codes[0][0]
    locker.retrieve_item(access_code)