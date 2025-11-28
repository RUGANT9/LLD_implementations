from enum import Enum

class CarType(Enum):
    BASIC = 'Basic'
    LUXURY = 'Luxury'
    COMFORT = 'Comfort'
    SPACE = 'Space'

class DriverStatus(Enum):
    IDLE = 'IDLE'
    OFFLINE = 'OFFLINE'
    BUSY = 'BUSY'

class CustomerStatus(Enum):
    IDLE = 'IDLE'
    BUSY = 'BUSY'

class Car:
    def __init__(self, name: str, number: str, car_type: CarType):
        self.name = name
        self.number = number
        self.type = car_type


class Ride:
    @staticmethod
    def confirm_ride(customer_name, driver_name, source, destination):
        ride_obj = {'customer': customer_name, 'driver':driver_name, 'source': source, 'destination': destination}
        return ride_obj
    

class RideShareApp(Ride):
    def __init__(self, drivers = None, customers = None):
        self.drivers = drivers if drivers is not None else []
        self.customers = customers if customers is not None else []
        self.rides = []
    

    def book_ride(self, customer, destination):
        if customer in self.customers and customer.customer_status == CustomerStatus.IDLE:
            for d in self.drivers:
                if d.location == customer.location and d.driver_status == DriverStatus.IDLE:
                    r_obj = Ride.confirm_ride(customer.name, d.name, customer.location, destination)
                    d.driver_status = DriverStatus.BUSY
                    customer.customer_status = CustomerStatus.BUSY
                    d.current_customer = customer
                    customer.current_driver = d
                    self.rides.append(r_obj)
    
    def end_ride(self, driver, customer):
        for r in self.rides:
            if r['driver'] == driver.name:
                self.rides.remove(r)
                driver.driver_status = DriverStatus.IDLE
                customer.customer_status = CustomerStatus.IDLE
                customer.current_driver = None
                driver.current_customer = None
                return True
        return False
    
class Customer():
    def __init__(self, name: str, location: str, owner_app: RideShareApp = None, customer_status: CustomerStatus = CustomerStatus.IDLE, current_driver = None):
        self.name = name
        self.location = location
        self.owner_app = owner_app
        self.customer_status = customer_status
        self.current_driver = current_driver
    
    def book_my_ride(self, customer, destination):
        RideShareApp.book_ride(self.owner_app, customer, destination)
    

class Driver():
    def __init__(self, name: str, car: Car = None, location: str = None, driver_status: DriverStatus = DriverStatus.IDLE, owner_app: RideShareApp = None, current_customer: Customer = None):
        self.name = name
        self.car = car
        self.location = location
        self.driver_status = driver_status
        self.owner_app = owner_app
        self.current_customer = current_customer
    
    def update_car(self, car: Car):
        self.car = car
    
    def update_location(self, location: str):
        self.location = location
    
    def update_status(self, updated_driver_status: DriverStatus):
        self.driver_status = updated_driver_status
    
    def end_my_ride(self, driver):
        RideShareApp.end_ride(self.owner_app, driver, driver.current_customer)

if __name__ == '__main__':
    cust1 = Customer('cust_1', 'Bellevue')
    cust2 = Customer('cust_2', 'Seattle')
    car1 = Car('Honda', '343BB', CarType.BASIC)
    d1 = Driver('driver_1', car1, 'Bellevue', DriverStatus.IDLE)
    rideshareapp = RideShareApp([], [])
    rideshareapp.customers = [cust1, cust2]
    rideshareapp.drivers = [d1]
    cust1.owner_app = rideshareapp
    d1.owner_app = rideshareapp
    cust1.book_my_ride(cust1, 'Redmond')
    print(rideshareapp.rides)
    d1.end_my_ride(d1)
    print(rideshareapp.rides)
