#!/usr/bin/env python3
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

import ops
from charms.operator_libs_linux.v0 import grub

from profiles import PRODUCTION_PROFILE, TESTING_PROFILE

logger = logging.getLogger(__name__)


class OsConfigWorkshopCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, *args):
        super().__init__(*args)
        self.grub = grub.GrubConfig(self.app.name)

        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_start(self, event: ops.StartEvent):
        """Handle start event."""
        self.unit.status = ops.ActiveStatus()

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        """Handle config changed event."""
        profile = self.config["profile"]

        try:
            self._grub_config(profile=profile)
        except (grub.ApplyError, grub.ValidationError) as e:
            logger.error(f"Error setting values on GRUB: {e.message}")
            self.unit.status = ops.BlockedStatus("GRUB config not possible")
            return

        self.unit.status = ops.ActiveStatus()

    def _on_remove(self, event: ops.RemoveEvent):
        """Handle start event."""
        self.grub.remove()

    def _grub_config(self, profile: str):
        """Add sysctl config."""
        if profile == "production":
            self.grub.update(config=PRODUCTION_PROFILE)
        elif profile == "testing":
            self.grub.update(config=TESTING_PROFILE)


if __name__ == "__main__":  # pragma: nocover
    ops.main(OsConfigWorkshopCharm)  # type: ignore
