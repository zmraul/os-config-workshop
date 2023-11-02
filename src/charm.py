#!/usr/bin/env python3
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

import ops

from profiles import PRODUCTION_PROFILE, TESTING_PROFILE

logger = logging.getLogger(__name__)


class OsConfigWorkshopCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_start(self, event: ops.StartEvent):
        """Handle start event."""
        self.unit.status = ops.ActiveStatus()

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        """Handle config changed event."""
        profile = self.config['profile']

        if profile == 'production':
            logger.info("Using PRODUCTION profile")
        elif profile == 'testing':
            logger.info("Using TESTING profile")


if __name__ == "__main__":  # pragma: nocover
    ops.main(OsConfigWorkshopCharm)  # type: ignore
