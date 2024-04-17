import unittest

from flora.pylib.rules.color import Color
from flora.pylib.rules.part import Part
from flora.pylib.rules.plant_duration import PlantDuration
from flora.pylib.rules.subpart import Subpart
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.habitat import Habitat

from labels.pylib.rules.admin_unit import AdminUnit
from labels.pylib.rules.locality import Locality
from tests.setup import parse


class TestLocality(unittest.TestCase):
    def test_locality_01(self):
        self.assertEqual(
            parse("""5 miles North of Mason off Hwy 386."""),
            [
                Locality(
                    locality="5 miles North of Mason off Hwy 386.",
                    start=0,
                    end=35,
                ),
            ],
        )

    def test_locality_02(self):
        self.assertEqual(
            parse(
                """
                Tunkhannock Twp. Pocono Pines Quadrangle. Mud Run, Stonecrest Park,.16
                miles SSW of Long Pond, PA. Headwaters wetland of Indiana Mountains
                Lake.
                """,
            ),
            [
                Locality(
                    locality="Tunkhannock Twp.",
                    start=0,
                    end=16,
                ),
                Locality(
                    locality="Pocono Pines Quadrangle.",
                    start=17,
                    end=41,
                ),
                Locality(
                    locality=(
                        "Mud Run, Stonecrest Park,.16 miles SSW of Long Pond, PA. "
                        "Headwaters wetland of Indiana Mountains Lake."
                    ),
                    start=42,
                    end=144,
                ),
            ],
        )

    def test_locality_03(self):
        self.assertEqual(
            parse("""; files. purple."""),
            [],
        )

    def test_locality_04(self):
        self.assertEqual(
            parse("""(Florida's Turnpike)"""),
            [
                Locality(
                    locality="Florida's Turnpike",
                    start=0,
                    end=19,
                ),
            ],
        )

    def test_locality_05(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                """
                Wallowa-Whitman National Forest, Forest Service Road 7312.
                """,
            ),
            [
                Locality(
                    locality="Wallowa-Whitman National Forest, Forest Service "
                    "Road 7312.",
                    start=0,
                    end=58,
                ),
            ],
        )

    def test_locality_06(self):
        self.assertEqual(
            parse("""Sonoran Desert scrub, disturbed trail side. Occasional annual."""),
            [
                Habitat(
                    habitat="sonoran desert scrub",
                    start=0,
                    end=20,
                ),
                Locality(
                    locality="disturbed trail side.",
                    start=22,
                    end=43,
                ),
                PlantDuration(
                    plant_duration="annual",
                    start=55,
                    end=61,
                ),
            ],
        )

    def test_locality_07(self):
        self.assertEqual(
            parse(
                """
                Arizona Uppland Sonoran Desert desert scrub, flats.
                Sandy soil Local erecta annual,
                """,
            ),
            [
                AdminUnit(start=0, end=7, us_state="Arizona"),
                Habitat(
                    habitat="uppland sonoran desert desert scrub flats",
                    start=8,
                    end=50,
                ),
                Habitat(habitat="sandy soil", start=52, end=62),
                PlantDuration(
                    plant_duration="annual",
                    start=76,
                    end=82,
                ),
            ],
        )

    def test_locality_08(self):
        self.assertEqual(
            parse("""Scattered on edge of forest;"""),
            [Habitat(end=27, habitat="edge of forest", start=13)],
        )

    def test_locality_09(self):
        self.assertEqual(
            parse("""lobes turned out or black."""),
            [
                Subpart(subpart="lobe", start=0, end=5),
                Color(
                    color="black",
                    start=20,
                    end=25,
                    subpart="lobe",
                ),
            ],
        )

    def test_locality_10(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                """
                LOCATION Along Rte. 39, 9.1 mi SEof Santiago Papasquiaro.
                HABITAT Pine-juniper-oak-acacia zone.
                """,
            ),
            [
                Locality(
                    locality="Along Rte. 39, 9.1 mi SEof Santiago Papasquiaro.",
                    labeled=True,
                    start=0,
                    end=57,
                ),
                Habitat(
                    habitat="Pine-juniper-oak-acacia zone",
                    start=58,
                    end=94,
                ),
            ],
        )

    def test_locality_11(self):
        self.assertEqual(
            parse(
                """
                Fruit is a
                grape and is dark purple in color.
                """,
            ),
            [
                Part(part="fruit", type="fruit_part", start=0, end=5),
                Color(
                    color="purple-in-color",
                    start=24,
                    end=44,
                    part="fruit",
                ),
            ],
        )

    def test_locality_12(self):
        self.assertEqual(
            parse("""Monteverde. Elev. 1400- 1500 m. Lower montane rainforest"""),
            [
                Elevation(
                    elevation=1400.0,
                    elevation_high=1500.0,
                    units="m",
                    start=12,
                    end=31,
                ),
                Habitat(
                    end=56,
                    habitat="montane rain forest",
                    start=38,
                ),
            ],
        )

    def test_locality_13(self):
        self.assertEqual(
            parse("""Point Sublime Road about 1 miles east of Milk Creek."""),
            [
                Locality(
                    locality="Point Sublime Road about 1 miles east of Milk Creek.",
                    start=0,
                    end=52,
                ),
            ],
        )

    def test_locality_14(self):
        self.assertEqual(
            parse("""north of the Illinois Central Railroad,"""),
            [
                Locality(
                    locality="north of the Illinois Central Railroad",
                    start=0,
                    end=38,
                ),
            ],
        )

    def test_locality_15(self):
        self.assertEqual(
            parse("""Location: Emory and Henry Campus Ebor Data ?: M a fo C1"""),
            [
                Locality(
                    start=0,
                    end=44,
                    locality="Emory and Henry Campus Ebor Data ?",
                    labeled=True,
                ),
            ],
        )

    def test_locality_16(self):
        self.assertEqual(
            parse("""M a fo C1 Vi 1"""),
            [],
        )

    def test_locality_17(self):
        self.assertEqual(
            parse("""Cheyenne Crossing on US Hwy. 85"""),
            [
                Locality(
                    start=0,
                    end=31,
                    locality="Cheyenne Crossing on US Hwy. 85",
                ),
            ],
        )
