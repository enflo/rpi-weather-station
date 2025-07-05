"""
Tests for utility functions.
"""

from src.utils import celsius_to_fahrenheit, fahrenheit_to_celsius


def test_celsius_to_fahrenheit():
    """Test the celsius_to_fahrenheit function."""
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert celsius_to_fahrenheit(-40) == -40


def test_fahrenheit_to_celsius():
    """Test the fahrenheit_to_celsius function."""
    assert fahrenheit_to_celsius(32) == 0
    assert fahrenheit_to_celsius(212) == 100
    assert fahrenheit_to_celsius(-40) == -40


def test_conversion_roundtrip():
    """Test that converting from Celsius to Fahrenheit and back gives the original value."""
    celsius_values = [-40, -10, 0, 10, 20, 30, 40, 100]
    for celsius in celsius_values:
        fahrenheit = celsius_to_fahrenheit(celsius)
        assert round(fahrenheit_to_celsius(fahrenheit), 10) == celsius