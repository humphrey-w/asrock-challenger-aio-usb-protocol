"""Encoders for the system metric values displayed on the AIO LCD."""
from abc import ABC, abstractmethod


class Encoder(ABC):
    """Abstract class for encoding system metrics into bytes."""
    PAD_BYTE: int = 0x00

    @abstractmethod
    def encode(self, value) -> bytes:
        """Encode a system metric into a 4-byte format for USB transmission."""


class TemperatureEncoder(Encoder):
    """Encoder for CPU temperature values."""
    def encode(self, value: float) -> bytes:
        """Encode CPU temperature as bytes."""
        temp_str = str(int(value)).zfill(2)  # Pad to 2 digits
        digits = [int(i) for i in temp_str]
        encoded_temp = bytes([self.PAD_BYTE] + digits + [self.PAD_BYTE])
        return encoded_temp


class FrequencyEncoder(Encoder):
    """Encoder for CPU frequency values."""
    def encode(self, value: int) -> bytes:
        """Encode CPU frequency as bytes."""
        freq_str = str(int(value)).zfill(4)  # Pad to 4 digits
        digits = [int(i) for i in freq_str]
        encoded_freq = bytes(digits)
        return encoded_freq


class PumpRPMEncoder(Encoder):
    """Encoder for pump RPM values."""
    def encode(self, value: int) -> bytes:
        """Encode pump RPM as bytes."""
        rpm_str = str(int(value)).zfill(4)  # Pad to 4 digits
        digits = [int(i) for i in rpm_str]
        encoded_rpm = bytes(digits)
        return encoded_rpm


class Encode:
    """Context class for encoding system metrics using a specified encoder."""
    encoder: Encoder

    def __init__(self, encoder: Encoder) -> None:
        self._encoder = encoder

    def encode(self, value) -> bytes:
        """Encode a system metric value using the specified encoder."""
        return self._encoder.encode(value)
