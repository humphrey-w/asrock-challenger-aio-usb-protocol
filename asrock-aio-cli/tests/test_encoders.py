from encoders import *


def test_temperature_encoder():
    '''Tests the TemperatureEncoder class.'''
    encoder = TemperatureEncoder()
    encoded_value = encoder.encode(39.0)

    assert encoded_value == b"\x00\x03\x09\x00"  # 39°C


def test_frequency_encoder():
    '''Tests the FrequencyEncoder class.'''
    encoder = FrequencyEncoder()
    encoded_value = encoder.encode(3500)

    assert encoded_value == b"\x03\x05\x00\x00"  # 3500 MHz


def test_pump_rpm_encoder():
    '''Tests the PumpRPMEncoder class.'''
    encoder = PumpRPMEncoder()
    encoded_value = encoder.encode(1200)

    assert encoded_value == b"\x01\x02\x00\x00"  # 1200 RPM


def test_context_class_with_temperature():
    '''Tests the Encode class with TemperatureEncoder.'''
    encoder = Encode(TemperatureEncoder())
    encoded_value = encoder.encode(39.4)

    assert encoded_value == b"\x00\x03\x09\x00"  # 39°C


def test_context_class_with_frequency():
    '''Tests the Encode class with FrequencyEncoder.'''
    encoder = Encode(FrequencyEncoder())
    encoded_value = encoder.encode(3500)

    assert encoded_value == b"\x03\x05\x00\x00"  # 3500 MHz


def test_context_class_with_pump_rpm():
    '''Tests the Encode class with PumpRPMEncoder.'''
    encoder = Encode(PumpRPMEncoder())
    encoded_value = encoder.encode(1200)

    assert encoded_value == b"\x01\x02\x00\x00"  # 1200 RPM
