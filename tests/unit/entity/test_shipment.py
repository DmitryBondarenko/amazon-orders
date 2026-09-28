__copyright__ = "Copyright (c) 2024-2025 Alex Laird"
__license__ = "MIT"

import os

from bs4 import BeautifulSoup

from amazonorders import util
from amazonorders.entity.shipment import Shipment
from tests.unittestcase import UnitTestCase


class TestShipment(UnitTestCase):
    def test_shipment_progress_tracker_link(self):
        # GIVEN
        with open(os.path.join(self.RESOURCES_DIR, "orders", "shipment-progress-tracker-snippet.html"),
                  "r",
                  encoding="utf-8") as f:
            parsed = BeautifulSoup(f.read(), self.test_config.bs4_parser)
        tag = util.select_one(parsed, self.test_config.selectors.SHIPMENT_ENTITY_SELECTOR)

        # WHEN
        shipment = Shipment(tag, self.test_config)

        # THEN
        self.assertEqual("Delivered January 6", shipment.delivery_status)
        self.assertTrue(shipment.tracking_link.startswith(
            f"{self.test_config.constants.BASE_URL}/progress-tracker/package?"))
        self.assertIn("orderId=112-0000000-0000000", shipment.tracking_link)
        self.assertEqual("AbCdEfGhI", shipment.shipment_id)

    def test_shipment_without_tracking_link(self):
        # GIVEN
        parsed = BeautifulSoup("<div class=\"a-box delivery-box\"><span class=\"delivery-box__primary-text\">"
                               "Delivered January 6</span></div>", self.test_config.bs4_parser)

        # WHEN
        shipment = Shipment(parsed, self.test_config)

        # THEN
        self.assertIsNone(shipment.tracking_link)
        self.assertIsNone(shipment.shipment_id)
