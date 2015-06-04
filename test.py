import unittest
import parser
import spicemix

from main import find_n_m_size
from stamp_builder import StampBuilder


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.entries = {'* Whole line comment': None,
                        'R1 1 2 1 * Это комментарий':
                        (spicemix.Resistor, 1, 1, 2, 1),
                        'R2 2 0 2':
                        (spicemix.Resistor, 2, 2, 0, 2),
                        'R3 3 0 3':
                        (spicemix.Resistor, 3, 3, 0, 3),
                        'V1 1 0 2':
                        (spicemix.Voltage, 1, 1, 0, 2),
                        'I1 2 3 0.3':
                        (spicemix.Current, 1, 2, 3, 0.3),
                        }
        self.n = 4
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

        builder_a, builder_z = self.builder.get_a_z()
        self.assertEqual(self.matrix_a, builder_a)
        self.assertEqual(self.matrix_z, builder_z)

        self.builder.clear_zer()
        builder_a, builder_z = self.builder.get_a_z()
        self.assertEqual(self.cut_matrix_a, builder_a)
        self.assertEqual(self.cut_matrix_z, builder_z)


if __name__ == '__main__':
    unittest.main()
