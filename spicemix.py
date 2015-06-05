from abc import ABCMeta, abstractmethod


class Component():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_p_node(self) -> int:
        """ Returns number of positive node """

    @abstractmethod
    def get_n_node(self) -> int:
        """ Returns number of negative node """

    @abstractmethod
    def get_value(self) -> float:
        """ Returns value of characteristic """

    @abstractmethod
    def get_id(self) -> int:
        """ Returns id for this type of component """


class Resistor(Component):
    def __init__(self, identity, resistance, p_node, n_node):
        self.__resistance = resistance
        self.__id = identity
        self.__p_node = p_node
        self.__n_node = n_node

    def get_id(self) -> int:
        return self.__id

    def get_p_node(self) -> int:
        return self.__p_node

    def get_value(self) -> float:
        return self.__resistance

    def get_n_node(self) -> int:
        return self.__n_node


class Voltage(Component):
    def __init__(self, identity, voltage, p_node, n_node):
        self.__voltage = voltage
        self.__id = identity
        self.__p_node = p_node
        self.__n_node = n_node

    def get_id(self) -> int:
        return self.__id

    def get_p_node(self) -> int:
        return self.__p_node

    def get_value(self) -> float:
        return self.__voltage

    def get_n_node(self) -> int:
        return self.__n_node


class Current(Component):
    def __init__(self, identity, current, p_node, n_node):
        self.__current = current
        self.__id = identity
        self.__p_node = p_node
        self.__n_node = n_node

    def get_id(self) -> int:
        return self.__id

    def get_p_node(self) -> int:
        return self.__p_node

    def get_value(self) -> float:
        return self.__current

    def get_n_node(self) -> int:
        return self.__n_node


class Diode(Component):
    def __init__(self, identity, p_node, n_node):
        self.__id = identity
        self.__p_node = p_node
        self.__n_node = n_node
        self.__voltage = None

    def get_id(self) -> int:
        return self.__id

    def get_p_node(self) -> int:
        return self.__p_node

    def get_value(self) -> float:
        return self.__voltage

    def get_n_node(self) -> int:
        return self.__n_node

    def set_voltage(self, vol):
        self.__voltage = vol


def spice_factory(char, id, p_node, n_node, val):

    """Lol nice name"""

    if char == 'R':
        return Resistor(id, val, p_node, n_node)
    if char == 'V':
        return Voltage(id, val, p_node, n_node)
    if char == 'I':
        return Current(id, val, p_node, n_node)
    if char == 'D':
        return Diode(id, p_node, n_node)

    return None
