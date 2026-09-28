__copyright__ = "Copyright (c) 2024-2025 Alex Laird"
__license__ = "MIT"

import logging
import re
from typing import Optional

from bs4 import Tag

from amazonorders.conf import AmazonOrdersConfig
from amazonorders.entity.parsable import Parsable

logger = logging.getLogger(__name__)

# The carrier header reads e.g. "Shipped with UPS" or "Delivery facilitated by Amazon".
_CARRIER_PREFIX_REGEX = re.compile(r"^(?:shipped with|delivered by|delivery (?:facilitated )?by|carrier:?)\s+",
                                   re.IGNORECASE)


class Tracking(Parsable):
    """
    The carrier tracking of an Amazon :class:`~amazonorders.entity.shipment.Shipment`, parsed from the
    page its :attr:`~amazonorders.entity.shipment.Shipment.tracking_link` points to. See
    :func:`~amazonorders.orders.AmazonOrders.get_tracking`.
    """

    def __init__(self,
                 parsed: Tag,
                 config: AmazonOrdersConfig) -> None:
        super().__init__(parsed, config)

        #: The carrier name, e.g. ``UPS``, or ``Amazon`` for Amazon's own delivery network.
        self.carrier: Optional[str] = self.safe_parse(self._parse_carrier)
        #: The carrier's tracking number, e.g. ``1Z999AA10123456784`` or ``TBA000000000000``.
        self.tracking_number: Optional[str] = self.safe_simple_parse(
            selector=self.config.selectors.FIELD_TRACKING_NUMBER_SELECTOR,
            prefix_split=":",
            prefix_split_fuzzy=True)

    def __repr__(self) -> str:
        return f"<Tracking: \"{self.carrier} {self.tracking_number}\">"

    def __str__(self) -> str:  # pragma: no cover
        return f"Tracking: {self.carrier} {self.tracking_number}"

    def _parse_carrier(self) -> Optional[str]:
        value = self.simple_parse(self.config.selectors.FIELD_TRACKING_CARRIER_SELECTOR)
        if not value:
            return None

        return _CARRIER_PREFIX_REGEX.sub("", str(value)).strip() or None
