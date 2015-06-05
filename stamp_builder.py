import spicemix
from math import exp


class StampBuilder():

    """Builds matrix from components(spicemix.Component)"""

    def __init__(self, nodes_count, vols_count):
        self.__n = nodes_count
        self.__m = vols_count
        self.__npm = self.__n + self.__m

        self.__matrix_a = [[0 for x in range(self.__npm)] for y in range(self.__npm)]
        self.__matrix_z = [0 for x in range(self.__npm)]

        self.__uncl = True

    def get_a_z(self):
        return self.__matrix_a, self.__matrix_z

    def add_component(self, component: spicemix.Component):

        """Some epics here"""

        p_num = component.get_p_node()
        n_num = component.get_n_node()
        val = component.get_value()
        col_row = self.__n + component.get_id() - 1

        if isinstance(component, spicemix.Resistor):
            self.__matrix_a[p_num][n_num] -= 1/val
            self.__matrix_a[n_num][p_num] -= 1/val
            self.__matrix_a[p_num][p_num] += 1/val
            self.__matrix_a[n_num][n_num] += 1/val

        elif isinstance(component, spicemix.Voltage):
            self.__matrix_a[p_num][col_row] = 1
            self.__matrix_a[n_num][col_row] = -1
            self.__matrix_a[col_row][p_num] = 1
            self.__matrix_a[col_row][n_num] = -1
            self.__matrix_z[col_row] = val

        elif isinstance(component, spicemix.Current):
            self.__matrix_z[p_num] = -val
            self.__matrix_z[n_num] = val

        elif isinstance(component, spicemix.Diode):
            vt = 25.85e-3
            i = 1e-12 * (exp(val / vt) - 1)
            g = i / vt
            ieq = i - g * val

            # print('G = ' + str(g))
            # print('Id = ' + str(ieq))

            self.__matrix_a[p_num][n_num] -= g
            self.__matrix_a[n_num][p_num] -= g
            self.__matrix_a[p_num][p_num] += g
            self.__matrix_a[n_num][n_num] += g

            self.__matrix_z[p_num] = -ieq
            self.__matrix_z[n_num] = ieq


    def clear_zer(self):
        if self.__uncl:
            new_mat_a = [[0 for x in range(self.__npm - 1)] for y in range(self.__npm - 1)]
            for x in range(self.__npm - 1):
                for y in range(self.__npm - 1):
                    new_mat_a[x][y] = self.__matrix_a[x + 1][y + 1]
            self.__matrix_a = new_mat_a
            self.__matrix_z = [z for z in self.__matrix_z[1:]]
            self.__uncl = False
