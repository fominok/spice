import unittest
import parser
import spicemix
import gaussian
from math import exp

from main import find_n_m_size
from stamp_builder import StampBuilder


class ParserStampTests(unittest.TestCase):
    def setUp(self):
        self.entries = {'* Whole line comment': None,
                        'R1 1 2 1000 * Это комментарий':
                        (spicemix.Resistor, 1, 1, 2, 1000),
                        'R2 2 0 1000':
                        (spicemix.Resistor, 2, 2, 0, 1000),
                        'V1 1 0 2':
                        (spicemix.Voltage, 1, 1, 0, 2),
                        'D1 2 0':
                        (spicemix.Diode, 1, 2, 0, None),
                        }
        self.n = 3
        self.m = 1

        self.v0 = 0.8

        i =  1e-12 * (exp(self.v0 / 25.85e-3) - 1)

        self.cut_matrix_a = [[1e-3, -1e-3, 1],
                             [-1e-3, 1e-3 + 1e-3 + i / 25.85e-3, 0],
                             [1, 0, 0],
                             ]
        self.cut_matrix_z = [0, -(i - i / 25.85e-3 * self.v0), 2]

        self.parser = parser.Parser()
        self.builder = StampBuilder(self.n, self.m)

    def test_correct_type_nodes_anything(self):
        comps_linear = []
        comps_diodes = []
        for entry, value in self.entries.items():
            comp = self.parser.next_entry(entry)

            if comp is None and value is not None:
                raise Exception('There is a component but parser returns None')

            if comp is not None:
                self.assertEqual(comp.get_id(), value[1], 'Wrong id')
                self.assertEqual(comp.get_p_node(), value[2], 'Wrong p node')
                self.assertEqual(comp.get_n_node(), value[3], 'Wrong n node')
                self.assertEqual(comp.get_value(), value[4], 'Wrong value')
                assert isinstance(comp, value[0])

                if isinstance(comp, spicemix.Diode):
                    comps_diodes.append(comp)
                else:
                    comps_linear.append(comp)

        for c in comps_linear:
            self.builder.add_component(c)
        for c in comps_diodes:
            c.set_vol_zero(self.v0)
            self.builder.add_component(c)

        n, m = find_n_m_size(comps_linear + comps_diodes)
        self.assertEqual(n, self.n)
        self.assertEqual(m, self.m)

        self.builder.clear_zer()
        builder_a, builder_z = self.builder.get_a_z()
        self.assertEqual(self.cut_matrix_a, builder_a)
        self.assertEqual(self.cut_matrix_z, builder_z)

        gaussian.print_matrix(gaussian.gaussian_elimintaion(self.cut_matrix_a, self.cut_matrix_z))


class GaussianTest(unittest.TestCase):

    """Test for gaussian elimination"""

    def setUp(self):
        self.matrix = [[2, 5, 7], [6, 3, 4], [5, -2, -3]]
        self.matrix_transposed = [[2, 6, 5], [5, 3, -2], [7, 4, -3]]
        self.epic_matrix = [[3, -3, -5, 8], [-3, 2, 4, -6],
                            [2, -5, -7, 5], [-4, 3, 5, -6]]
        self.minor_0_1 = [[6, 4], [5, -3]]
        self.minor_1_2 = [[2, 5], [5, -2]]
        self.det = -1
        self.epic_det = 18

    def test_minor_determinant(self):
        self.assertEqual(self.minor_0_1, gaussian.minor(self.matrix, 0, 1))
        self.assertEqual(self.minor_1_2, gaussian.minor(self.matrix, 1, 2))
        self.assertEqual(self.det, gaussian.determinant(self.matrix))
        self.assertEqual(self.epic_det, gaussian.determinant(self.epic_matrix))
    
    def test_transpose(self):
        self.assertEqual(self.matrix_transposed, gaussian.transpose(self.matrix))


if __name__ == '__main__':
    unittest.main()
