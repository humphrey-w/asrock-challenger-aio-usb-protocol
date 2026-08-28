"""PacketBuilder constructs USBPacket instances from SystemMetrics data."""
from encoders import (Encode, TemperatureEncoder, FrequencyEncoder,
                      PumpRPMEncoder)
from models.protocol import USBPacket, MetricsType, DisplayMode


class PacketBuilder:
    """Builder for constructing USBPacket instances from SystemMetrics."""
    PAD_BYTE: int = 0x00
    CPU_FREQ_ENCODER: Encode = Encode(FrequencyEncoder())
    CPU_TEMP_ENCODER: Encode = Encode(TemperatureEncoder())
    PUMP_RPM_ENCODER: Encode = Encode(PumpRPMEncoder())

    def __init__(self):
        self.metrics_type: MetricsType
        self.encoded_value: bytes
        self.reserved_byte_1: DisplayMode = self.PAD_BYTE
        self.reserved_byte_2: int = self.PAD_BYTE

    def with_mode(self, mode: DisplayMode) -> 'PacketBuilder':
        """Set display mode in the packet."""
        self.reserved_byte_1 = mode
        return self

    def with_bar_indicator(self, bar_indicator: int) -> 'PacketBuilder':
        """Set bar indicator level in the packet."""
        self.reserved_byte_2 = bar_indicator
        return self

    def with_cpu_temperature(self,
                             temperature_celsius: float) -> 'PacketBuilder':
        """Set CPU temperature in the packet."""
        self.metrics_type = MetricsType.CPU_TEMPERATURE
        self.encoded_value = self.CPU_TEMP_ENCODER.encode(temperature_celsius)
        return self

    def with_cpu_frequency(self, frequency_mhz: int) -> 'PacketBuilder':
        """Set CPU frequency in the packet."""
        self.metrics_type = MetricsType.CPU_FREQUENCY
        self.encoded_value = self.CPU_FREQ_ENCODER.encode(frequency_mhz)
        return self

    def with_pump_rpm(self, pump_rpm: int) -> 'PacketBuilder':
        """Set pump RPM in the packet."""
        self.metrics_type = MetricsType.PUMP_RPM
        self.encoded_value = self.PUMP_RPM_ENCODER.encode(pump_rpm)
        return self

    def build(self) -> USBPacket:
        """Return the constructed USBPacket."""
        packet = USBPacket(
            metrics_type=self.metrics_type,
            encoded_value=self.encoded_value,
            reserved_byte_1=self.reserved_byte_1,
            reserved_byte_2=self.reserved_byte_2
        )
        return packet

    def reset(self) -> 'PacketBuilder':
        """Reset the builder to its initial state."""
        self.metrics_type = None
        self.encoded_value = None
        self.reserved_byte_1 = self.PAD_BYTE
        self.reserved_byte_2 = self.PAD_BYTE
        return self
