"""Real HID transport for USB communication with ASRock AIO."""
import hid
from typing import List
from .transport import Transport, DeviceNotFoundError, TransmissionError


class HIDTransport(Transport):
    """Transport using HID API for USB communication."""

    def __init__(self):
        self._device = None

    def connect(self) -> None:
        """Connect to the device via HID."""
        try:
            self._device = hid.device()
            self._device.open(self.VENDOR_ID, self.PRODUCT_ID)
        except OSError as e:
            raise DeviceNotFoundError(
                f"Could not find {self.VENDOR_ID:#06x}:{self.PRODUCT_ID:#06x}"
            ) from e

    def disconnect(self) -> None:
        """Close the HID connection."""
        if self._device:
            self._device.close()
            self._device = None

    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self._device is not None

    def send_packet(self, packet: bytes) -> None:
        """Send a single packet."""
        if not self.is_connected():
            raise RuntimeError("Not connected to device")

        if len(packet) != 64:
            raise ValueError(f"Packet must be 64 bytes, got {len(packet)}")

        try:
            self._device.write(packet)
        except OSError as e:
            raise TransmissionError(f"Failed to send packet: {e}") from e

    def send_sequence(self, packets: List[bytes]) -> None:
        """Send a sequence of packets."""
        for packet in packets:
            self.send_packet(packet)

    def close(self) -> None:
        """Close and clean up."""
        self.disconnect()
