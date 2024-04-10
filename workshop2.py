class Engine:
    """
    this class represent an engine and its characteristics

    Parameters:
      type_ (str): engine type
      power (int): engine power
      weight (float): engine weight
    """

    def __init__(self, type_: str, power: int, weight: float):
        self.type_ = type_
        self.power = power
        self.weight = weight


class Vehicle:
    """
    This is a generic class that represent a vehicle

    Parameters:
     type_ (str): vehicle type
     engine (Engine): engine used by the vehicle
     chassis (str): type of chassis used in the vehicle
     model (str): name of the vehicle
     year (int): year of manufacture

    funtions:
     calculate_gas_consumption(): calculates engine fuel consumption
    """

    def __init__(self, type_: str, engine: Engine, chassis: str, model: str, year: int):
        self.type_ = type_
        self.engine = engine
        self.chassis = chassis
        self.model = model
        self.year = year

    def calculate_gas_consumption(self) -> float:
        if self.chassis == "A":
            return (
                1.1 * float(self.engine.power) + 0.2 * float(self.engine.weight) - 0.3
            )
        elif self.chassis == "B":
            return (
                1.1 * float(self.engine.power) + 0.2 * float(self.engine.weight) - 0.5
            )


class Car(Vehicle):
    """
    this class represent a car
    """

    def __init__(self, type_, engine, chassis, model, year):
        super().__init__(type_, engine, chassis, model, year)


class Truck(Vehicle):
    """
    this class represent a truck
    """

    def __init__(self, type_, engine, chassis, model, year):
        super().__init__(type_, engine, chassis, model, year)


class Yacht(Vehicle):
    """
    this class represent a yacht
    """

    def __init__(self, type_, engine, chassis, model, year):
        super().__init__(type_, engine, chassis, model, year)


class Motorcycle(Vehicle):
    """
    this class represent a motorcycle
    """

    def __init__(self, type_, engine, chassis, model, year):
        super().__init__(type_, engine, chassis, model, year)

class user:
    """
    
    """
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def authenticate(self, username, password)-> bool:
        for elem in users:
            if elem.username == self._username and elem.password == self._password:
                return True
        return False

    


list_vehicles = []
list_engines = []
users = []


def new_engine():
    print("enter engine type")
    engine_type = input()
    print("enter engine power")
    engine_power = input()
    print("enter engine weight")
    engine_weight = input()
    enginet = Engine(engine_type, engine_power, engine_weight)
    list_engines.append(enginet)
    return enginet


def new_vehicle():
    print("what type of vehicle do you want to create? (car, truck, yacht, motorcycle)")
    vehicle_type = input()  # poner comprobacion
    if vehicle_type not in ["car", "truck", "yacht", "motorcycle"]:
        raise ValueError("incorrect vehicle type")
    print("enter model")
    model = input()
    print("enter year")
    year = input()
    print("enter chassis (A or B)")
    chassis = input()  # poner comprobacion
    if chassis not in ["A", "B"]:
        raise ValueError("incorrect chassis type")
    enginet = new_engine()

    if vehicle_type == "car":

        car = Car(vehicle_type, enginet, chassis, model, year)
        list_vehicles.append(car)

    elif vehicle_type == "truck":

        truck = Truck(vehicle_type, enginet, chassis, model, year)
        list_vehicles.append(truck)

    elif vehicle_type == "yacht":

        yacht = Yacht(vehicle_type, enginet, chassis, model, year)
        list_vehicles.append(yacht)

    elif vehicle_type == "motorcycle":

        bike = Motorcycle(vehicle_type, enginet, chassis, model, year)
        list_vehicles.append(bike)




def main():
    while True:
        l = int(input("1-login \n 2-register \n 0-exit \n"))
        if l == 1:
            if authenticate():
                while True:

                    print(
                        "what you want to do? \n 1-create vehicles \n 2-show vehicles \n 3-create engine \n 4-show engines \n 0-exit"
                    )
                    n = int(input())

                    if n == 1:
                        new_vehicle()

                    elif n == 2:
                        for elem in list_vehicles:
                            print(
                                f"-vehicle type: {elem.type_}, model: {elem.model}, chasis: {elem.chassis}, year: {elem.year}, engine type: {elem.engine.type_}, engine power: {elem.engine.power}, engine weight: {elem.engine.weight}, gas consumption: {elem.calculate_gas_consumption()}"
                            )

                    elif n == 3:
                        new_engine()

                    elif n == 4:
                        for elem in list_engines:
                            print(
                                f"engine type: {elem.type_}, engine power: {elem.power}, engine weight: {elem.weight}"
                            )

                    elif n == 0:
                        break

                    else:
                        print("chose a correct option")
            else:
                print("user or password incorrect")
        elif l == 2:
            print("enter username")
            username = input()
            print("enter password")
            password = input()
            user_ = user(username, password)
            users.append(user_)
        elif l == 0:
            break
        else:
            print("chose a correct option")


if __name__ == "__main__":
    main()
