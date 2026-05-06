import unittest

from parser.portal_parser import PortalParser


class PortalParserTests(unittest.TestCase):
    def test_uses_map_145_reverse_portals_to_fill_destination_coordinates(self):
        parser = PortalParser("./input", "map")

        groups = parser.insert_portals([
            ["c_map", "0", "145", "1"],
            ["gp", "87", "6", "146", "-1", "3", "0"],
            ["gp", "104", "87", "146", "-1", "5", "0"],
            ["gp", "115", "117", "146", "-1", "7", "0"],
            ["gp", "125", "168", "146", "-1", "8", "0"],
            ["c_map", "0", "146", "1"],
            ["gp", "2", "85", "145", "-1", "0", "0"],
            ["gp", "3", "118", "145", "-1", "1", "0"],
            ["gp", "3", "169", "145", "-1", "2", "0"],
            ["gp", "9", "6", "145", "-1", "3", "0"],
        ])

        destinations = {
            (p.source_map_x, p.source_map_y): (p.destination_map_x, p.destination_map_y)
            for p in groups[146]
            if p.destination_map_id == 145
        }

        self.assertEqual({
            (2, 85): (104, 87),
            (3, 118): (115, 117),
            (3, 169): (125, 168),
            (9, 6): (87, 6),
        }, destinations)

    def test_uses_transition_landing_to_fill_single_unmatched_destination(self):
        parser = PortalParser("./input", "map")

        groups = parser.insert_portals([
            ["c_map", "0", "150", "1"],
            ["gp", "171", "170", "98", "-1", "0", "0"],
            ["c_map", "0", "150", "0"],
            ["at", "2073308", "98", "7", "35", "2", "0", "6", "1", "-1"],
            ["c_map", "0", "98", "1"],
        ])

        portal = groups[150][0]

        self.assertEqual(98, portal.destination_map_id)
        self.assertEqual((7, 35), (portal.destination_map_x, portal.destination_map_y))

    def test_skips_removed_nosville_portal(self):
        parser = PortalParser("./input", "map")

        groups = parser.insert_portals([
            ["c_map", "0", "1", "1"],
            ["gp", "17", "52", "2547", "-1", "0", "0"],
            ["gp", "79", "2", "2", "-1", "1", "0"],
        ])

        sources = {(p.source_map_x, p.source_map_y) for p in groups[1]}

        self.assertNotIn((17, 52), sources)
        self.assertIn((79, 2), sources)

    def test_adds_lord_draco_metadata_to_dragon_cavern_raid_portal(self):
        parser = PortalParser("./input", "map")

        groups = parser.insert_portals([
            ["c_map", "0", "2547", "1"],
            ["gp", "23", "6", "4996", "8", "0", "0"],
        ])

        portal = groups[2547][0]

        self.assertEqual(8, portal.type)
        self.assertEqual(16, portal.raid_type)
        self.assertEqual(4996, portal.map_name_id)

    def test_adds_metadata_to_known_packet_raid_portals(self):
        parser = PortalParser("./input", "map")

        groups = parser.insert_portals([
            ["c_map", "0", "282", "1"],
            ["gp", "14", "40", "4996", "8", "0", "0"],
            ["c_map", "0", "283", "1"],
            ["gp", "16", "6", "4996", "8", "0", "0"],
            ["c_map", "0", "2515", "1"],
            ["gp", "19", "3", "4996", "8", "0", "0"],
            ["c_map", "0", "2567", "1"],
            ["gp", "16", "1", "4996", "8", "0", "0"],
            ["c_map", "0", "2635", "1"],
            ["gp", "57", "38", "4996", "8", "0", "0"],
            ["c_map", "0", "2636", "1"],
            ["gp", "20", "22", "4996", "8", "0", "0"],
            ["c_map", "0", "2638", "1"],
            ["gp", "209", "49", "4996", "8", "0", "0"],
            ["c_map", "0", "2648", "1"],
            ["gp", "61", "9", "4996", "8", "0", "0"],
        ])

        expected = {
            282: 39,
            283: 40,
            2515: 10,
            2567: 16,
            2635: 34,
            2636: 30,
            2638: 31,
            2648: 32,
        }

        for map_id, raid_type in expected.items():
            portal = groups[map_id][0]
            self.assertEqual(8, portal.type)
            self.assertEqual(raid_type, portal.raid_type)
            self.assertEqual(4996, portal.map_name_id)


if __name__ == "__main__":
    unittest.main()
