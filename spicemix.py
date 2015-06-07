from abc import ABCMeta, abstractmethod
from math import exp


vt = 25.85e-3
isat = 1e-12


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
    def __init__(self, identity, p_node, n_node, resistance):
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
    def __init__(self, identity, p_node, n_node, voltage):
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
    def __init__(self, identity, p_node, n_node, current):
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
        self.__vol_zero = None

    def get_id(self) -> int:
        return self.__id

    def get_p_node(self) -> int:
        return self.__p_node

    def get_value(self) -> float:
        return self.__vol_zero

    def get_n_node(self) -> int:
        return self.__n_node

    def set_vol_zero(self, vol):
        self.__vol_zero = vol
        self.__i = isat * (exp(self.__vol_zero / vt) - 1)
        self.__g = self.__i / vt
        self.__ieq = self.__i - self.__g * self.__vol_zero

    def get_equivalents(self):
        return spice_factory('R', int(str(self.__id) + '0'), self.__p_node, self.__n_node, 1 / self.__g), \
               spice_factory('I', int(str(self.__id) + '0'), self.__p_node, self.__n_node, self.__ieq)



def spice_factory(char, id, p_node, n_node, val):

    """Lol nice name"""

    if char == 'R':
        return Resistor(id, p_node, n_node, val)
    if char == 'V':
        return Voltage(id, p_node, n_node, val)
    if char == 'I':
        return Current(id, p_node, n_node, val)
    if char == 'D':
        return Diode(id, p_node, n_node)

    return None
