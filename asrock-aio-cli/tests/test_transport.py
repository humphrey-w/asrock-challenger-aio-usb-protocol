"""Unit tests for the transport classes."""
import pytest
from typing import List
from transports import (
    Transport,
    TransmissionError,
    HIDTransport,
    DeviceNotFoundError
)


class MockTransport(Transport):
    """Mock transport that records sent packets for testing."""

    def __init__(self):
        self._connected = False
        self.sent_packets: List[bytes] = []
        self.should_fail = False

    def connect(self) -> None:
        """Simulate connection."""
        self._connected = True

    def disconnect(self) -> None:
        """Simulate disconnection."""
        self._connected = False

    def is_connected(self) -> bool:
        """Return connection status."""
        return self._connected

    def send_packet(self, packet: bytes) -> None:
        """Record packet without sending."""
        if not self.is_connected():
            raise RuntimeError("Not connected")

        if self.should_fail:
            raise TransmissionError("Simulated transmission failure")

        self.sent_packets.append(packet)

    def send_sequence(self, packets: List[bytes]) -> None:
        """Send multiple packets in sequence."""
        for packet in packets:
            self.send_packet(packet)

    def close(self) -> None:
        """Clean up."""
        self.disconnect()

    def reset(self) -> None:
        """Reset for next test."""
        self.sent_packets = []
        self.should_fail = False


def test_mock_transport_connection():
    """Test mock transport connection state."""
    transport = MockTransport()
    assert not transport.is_connected()

    transport.connect()
    assert transport.is_connected()

    transport.disconnect()
    assert not transport.is_connected()


def test_mock_transport_records_packets():
    """Test that mock transport records sent packets."""
    transport = MockTransport()
    transport.connect()

    packet = b'\x07' + b'\x00' * 63
    transport.send_packet(packet)

    assert len(transport.sent_packets) == 1
    assert transport.sent_packets[0] == packet


def test_mock_transport_sends_sequence():
    """Test sending multiple packets in sequence."""
    transport = MockTransport()
    transport.connect()

    packets = [
        b'\x07\x00' + b'\x00' * 62,
        b'\x07\x03' + b'\x00' * 62,
        b'\x07\x04' + b'\x00' * 62,
    ]

    transport.send_sequence(packets)
    assert len(transport.sent_packets) == 3


def test_mock_transport_fails_if_not_connected():
    """Test error when sending without connection."""
    transport = MockTransport()
    packet = b'\x07' + b'\x00' * 63

    with pytest.raises(RuntimeError):
        transport.send_packet(packet)


def test_context_manager():
    """Test transport as context manager."""
    with MockTransport() as transport:
        assert transport.is_connected()
    assert not transport.is_connected()


def test_hid_transport_connection():
    """Test HID transport connection."""
    transport = HIDTransport()
    try:
        transport.connect()
        assert transport.is_connected()
    except DeviceNotFoundError as e:
        pytest.skip(e)
    finally:
        transport.close()


def test_hid_transport_send_packet():
    """Test sending a packet with HID transport."""
    transport = HIDTransport()
    try:
        transport.connect()
        packet = b'\x07' + b'\x00' * 63
        transport.send_packet(packet)
    except DeviceNotFoundError as e:
        pytest.skip(e)
    finally:
        transport.close()


def test_hid_transport_send_sequence():
    """Test sending a sequence of packets with HID transport."""
    transport = HIDTransport()
    try:
        transport.connect()
        packets = [
            b'\x07\x00' + b'\x00' * 62,
            b'\x07\x03' + b'\x00' * 62,
            b'\x07\x04' + b'\x00' * 62,
        ]
        transport.send_sequence(packets)
    except DeviceNotFoundError as e:
        pytest.skip(e)
    finally:
        transport.close()


def test_hid_transport_disconnect():
    """Test HID transport disconnection."""
    transport = HIDTransport()
    try:
        transport.connect()
        assert transport.is_connected()
        transport.disconnect()
        assert not transport.is_connected()
    except DeviceNotFoundError as e:
        pytest.skip(e)
    finally:
        transport.close()
