import sys
from copy import deepcopy
from math import fabs

from parser import Parser
from stamp_builder import StampBuilder
from gaussian import gaussian_elimintaion, print_matrix
import spicemix

start_appr = 0.8
eps = 0.00001

def find_n_m_size(comp_list):

    """Function to get the size of matrix (N + M)"""

    max_value = 0
    voltage_number = 0

    for comp in comp_list:
        p = comp.get_p_node()
        n = comp.get_n_node()
        max = p if p > n else n
        if max > max_value:
            max_value = max
        if isinstance(comp, spicemix.Voltage):
            voltage_number += 1

    return max_value + 1, voltage_number


def form_output(file, solution, n, m):
    with open(file, 'w') as out:
        for i in range(n - 1):
            out.write('V%s: %s volts.\n' % (str(i + 1), str(solution[i])))
        for i in range(m):
            out.write('I(V%s): %s amps.\n' % (str(i + 1), str(solution[n + i - 1])))


def main(args):
    if len(args) != 3:
        print('Usage: python ' + args[0] + ' input.txt output.txt')
        sys.exit()

    parser = Parser()
    components = []
    diodes = []

    with open(args[1]) as file:
        for line in file:
            comp = parser.next_entry(line)
            if comp is not None:
                if not isinstance(comp, spicemix.Diode):
                    components.append(comp)
                elif isinstance(comp, spicemix.Diode):
                    diodes.append(comp)

    n, m = find_n_m_size(components)
    builder = StampBuilder(n, m)
    for comp in components:
        builder.add_component(comp)

    solution = [[start_appr] for x in range(n + m - 1)]
    prev = start_appr

    for d in diodes:
        d.set_voltage(solution[d.get_p_node() - 1][0])

    if len(diodes) > 0:
        while True:
            prepared_builder = deepcopy(builder)
            for d in diodes:
                prepared_builder.add_component(d)
            prepared_builder.clear_zer()
            a, z = prepared_builder.get_a_z()
            solution = gaussian_elimintaion(a, z)
            for d in diodes:
                d.set_voltage(solution[d.get_p_node() - 1])
            dx = fabs(diodes[0].get_value() - prev)
            prev = diodes[0].get_value()
            if dx < eps:
                break # why python hasnt do while ?
        
    else:
        builder.clear_zer()
        a, z = builder.get_a_z()
        solution = gaussian_elimintaion(a, z)

    form_output(args[2], solution, n, m)
    

if __name__ == '__main__':
    main(sys.argv)
