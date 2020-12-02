# 1. Read Input file into a DataFrame;
# 2. Remove specific characters and whitespaces;
# 3. Cleaning columns one by one;
# 4. Check units and convert, once necessary;
# 6. Fix ranges separation, while multiple values are present;
# 5. Add temperature association.

# OUT. Allow for multiple output formats: csv, json, xlsx;

import pandas as pd
import logging
import re
import argparse
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
IN_FILE = os.path.join(CURRENT_DIR, "..", "data", "Python Developer Test.xlsx")
OUT_PATH = os.path.join(CURRENT_DIR, "..", "out")

SPEC_CHAR = "[ ,°<>]"
OO_MAGNITUDE = "x10-6|µ"  # -> * pow(10,-6)
RANGE_INDICATOR = "-|to"  # -> ',' coma
TEMPERATURE_SEPARATOR = "@"  # -> ';' semicolon
UNIT_SEPARATORS = "W/m|MPa|g/c|C"  # regular_expression for separating units;


def parse_thermal_expansion(input_value: str) -> str:
    """
    Converts input value(s) in a given format to the string with floating point value(s).
    :param input_value:
    :return: cleaned string
    """
    input_value = re.sub(SPEC_CHAR, "", input_value)
    value = re.split(OO_MAGNITUDE, input_value)[0]
    nums = re.split(RANGE_INDICATOR, value)

    out_values = []
    for n in nums:
        num = float(n) * pow(10, -6)
        out_values.append("{:.7f}".format(num))
    return ",".join(out_values)


def fahrenheit_to_celsius(fahrenheit_str: str) -> str:
    """
    Converts value from the input string from fahrenheit to celsius;
    :param fahrenheit_str: string with the value in °F
    :return: string with the corresponding value in °C
    """
    fahrenheit = int(fahrenheit_str)
    celsius = int((fahrenheit - 32) / 1.8)
    return str(celsius)


def parse_generic_column(input_value: str) -> str:
    """A generic parser, used while NO unit conversion is required;
    Applied for the following columns:
    - thermalConductivity, -fractureToughness, -density.
    :param input_value:
    :return: cleaned string
    """
    input_value = re.sub(SPEC_CHAR, "", input_value)
    value = re.split(UNIT_SEPARATORS, input_value)[0]
    value = re.sub(RANGE_INDICATOR, ",", value)
    value = re.sub(TEMPERATURE_SEPARATOR, ";", value)
    return value


def parse_melting_point(input_value: str) -> str:
    """
    Input value(s) are converted to °C and stored in a string
    :param input_value: string
    :return: cleaned string
    """
    input_value = re.sub(SPEC_CHAR, "", input_value)
    value = ""

    if "F" in input_value:
        fahrenheit_str = input_value.split("F")[0]
        value = fahrenheit_to_celsius(fahrenheit_str)

    elif "C" in input_value:
        value = input_value.split("C")[0]

    value = re.sub(RANGE_INDICATOR, ",", value)
    value = re.sub(TEMPERATURE_SEPARATOR, ";", value)
    return value


if __name__ == "__main__":

    out_format_options = ["csv", "json", "xlsx"]
    parser = argparse.ArgumentParser(description="Select output format")
    parser.add_argument(
        "-o",
        "--outformat",
        dest="output_format",
        choices=out_format_options,
        default="xlsx",
    )
    out_format = parser.parse_args().output_format

    input_file = pd.ExcelFile(IN_FILE)
    df_raw = pd.read_excel(input_file, sheet_name="Ceramic_Raw_Data")
    df_map = pd.read_excel(input_file, sheet_name="material_property_map")
    df_out = pd.read_excel(input_file, sheet_name="material_data_result")

    raw_columns = list(df_raw.columns)
    out_columns = list(df_out.columns)

    # 1. Renaming columns

    column_names = dict(zip(raw_columns, out_columns))
    df_raw = df_raw.rename(columns=column_names)

    logger.info(df_raw.dtypes)

    # 2. Parsing data by columns

    df_raw["linearCoefficientOfThermalExpansion"] = df_raw[
        "linearCoefficientOfThermalExpansion"
    ].apply(lambda x: parse_thermal_expansion(str(x)))
    df_raw["thermalConductivity"] = df_raw["thermalConductivity"].apply(
        lambda x: parse_generic_column(str(x))
    )
    df_raw["fractureToughness"] = df_raw["fractureToughness"].apply(
        lambda x: parse_generic_column(str(x))
    )
    df_raw["density"] = df_raw["density"].apply(lambda x: parse_generic_column(str(x)))
    df_raw["meltingPoint"] = df_raw["meltingPoint"].apply(
        lambda x: parse_melting_point(str(x))
    )

    # 3. Saving cleaned dataframe to the output file with the specified format

    result = {
        "csv": lambda x: x.to_csv(os.path.join(OUT_PATH, "output.csv"), index=False),
        "json": lambda x: x.to_json(
            os.path.join(OUT_PATH, "output.json"), orient="split", index=False
        ),
        "xlsx": lambda x: x.to_excel(
            os.path.join(OUT_PATH, "output.xlsx"),
            sheet_name="material_data_result",
            index=False,
        ),
    }[out_format](df_raw)
