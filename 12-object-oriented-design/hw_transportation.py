from collections import deque
import logging


class Building:
    """Framework for buildings"""

    def __init__(self, stock):
        self.vehicles = []
        self.stock = stock

    def add_vehicles(self, *args):
        self.vehicles.extend(args)

    def attach_cargo(self, cargo):
        self.stock.append(cargo)

    def detach_cargo(self):
        return self.stock.popleft()

    @property
    def is_stock(self):
        return self.stock

    def find_vehicle_with_less_travel_time(self):
        min_val, vehicle = float('inf'), None
        for v in self.vehicles:
            if v.travel_time < min_val:
                min_val = v.travel_time
                vehicle = v
        return vehicle


class Factory(Building):
    """Building from which containers will be send."""

    def __init__(self, stock):
        self.stock = deque([i, 0] for i in stock)
        super(Factory, self).__init__(self.stock)

    def factory_depart(self):

        # Define cargo, address, vehicle to depart from factory
        cargo = self.detach_cargo()
        address = Warehouse.warehouses[cargo[0]]
        vehicle = self.find_vehicle_with_less_travel_time()

        # If there is port on the way add additional time
        if address.has_port:
            cargo[1] += address.port.travel_time + vehicle.travel_time
            vehicle.travel_time += address.port.travel_time * 2
            address.port.attach_cargo(cargo)

            # Change vehicle to ship
            vehicle = address.port.find_vehicle_with_less_travel_time()
            travel.send_vehicle_from_port(cargo, address, vehicle)
        else:
            travel.send_vehicle_from_factory(cargo, address, vehicle)


class Port(Building):
    """Intermediate building on the way between factory and warehouse."""

    def __init__(self, travel_time):
        self.travel_time = travel_time
        self.stock = deque()
        super(Port, self).__init__(self.stock)


class Warehouse:
    """Building to which containers will be send"""
    warehouses = {}

    def __init__(self, name, travel_time, port=None):
        self.travel_time = travel_time
        self.name = name
        self.stock = deque()
        self.port = port
        Warehouse.warehouses[name] = self

    @property
    def has_port(self):
        return self.port

    def attach_cargo(self, cargo):
        self.stock.append(cargo)


class Travelling:
    def __init__(self, factory):
        self.factory = factory

    def start_travel(self):
        self.factory.factory_depart()

    def send_vehicle_from_port(self, cargo, address, vehicle):
        """Sends vehicle from port to deliver containers."""
        if cargo[1] < vehicle.travel_time:
            cargo[1] = address.travel_time + vehicle.travel_time
            vehicle.travel_time += address.travel_time * 2
        else:
            vehicle.travel_time = cargo[1] + address.travel_time * 2
            cargo[1] += address.travel_time

        address.attach_cargo(cargo)
        address.port.detach_cargo()


    def send_vehicle_from_factory(self, cargo, address, vehicle):
        """Sends vehicle from factory to deliver containers."""
        if cargo[1] < vehicle.travel_time:
            cargo[1] = address.travel_time + vehicle.travel_time
            vehicle.set_travel_time(address.travel_time * 2)

        # Ready to take cargo immediately
        else:
            vehicle.set_travel_time(cargo[1] + address.travel_time * 2)
            cargo[1] += address.travel_time
        address.attach_cargo(cargo)
        logging.info(cargo)


class Transport:
    """Vehicle to transport containers."""

    def __init__(self):
        self.cargo = deque()
        self.travel_time = 0

    def set_travel_time(self, time):
        self.travel_time += time


if __name__ == '__main__':
    inp = input('Enter container sequence: ')

    logging.basicConfig(filename="log_info.log",
                        filemode="w", level=logging.INFO)
    logging.info("Program started")

    port1 = Port(1)
    port2 = Port(1)
    warehouse_a = Warehouse('A', 4, port=port1)
    warehouse_b = Warehouse('B', 5, port=None)

    factory1 = Factory(inp)

    truck1 = Transport()
    truck2 = Transport()

    ship_a = Transport()
    ship_b = Transport()

    factory1.add_vehicles(truck1, truck2)
    port1.add_vehicles(ship_a)
    port2.add_vehicles(ship_b)

    travel = Travelling(factory1)

    while factory1.stock:
        travel.start_travel()

    max_a = max(warehouse_a.stock)[1]
    max_b = max(warehouse_b.stock)[1]
    time = max(max_a, max_b)
    print(time)
    logging.info(f"Number of hours that it would take to get containers "
                 f"delivered: {time} ")
    logging.info("Finished")
    print(factory1.stock)
    print(warehouse_a.stock)
    print(warehouse_b.stock)
