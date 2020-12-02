import pytest

from src.main import (parse_thermal_expansion,
                      fahrenheit_to_celsius,
                      parse_melting_point,
                      parse_generic_column)


@pytest.mark.parametrize("test_input,expected", [("11 x 10-6/K", "0.000011"),
                                                 ("7.00 µm/m-°C", "0.000007"),
                                                 ("7.9 - 11 x10 -6 / ° C", "0.000007,0.000011"),
                                                 ("10x10 -6 / ° C for 20C", "0.00001"),
                                                 ("10.5 x 10-6/°C", "0.0000105")])
def test_parse_thermal_expansion(test_input, expected):
    assert parse_thermal_expansion(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [("2.5 to 3 W/mK", "2.5,3"),
                                                 ("1.675 W/m-K", "1.675"),
                                                 ("2.7 - 3.0", "2.7,3.0")])
def test_parse_thermal_conductivity(test_input, expected):
    assert parse_generic_column(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [("4919", "2715"),
                                                 ("50", "10")])
def test_fahrenheit_to_celsius(test_input, expected):
    assert fahrenheit_to_celsius(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [("6.5 to 8 MPam1/2", "6.5,8"),
                                                 (">6.04@23C", "6.04;23")])
def test_parse_fracture_toughness(test_input, expected):
    assert parse_generic_column(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [("5.68 g/cc", "5.68")])
def test_parse_density(test_input, expected):
    assert parse_generic_column(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [("2681 - 2847 °C", "2681.0,2847.0"),
                                                 ("4,919° F", "2715")])
def test_parse_melting_point(test_input, expected):
    assert parse_melting_point(test_input) == expected