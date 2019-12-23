from collections import deque


class Building:
    """Framework for buildings"""

    def send_vehicle(self):
        """
        Send vehicle from the base building.
        """
        raise NotImplementedError


class Factory(Building):
    """
    The Factory object has containers in stock.

    Args:
        self.stock (deque): The stock is used for tracing containers.
        self.vehicles (dict): Factory owned vehicles.

    """

    def __init__(self, stock):
        self.vehicles = {}
        self.stock = deque([i, 0] for i in stock)
        super().__init__()

    def send_vehicle(self):
        cargo = self.stock.popleft()

        # Choosing the vehicle that will return earlier from transportation
        vehicle = min(self.vehicles, key=self.vehicles.get)
        address = Warehouse.warehouses[cargo[0]]

        if cargo[0] == 'A':
            cargo[1] += port.travel_time + self.vehicles[vehicle]
            vehicle.transportation(cargo, address)
        else:
            cargo[1] += address.travel_time + self.vehicles[vehicle]
            vehicle.transportation(cargo, address)


class Port(Building):
    """
    The Port object has containers in stock.

    Args:
        travel_time (int): Travel time to the port.
        self.stock (deque): The stock is used for tracing containers.
        self.vehicles (dict): Factory owned vehicles.

    """

    def __init__(self, travel_time):
        self.stock = deque()
        self.vehicles = {}
        self.travel_time = travel_time
        super().__init__()

    def send_vehicle(self):
        cargo = self.stock.popleft()
        vehicle = min(self.vehicles, key=self.vehicles.get)
        address = Warehouse.warehouses[cargo[0]]
        if cargo[1] < self.vehicles[vehicle]:
            cargo[1] = address.travel_time + self.vehicles[vehicle]
            self.vehicles[vehicle] += address.travel_time * 2
        else:
            self.vehicles[vehicle] = cargo[1] + address.travel_time * 2
            cargo[1] += address.travel_time

        address.stock.append(cargo)


class Warehouse(Building):
    warehouses = {}

    def __init__(self, name, travel_time):
        self.travel_time = travel_time
        self.name = name
        self.vehicles = {}
        self.stock = deque()
        Warehouse.warehouses[name] = self
        super().__init__()

    def __str__(self):
        return f'Warehouse {self.name}'

    def __repr__(self):
        return f'Warehouse {self.name}'

    def send_vehicle(self):
        pass


class Transport:
    """Framework for transports
    Args:
        base (str): Base for transport.
    """

    def __init__(self, base):
        self.base = base
        self.base.vehicles[self] = 0

    def transportation(self, cargo, address):
        """
        Send vehicle to the specified warehouse.
        """
        raise NotImplementedError


class Truck(Transport):
    def transportation(self, cargo, address):
        if address == warehouse_a:
            port.stock.append(cargo)
            self.base.vehicles[self] += port.travel_time * 2
        else:
            address.stock.append(cargo)
            self.base.vehicles[self] += address.travel_time * 2


class Ship(Transport):
    def transportation(self, cargo, address):
        address.stock.append(cargo)
        self.base.vehicles[self] += address.travel_time * 2 + 1


if __name__ == '__main__':
    inp = 'ABBBABAAABBB'
    factory = Factory(inp)
    warehouse_a = Warehouse('A', 4)
    warehouse_b = Warehouse('B', 5)
    port = Port(1)

    truck1 = Truck(factory)
    truck2 = Truck(factory)
    ship = Ship(port)

    while factory.stock:
        factory.send_vehicle()

    while port.stock:
        port.send_vehicle()

    max_a = max(warehouse_a.stock)[1]
    max_b = max(warehouse_b.stock)[1]

    print(max(max_a, max_b))
