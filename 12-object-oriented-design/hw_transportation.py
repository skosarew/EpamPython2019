from collections import deque
import logging


class Building:
    """Framework for buildings"""

    def __init__(self):
        self.vehicles = {}

    def add_vehicles(self, *args):
        for arg in args:
            self.vehicles[arg] = 0


class Factory(Building):
    """Building from which containers will be send."""

    def __init__(self, stock):
        self.stock = deque([i, 0] for i in stock)
        super(Factory, self).__init__()


class Port(Building):
    """Intermediate building on the way between factory and warehouse."""

    def __init__(self, travel_time):
        self.travel_time = travel_time
        self.stock = deque()
        super(Port, self).__init__()


class Warehouse:
    """Building to which containers will be send"""
    warehouses = {}

    def __init__(self, name, travel_time, port=None):
        self.travel_time = travel_time
        self.name = name
        self.stock = deque()
        self.port = port
        Warehouse.warehouses[name] = self


class Transport:
    """Vehicle to transport containers."""

    def __init__(self):
        self.cargo = deque()


def transportation(building):
    """Returns cargo, address to deliver and vehicle who will transport"""
    cargo = building.stock.popleft()
    address = Warehouse.warehouses[cargo[0]]
    vehicle = min(building.vehicles, key=building.vehicles.get)
    return cargo, address, vehicle


def send_vehicle_from_port(port):
    """Sends vehicle from port to deliver containers."""
    cargo, address, vehicle = transportation(port)

    if cargo[1] < port.vehicles[vehicle]:
        cargo[1] = address.travel_time + port.vehicles[vehicle]
        port.vehicles[vehicle] += address.travel_time * 2
    else:
        port.vehicles[vehicle] = cargo[1] + address.travel_time * 2
        cargo[1] += address.travel_time
    address.stock.append(cargo)
    logging.info(cargo)


def send_vehicle(factory):
    """Sends vehicle from factory to deliver containers."""
    while factory.stock:
        cargo, address, vehicle = transportation(factory)

        # If there is port on the way
        if address.port:
            cargo[1] += address.port.travel_time + factory.vehicles[vehicle]
            factory.vehicles[vehicle] += address.port.travel_time * 2
            address.port.stock.append(cargo)
            while address.port.stock:
                send_vehicle_from_port(address.port)
        else:
            # If vehicle still in on the way add to travel time of cargo
            # journey time of vehicle
            if cargo[1] < factory.vehicles[vehicle]:
                cargo[1] = address.travel_time + factory.vehicles[vehicle]
                factory.vehicles[vehicle] += address.travel_time * 2

            # Ready to take cargo immediately
            else:
                factory.vehicles[vehicle] = cargo[1] + address.travel_time * 2
                cargo[1] += address.travel_time
            address.stock.append(cargo)
            logging.info(cargo)


if __name__ == '__main__':
    inp = input('Enter container sequence: ')

    logging.basicConfig(filename="log_info.log",
                        filemode="w", level=logging.INFO)
    logging.info("Program started")

    port1 = Port(1)
    port2 = Port(1)
    warehouse_a = Warehouse('A', 4, port=port1)
    warehouse_b = Warehouse('B', 5, port=None)

    factory = Factory(inp)

    truck1 = Transport()
    truck2 = Transport()

    ship_a = Transport()
    ship_b = Transport()

    factory.add_vehicles(truck1, truck2)
    port1.add_vehicles(ship_a)
    port2.add_vehicles(ship_b)

    send_vehicle(factory)
    max_a = max(warehouse_a.stock)[1]
    max_b = max(warehouse_b.stock)[1]
    time = max(max_a, max_b)
    print(time)
    logging.info(f"Number of hours that it would take to get containers "
                 f"delivered: {time} ")
    logging.info("Finished")
