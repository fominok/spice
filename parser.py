import re
import spicemix


class Parser():

    """The parser class."""

    def next_entry(self, entry: str) -> spicemix.Component:
        """Parse next entry and return Component"""
        entry = entry.strip()
        try:
            if entry[0] == '*':
                return None # Omg in one line it doesnt work
        except IndexError as e:
            return None

        # Warning: regular expressions here
        re_str = '^(?P<type>\w)(?P<id>\d+)\s(?P<p_node>\d+)\s(?P<n_node>\d+)\s(?P<val>[-+]?\d*\.\d+|\d+)'
        parse_re = re.compile(re_str, re.A)
        match = parse_re.search(entry)

        char = match.group('type')
        id = int(match.group('id'))
        p_node = int(match.group('p_node'))
        n_node = int(match.group('n_node'))
        val = float(match.group('val'))

        return spicemix.spice_factory(char, id, p_node, n_node, val)
