from builders import PacketBuilder
from models.protocol import DisplayMode


def test_packet_builder_with_temperature():
    '''Tests the with_temperature method of the PacketBuilder class.'''
    builder = PacketBuilder()
    packet = builder.with_cpu_temperature(39.0).build()

    assert packet.metrics_type == 0x00  # Metrics type (CPU_TEMPERATURE)
    assert packet.encoded_value == b"\x00\x03\x09\x00"  # 39°C


def test_packet_builder_with_frequency():
    '''Tests the with_cpu_frequency method of the PacketBuilder class.'''
    builder = PacketBuilder()
    packet = builder.with_cpu_frequency(3500).build()

    assert packet.metrics_type == 0x03  # Metrics type (CPU_FREQUENCY)
    assert packet.encoded_value == b"\x03\x05\x00\x00"  # 3500 MHz


def test_packet_builder_with_pump_rpm():
    '''Tests the with_pump_rpm method of the PacketBuilder class.'''
    builder = PacketBuilder()
    packet = builder.with_pump_rpm(1200) \
        .with_mode(DisplayMode.MODE_3) \
        .with_bar_indicator(14).build()

    assert packet.metrics_type == 0x04  # Metrics type (PUMP_RPM)
    assert packet.encoded_value == b"\x01\x02\x00\x00"  # 1200 RPM
    assert packet.reserved_byte_1 == 0x04  # Mode (MODE_3)
    assert packet.reserved_byte_2 == 0x0e  # Bar indicator (14)
