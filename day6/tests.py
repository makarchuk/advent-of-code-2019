import unittest
import main

class OrbitsTest(unittest.TestCase):
    def test_part_1(self):
        orbits_map = main.Map('''
            COM)B
            B)C
            C)D
            D)E
            E)F
            B)G
            G)H
            D)I
            E)J
            J)K
            K)L
            ''')
        self.assertEqual(len(list(orbits_map.all_orbits())), 42)

    def test_part_2(self):
        orbits_map = main.Map('''
            COM)B
            B)C
            C)D
            D)E
            E)F
            B)G
            G)H
            D)I
            E)J
            J)K
            K)L
            K)YOU
            I)SAN
        ''')
        route = orbits_map.find_route()
        self.assertEqual(route, list("KJEDI"))