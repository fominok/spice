import sys

from parser import Parser
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

    return max_value + voltage_number + 1


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


if __name__ == '__main__':
    main(sys.argv)
