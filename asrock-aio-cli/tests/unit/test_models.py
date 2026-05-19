"""Unit tests for the models module."""
from models import SystemMetrics, MetricsType, DisplayMode, USBPacket


def test_system_metrics():
    """Tests the SystemMetrics class."""
    # Fix parameter names to match class definition
    metrics_data = {
        "cpu_temperature_celsius": 50.0,
        "cpu_frequency_mhz": 3500,
        "pump_rpm": 1200
    }
    system_metrics = SystemMetrics(**metrics_data)
    assert system_metrics.cpu_temperature_celsius == 50.0
    assert system_metrics.cpu_frequency_mhz == 3500
    assert system_metrics.pump_rpm == 1200


def test_usb_packet_to_bytes():
    """Tests the to_bytes method of the USBPacket class."""
    # Create a packet with specific values
    packet = USBPacket(
        report_id=0x07,
        metrics_type=MetricsType.CPU_TEMPERATURE,
        encoded_value=b'\x00\x33\x09\x00',  # Example from README
        reserved_byte_1=DisplayMode.MODE_3,
        reserved_byte_2=0x08
    )

    bytes_result = packet.to_bytes()

    # Should be exactly 64 bytes
    assert len(bytes_result) == 64

    # Check specific byte positions from README structure
    assert bytes_result[0] == 0x07  # Report ID
    assert bytes_result[1] == 0x00  # Metrics type (CPU temp)
    assert bytes_result[2:6] == b'\x00\x33\x09\x00'  # Encoded value
    assert bytes_result[6] == 0x04  # Mode (MODE_3 = 0x04)
    assert bytes_result[7] == 0x08  # Bar indicator

    # Check padding (remaining bytes should be 0x00)
    assert all(b == 0x00 for b in bytes_result[8:])
