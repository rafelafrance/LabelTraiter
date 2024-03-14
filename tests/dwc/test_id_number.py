import unittest

from tests.setup import to_dwc

LABEL = "id_number"


class TestIdNumber(unittest.TestCase):
    def test_id_number_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Sarah Nunn and S. Jacobs and R. Mc Elderry 9480"),
            {
                "dwc:recordNumber": "9480",
            },
        )

    def test_id_number_02(self):
        self.assertEqual(
            to_dwc(LABEL, "Det;; N. H Russell 195"),
            {
                "dwc:recordNumber": "195",
            },
        )

    def test_id_number_03(self):
        self.assertEqual(
            to_dwc(LABEL, "R. Mc Elderry No. 9480"),
            {
                "dwc:recordNumber": "9480",
                "dwc:dynamicProperties": {"recordNumberIsLabeled": True},
            },
        )
