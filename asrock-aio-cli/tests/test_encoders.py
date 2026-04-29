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


def test_temperature_encoder_single_digit():
    '''Tests TemperatureEncoder with single-digit temperature.'''
    encoder = TemperatureEncoder()
    encoded_value = encoder.encode(9.0)

    assert encoded_value == b"\x00\x00\x09\x00"  # 9°C (padded to "09")
    assert len(encoded_value) == 4


def test_frequency_encoder_three_digits():
    '''Tests FrequencyEncoder with three-digit frequency.'''
    encoder = FrequencyEncoder()
    encoded_value = encoder.encode(700)

    assert encoded_value == b"\x00\x07\x00\x00"  # 700 MHz (padded to "0700")
    assert len(encoded_value) == 4


def test_pump_rpm_encoder_three_digits():
    '''Tests PumpRPMEncoder with three-digit RPM.'''
    encoder = PumpRPMEncoder()
    encoded_value = encoder.encode(700)

    assert encoded_value == b"\x00\x07\x00\x00"  # 700 RPM (padded to "0700")
    assert len(encoded_value) == 4


def test_temperature_encoder_ensures_four_bytes():
    '''Tests that temperature encoder always produces exactly 4 bytes.'''
    encoder = TemperatureEncoder()

    for temp in [0, 5, 9, 15, 42, 99]:
        encoded = encoder.encode(float(temp))
        assert len(encoded) == 4


def test_frequency_encoder_ensures_four_bytes():
    '''Tests that frequency encoder always produces exactly 4 bytes.'''
    encoder = FrequencyEncoder()

    for freq in [1, 10, 100, 700, 999, 3500, 4999]:
        encoded = encoder.encode(freq)
        assert len(encoded) == 4


def test_rpm_encoder_ensures_four_bytes():
    '''Tests that RPM encoder always produces exactly 4 bytes.'''
    encoder = PumpRPMEncoder()

    for rpm in [1, 10, 100, 700, 999, 1200, 2967]:
        encoded = encoder.encode(rpm)
        assert len(encoded) == 4
