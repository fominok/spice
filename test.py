import unittest
import parser
import spicemix
import gaussian

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
                        'D1 0 2':
                        (spicemix.Diode, 1, 0, 2, 0.8),
                        }
        self.n = 3
        self.m = 1

        self.matrix_a = [[1/2 + 1/3, 0,  -0.5, -1/3, -1],
                         [0, 1, -1, 0, 1],
                         [-0.5, -1, 1.5, 0, 0],
                         [-1/3, 0, 0, 1/3, 0],
                         [-1, 1, 0, 0, 0]
                         ]

        self.matrix_z = [0, 0, -0.3, 0.3, 2]

        self.cut_matrix_a = [[1, -1, 0, 1],
                             [-1, 1.5, 0, 0],
                             [0, 0, 1/3, 0],
                             [1, 0, 0, 0]
                             ]

        self.cut_matrix_z = [0, -0.3, 0.3, 2]

        self.parser = parser.Parser()
        self.builder = StampBuilder(self.n, self.m)

    def test_correct_type_nodes_anything(self):
        comps = []
        for entry, value in self.entries.items():
            comp = self.parser.next_entry(entry)
            if isinstance(comp, spicemix.Diode):
                comp.set_voltage(0.8)

            if comp is None and value is not None:
                raise Exception('There is a component but parser returns None')

            if comp is not None:
                self.builder.add_component(comp)
                comps.append(comp)
                assert isinstance(comp, value[0])
                self.assertEqual(comp.get_id(), value[1], 'Wrong id')
                self.assertEqual(comp.get_p_node(), value[2], 'Wrong p node')
                self.assertEqual(comp.get_n_node(), value[3], 'Wrong n node')
                self.assertEqual(comp.get_value(), value[4], 'Wrong value')

        n, m = find_n_m_size(comps)
        self.assertEqual(n, self.n)
        self.assertEqual(m, self.m)

        # builder_a, builder_z = self.builder.get_a_z()
        # self.assertEqual(self.matrix_a, builder_a)
        # self.assertEqual(self.matrix_z, builder_z)

        # self.builder.clear_zer()
        # builder_a, builder_z = self.builder.get_a_z()
        # self.assertEqual(self.cut_matrix_a, builder_a)
        # self.assertEqual(self.cut_matrix_z, builder_z)


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
