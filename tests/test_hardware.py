from src.hardware import get_rpi_model, is_raspberry_pi
from unittest.mock import patch, mock_open

def test_get_rpi_model_zero_2_w():
    cpuinfo_mock = """
Hardware	: BCM2835
Revision	: 902120
Serial		: 0000000000000000
Model		: Raspberry Pi Zero 2 W Rev 1.0
"""
    with patch("builtins.open", mock_open(read_data=cpuinfo_mock)):
        info = get_rpi_model()
        assert info["model"] == "Raspberry Pi Zero 2 W"
        assert info["family"] == "Zero"

def test_get_rpi_model_pi_5():
    cpuinfo_mock = """
Hardware	: BCM2835
Revision	: c04170
Serial		: 0000000000000000
Model		: Raspberry Pi 5 Model B Rev 1.0
"""
    with patch("builtins.open", mock_open(read_data=cpuinfo_mock)):
        info = get_rpi_model()
        assert "Raspberry Pi 5" in info["model"]
        assert info["family"] == "5"

def test_get_rpi_model_non_pi():
    with patch("builtins.open", side_effect=FileNotFoundError):
        info = get_rpi_model()
        assert info["family"] == "Generic"
        assert is_raspberry_pi() is False

def test_get_rpi_model_unknown_revision():
    cpuinfo_mock = """
Hardware	: BCM2835
Revision	: fffff
"""
    with patch("builtins.open", mock_open(read_data=cpuinfo_mock)):
        info = get_rpi_model()
        assert "Raspberry Pi" in info["model"]
        assert info["family"] == "Unknown"
