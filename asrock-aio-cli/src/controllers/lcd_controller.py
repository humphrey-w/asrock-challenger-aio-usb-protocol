"""LCD Controller module for ASRock AIO CLI."""
from builders import PacketBuilder
from transports import Transport, DeviceNotFoundError
from models import (
    SystemMetrics,
    DisplayMode,
    USBPacket,
    LCDPacketSequence,
    MAX_BAR_INDICATOR
)


class LCDController:
    """Controller for managing the LCD display of ASRock AIO devices."""
    def __init__(self, transport: Transport):
        self.__transport = transport
        self.__builder = PacketBuilder()
        try:
            self.__transport.connect()
        except DeviceNotFoundError as e:
            print(f"Error connecting to ASRock AIO device: {e}")
            raise

    def display(self, metrics: SystemMetrics, mode: DisplayMode):
        """Display system metrics on the LCD based on the specified mode."""
        bars: int = 0
        cpu_temp_packet = self.__build_cpu_temp_packet(
            metrics.cpu_temperature_celsius
        )
        cpu_freq_packet = self.__build_cpu_freq_packet(
            metrics.cpu_frequency_mhz
        )
        bars = self.__calculate_bar_indicator(metrics, mode)
        pump_rpm_packet = self.__build_pump_rpm_packet(
            metrics.pump_rpm, mode, bars)
        packets = [cpu_temp_packet, cpu_freq_packet, pump_rpm_packet]
        sequence = LCDPacketSequence(*packets)
        try:
            self.__transport.send_sequence(sequence.to_bytes_sequence())
        except Exception as e:
            print(f"Error sending packet sequence: {e}")
            raise

    def __build_cpu_temp_packet(self, temp: float) -> USBPacket:
        """Create a USBPacket for CPU temperature."""
        packet = self.__builder.with_cpu_temperature(temp).build()
        return packet

    def __build_cpu_freq_packet(self, freq: int) -> USBPacket:
        """Create a USBPacket for CPU frequency."""
        packet = self.__builder.with_cpu_frequency(freq).build()
        return packet

    def __build_pump_rpm_packet(self, rpm: int, mode: DisplayMode,
                                bars: int) -> USBPacket:
        """Create a USBPacket for pump RPM with the specified display mode."""
        packet = (
            self.__builder
            .with_pump_rpm(rpm)
            .with_mode(mode)
            .with_bar_indicator(bars)
            .build()
        )
        return packet

    def __calculate_bar_indicator(self, metrics: SystemMetrics,
                                  mode: DisplayMode) -> int:
        """Calculate the bar indicator value based on the display mode."""
        if mode == DisplayMode.MODE_1:
            return int((metrics.pump_rpm / metrics.limits.max_pump_rpm) *
                       MAX_BAR_INDICATOR)
        elif mode == DisplayMode.MODE_2:
            return int((metrics.cpu_frequency_mhz /
                       metrics.limits.max_cpu_frequency_mhz) *
                       MAX_BAR_INDICATOR)
        elif mode == DisplayMode.MODE_3:
            return round((metrics.cpu_temperature_celsius /
                         metrics.limits.max_cpu_temperature_celsius) *
                         MAX_BAR_INDICATOR)
        else:
            raise ValueError(f"Unsupported display mode: {mode}")

    def close(self):
        """Close the transport connection."""
        try:
            self.__transport.close()
        except Exception as e:
            print(f"Error closing transport: {e}")
            raise

    def __del__(self):
        """Destructor to ensure the transport is closed."""
        self.close()

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context related to this object."""
        self.close()
