"""Unit tests for the encoder classes."""
import pytest
from encoders import (
    Encode,
    TemperatureEncoder,
    FrequencyEncoder,
    PumpRPMEncoder
)


def test_temperature_encoder(system_metrics):
    """Tests the TemperatureEncoder class."""
    encoder = TemperatureEncoder()
    encoded_value = encoder.encode(system_metrics.cpu_temperature_celsius)

    assert encoded_value == b'\x00\x03\x09\x00'  # 39°C


def test_frequency_encoder(system_metrics):
    """Tests the FrequencyEncoder class."""
    encoder = FrequencyEncoder()
    encoded_value = encoder.encode(system_metrics.cpu_frequency_mhz)

    assert encoded_value == b'\x03\x06\x00\x00'  # 3600 MHz


def test_pump_rpm_encoder(system_metrics):
    """Tests the PumpRPMEncoder class."""
    encoder = PumpRPMEncoder()
    encoded_value = encoder.encode(system_metrics.pump_rpm)

    assert encoded_value == b'\x02\x09\x06\x07'  # 2967 RPM


def test_context_class_with_temperature(system_metrics):
    """Tests the Encode class with TemperatureEncoder."""
    encoder = Encode(TemperatureEncoder())
    encoded_value = encoder.encode(system_metrics.cpu_temperature_celsius)

    assert encoded_value == b'\x00\x03\x09\x00'  # 39°C


def test_context_class_with_frequency(system_metrics):
    """Tests the Encode class with FrequencyEncoder."""
    encoder = Encode(FrequencyEncoder())
    encoded_value = encoder.encode(system_metrics.cpu_frequency_mhz)

    assert encoded_value == b'\x03\x06\x00\x00'  # 3600 MHz


def test_context_class_with_pump_rpm(system_metrics):
    """Tests the Encode class with PumpRPMEncoder."""
    encoder = Encode(PumpRPMEncoder())
    encoded_value = encoder.encode(system_metrics.pump_rpm)

    assert encoded_value == b'\x02\x09\x06\x07'  # 2967 RPM


def test_temperature_encoder_single_digit():
    """Tests TemperatureEncoder with single-digit temperature."""
    encoder = TemperatureEncoder()
    encoded_value = encoder.encode(9.0)

    assert encoded_value == b'\x00\x00\x09\x00'  # 9°C (padded to "09")
    assert len(encoded_value) == 4


def test_frequency_encoder_three_digits():
    """Tests FrequencyEncoder with three-digit frequency."""
    encoder = FrequencyEncoder()
    encoded_value = encoder.encode(700)

    assert encoded_value == b'\x00\x07\x00\x00'  # 700 MHz (padded to "0700")
    assert len(encoded_value) == 4


def test_pump_rpm_encoder_three_digits():
    """Tests PumpRPMEncoder with three-digit RPM."""
    encoder = PumpRPMEncoder()
    encoded_value = encoder.encode(700)

    assert encoded_value == b'\x00\x07\x00\x00'  # 700 RPM (padded to "0700")
    assert len(encoded_value) == 4


@pytest.mark.parametrize("temp", [0, 5, 9, 15, 42, 99])
def test_temperature_encoder_ensures_four_bytes(temp):
    """Tests that temperature encoder always produces exactly 4 bytes."""
    encoder = TemperatureEncoder()

    encoded = encoder.encode(float(temp))
    assert len(encoded) == 4


@pytest.mark.parametrize("freq", [1, 10, 100, 700, 999, 3500, 4999])
def test_frequency_encoder_ensures_four_bytes(freq):
    """Tests that frequency encoder always produces exactly 4 bytes."""
    encoder = FrequencyEncoder()

    encoded = encoder.encode(freq)
    assert len(encoded) == 4


@pytest.mark.parametrize("rpm", [1, 10, 100, 700, 999, 1200, 2967])
def test_rpm_encoder_ensures_four_bytes(rpm):
    """Tests that RPM encoder always produces exactly 4 bytes."""
    encoder = PumpRPMEncoder()

    encoded = encoder.encode(rpm)
    assert len(encoded) == 4
