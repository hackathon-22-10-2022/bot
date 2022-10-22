import re


def checkbox_field_values_to_str(field_values: dict) -> str:
    strnig = ""
    for key, value in field_values.items():
        strnig += f"{key}: {value}\n"
    return strnig[:-1]


def radio_field_values_to_str(field_values: list) -> str:
    string = ""
    i = 1
    for value in field_values:
        string += f"{i}: {value}\n"
        i += 1
    return string[:-1]


def convert_str_with_commas_to_list(str_with_commas: str) -> list[int]:
    return [int(x) for x in re.findall(r"\b\d+\b", str_with_commas)]
