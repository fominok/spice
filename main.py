import sys

from parser import Parser
from stamp_builder import StampBuilder
from gaussian import gaussian_elimintaion
import spicemix


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


def main(args):
    if len(args) != 2:
        print('Usage: python ' + args[0] + ' input.txt')
        sys.exit()

    parser = Parser()
    components = []

    with open(args[1]) as file:
        for line in file:
            comp = parser.next_entry(line)
            if comp is not None:
                components.append(comp)

    n, m = find_n_m_size(components)
    builder = StampBuilder(n, m)
    for comp in components:
        builder.add_component(comp)
    builder.clear_zer()
    a, z = builder.get_a_z()

    solution = gaussian_elimintaion(a, z)


if __name__ == '__main__':
    main(sys.argv)
