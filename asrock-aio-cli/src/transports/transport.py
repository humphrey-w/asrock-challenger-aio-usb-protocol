"""Abstract interface for USB transport implementations."""
from abc import ABC, abstractmethod
from typing import List


class TransportError(Exception):
    """Base exception for transport layer errors."""


class DeviceNotFoundError(TransportError):
    """Raised when the device cannot be found on the USB bus."""


class TransmissionError(TransportError):
    """Raised when a packet transmission fails."""


class Transport(ABC):
    """Abstract base class for USB/HID transport implementations."""

    # USB device identifiers for ASRock Challenger AIO
    VENDOR_ID = 0x26ce  # ASRock vendor ID
    PRODUCT_ID = 0x0a13  # ASRock Challenger AIO product ID

    @abstractmethod
    def connect(self) -> None:
        """Connect to the device. Raises DeviceNotFoundError if not found."""

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the device."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connected to the device."""

    @abstractmethod
    def send_packet(self, packet: bytes) -> None:
        """
        Send a single 64-byte packet to the device.

        Args:
            packet: 64-byte USB packet

        Raises:
            TransmissionError: If send fails
            RuntimeError: If not connected
        """

    @abstractmethod
    def send_sequence(self, packets: List[bytes]) -> None:
        """
        Send a sequence of packets (for LCDPacketSequence).

        Args:
            packets: List of 64-byte USB packets

        Raises:
            TransmissionError: If any send fails
            RuntimeError: If not connected
        """

    @abstractmethod
    def close(self) -> None:
        """Close and clean up resources."""

    def __enter__(self):
        """Context manager support."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support."""
        self.close()
