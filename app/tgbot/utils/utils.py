import logging
from typing import Any

logger = logging.getLogger(__name__)


def parse_user_info(records: list) -> dict:
    user_info = {}
    for record in records:

        logger.info(f"Parameter Name: {record.get("parameter_name")}, Parameter Value: {record.get("parameter_value")}")
        user_info[record.get("parameter_name")] = convert_value(record.get("parameter_value"),
                                                                record.get("parameter_value_data"))
    return user_info


def convert_value(value: str, data_type: str) -> Any:
    """Converts a string value to the specified data type."""
    print(data_type)
    try:
        if data_type == "int":
            return int(value)
        elif data_type == "float":
            return float(value)
        elif data_type == "string":
            return str(value)
        else:
            logger.warning(f"Unknown data type: {data_type}, returning as string")
            return str(value)
    except ValueError as e:
        logger.error(f"Error converting value '{value}' to type '{data_type}': {e}")
        return str(value)  # Return as string in case of error
