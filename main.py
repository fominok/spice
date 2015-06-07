import sys

from parser import Parser
from stamp_builder import StampBuilder
from gaussian import gaussian_elimintaion, print_matrix
import spicemix
from copy import deepcopy
from math import fabs


start_appr = 0.8
eps = 0.001


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
    comps_linear = []
    comps_diodes = []

    with open(args[1]) as file:
        for line in file:
            comp = parser.next_entry(line)
            if comp is not None:
                if isinstance(comp, spicemix.Diode):
                    comps_diodes.append(comp)
                else:
                    comps_linear.append(comp)

    n, m = find_n_m_size(comps_linear + comps_diodes)
    builder = StampBuilder(n, m)

    for comp in comps_linear:
        builder.add_component(comp)

    # solution = [[start_appr] for x in range(n + m - 1)]
    prev = start_appr

    for d in comps_diodes:
        d.set_vol_zero(start_appr)

    if len(comps_diodes) > 0:
        the_p = comps_diodes[len(comps_diodes) - 1].get_p_node()
        while True:
            prepared_builder = deepcopy(builder)
            for d in comps_diodes:
                prepared_builder.add_component(d)
            prepared_builder.clear_zer()
            a, z = prepared_builder.get_a_z()
            solution = gaussian_elimintaion(a, z)
            print_matrix(solution)
            for d in comps_diodes:
                d.set_vol_zero(solution[the_p - 1])
            dx = fabs(comps_diodes[0].get_value() - prev)
            prev = comps_diodes[0].get_value()
            if dx < eps:
                break # why python hasnt do while ?
        
    else:
        builder.clear_zer()
        a, z = builder.get_a_z()
        solution = gaussian_elimintaion(a, z)

    form_output(args[2], solution, n, m)


if __name__ == '__main__':
    main(sys.argv)
