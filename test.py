import unittest
import parser
import spicemix


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
                        'V12 2 3 -0.3':
                        (spicemix.Voltage, 12, 2, 3, -0.3),
                        }
                       

        self.parser = parser.Parser()

    def test_correct_type_nodes_anything(self):
        for entry, value in self.entries.items():
            comp = self.parser.next_entry(entry)

            if comp is None and value is not None:
                raise Exception('There is a component but parser returns None')

            if comp is not None:
                assert isinstance(comp, value[0])
                self.assertEqual(comp.get_id(), value[1], 'Wrong id')
                self.assertEqual(comp.get_p_node(), value[2], 'Wrong p node')
                self.assertEqual(comp.get_n_node(), value[3], 'Wrong n node')
                self.assertEqual(comp.get_value(), value[4], 'Wrong value')


if __name__ == '__main__':
    unittest.main()
