import unittest

from flora.pylib.rules.part import Part

from labels.pylib.rules.admin_unit import AdminUnit
from labels.pylib.rules.locality import Locality
from tests.setup import parse


class TestAdminUnit(unittest.TestCase):
    def test_admin_unit_01(self):
        """It gets a county notation."""
        self.assertEqual(
            parse("""Hempstead County"""),
            [
                AdminUnit(
                    us_county="Hempstead",
                    start=0,
                    end=16,
                ),
            ],
        )

    def test_admin_unit_02(self):
        """A label is required."""
        self.assertEqual(
            parse("""Watauga"""),
            [],
        )

    def test_admin_unit_03(self):
        """It handles a confusing county notation."""
        self.assertEqual(
            parse("""Flora of ARKANSAS County: MISSISSIPPI"""),
            [
                AdminUnit(
                    us_county="Mississippi",
                    us_state="Arkansas",
                    start=0,
                    end=37,
                ),
            ],
        )

    def test_admin_unit_04(self):
        """It handles a county label before the county name."""
        self.assertEqual(
            parse("""COUNTY: Lee"""),
            [AdminUnit(us_county="Lee", start=0, end=11)],
        )

    def test_admin_unit_05(self):
        """It handles a trailing county abbreviation."""
        self.assertEqual(
            parse("""Alleghany Co,"""),
            [
                AdminUnit(
                    us_county="Alleghany",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_admin_unit_06(self):
        """It handles a state abbreviation."""
        self.assertEqual(
            parse("""Desha Co., Ark."""),
            [
                AdminUnit(
                    us_state="Arkansas",
                    us_county="Desha",
                    start=0,
                    end=15,
                ),
            ],
        )

    def test_admin_unit_07(self):
        """It gets a state notation."""
        self.assertEqual(
            parse("""PLANTS OF ARKANSAS"""),
            [
                AdminUnit(
                    us_state="Arkansas",
                    start=0,
                    end=18,
                ),
            ],
        )

    def test_admin_unit_08(self):
        """It gets a multi-word state notation."""
        self.assertEqual(
            parse("""PLANTS OF NORTH CAROLINA"""),
            [
                AdminUnit(
                    us_state="North Carolina",
                    start=0,
                    end=24,
                ),
            ],
        )

    def test_admin_unit_09(self):
        """It gets a state notation separated from the county."""
        self.assertEqual(
            parse(
                """
                APPALACHIAN STATE UNIVERSITY HERBARIUM
                PLANTS OF NORTH CAROLINA
                STONE MOUNTAIN STATE PARK
                WILKES COUNTY
                """,
            ),
            [
                AdminUnit(
                    us_state="North Carolina",
                    start=39,
                    end=63,
                ),
                AdminUnit(
                    us_county="Wilkes",
                    start=90,
                    end=103,
                ),
            ],
        )

    def test_admin_unit_10(self):
        """It parses multi-word counties and states."""
        self.assertEqual(
            parse("""Cape May, New Jersey"""),
            [
                AdminUnit(
                    us_county="Cape May",
                    us_state="New Jersey",
                    start=0,
                    end=20,
                ),
            ],
        )

    def test_admin_unit_11(self):
        """County vs colorado (CO)."""
        self.assertEqual(
            parse("""ARCHULETA CO"""),
            [
                AdminUnit(
                    us_county="Archuleta",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_admin_unit_12(self):
        """County vs colorado (CO)."""
        self.assertEqual(
            parse("""Archuleta CO"""),
            [
                AdminUnit(
                    us_state="Colorado",
                    us_county="Archuleta",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_admin_unit_13(self):
        """It does not pick up label headers and footers."""
        self.assertEqual(
            parse("""The University of Georgia Athens, GA, U.S.A."""),
            [
                AdminUnit(
                    country="USA",
                    us_state="Georgia",
                    end=44,
                    start=34,
                ),
            ],
        )

    def test_admin_unit_14(self):
        """It does not pick up label headers and footers."""
        self.assertEqual(
            parse("""Tree The New York Botanical Garden Herbarium"""),
            [Part(part="tree", type="plant_part", start=0, end=4)],
        )

    def test_admin_unit_15(self):
        self.assertEqual(
            parse("""St. Lucie Co.: Fort Pierce."""),
            [
                AdminUnit(
                    us_county="St. Lucie",
                    start=0,
                    end=13,
                ),
                Locality(
                    locality="Fort Pierce.",
                    start=15,
                    end=27,
                ),
            ],
        )

    def test_admin_unit_16(self):
        """It gets a province."""
        self.assertEqual(
            parse("""Province of Panama"""),
            [AdminUnit(end=18, province="panama", start=0)],
        )

    def test_admin_unit_17(self):
        """It gets state county notation on two lines."""
        self.assertEqual(
            parse(
                """
                Herbarium of the University of North Carolina
                SOUTH CAROLINA
                Dillon County
                """,
            ),
            [
                AdminUnit(
                    us_state="South Carolina",
                    us_county="Dillon",
                    start=46,
                    end=74,
                ),
            ],
        )

    def test_admin_unit_18(self):
        self.assertEqual(
            parse("""St. Louis, Missouri,"""),
            [
                AdminUnit(
                    us_state="Missouri",
                    us_county="St. Louis",
                    start=0,
                    end=19,
                ),
            ],
        )

    def test_admin_unit_19(self):
        self.assertEqual(
            parse("""N. C. Mecklenburg Co;"""),
            [
                AdminUnit(
                    us_state="North Carolina",
                    us_county="Mecklenburg",
                    start=0,
                    end=20,
                ),
            ],
        )

    def test_admin_unit_20(self):
        self.assertEqual(
            parse("""ST. BERNARDO PARISH."""),
            [
                AdminUnit(
                    us_county="St. Bernard",
                    start=0,
                    end=19,
                ),
            ],
        )

    def test_admin_unit_21(self):
        self.assertEqual(
            parse("""San Benito County, California."""),
            [
                AdminUnit(
                    us_state="California",
                    us_county="San Benito",
                    start=0,
                    end=29,
                ),
            ],
        )

    def test_admin_unit_22(self):
        self.assertEqual(
            parse("""Plants of Kern Co, USA"""),
            [
                AdminUnit(
                    us_county="Kern",
                    start=10,
                    end=17,
                ),
                AdminUnit(
                    country="USA",
                    start=19,
                    end=22,
                ),
            ],
        )

    def test_admin_unit_23(self):
        self.assertEqual(
            parse("""Oregon State Agricultural College"""),
            [],
        )
