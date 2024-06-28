import json
import pathlib
import re
def _parse_simple_yaml(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split(':', 1)
                config[key.strip()] = value.strip()
    return config

def _round_down_to_hour(dt):
    return dt.replace(minute=0, second=0, microsecond=0)

def _round_down_to_day(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def _round_down_to_month(dt):
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)



def _print_json_as_table(json_object, file_path):
    # Flatten the JSON object
    # Parse the JSON data
    data = json_object

    # Extract the column headers
    headers = ['fhora'] + list(next(iter(data.values())).keys()) + ['nombre']

    # Prepare the rows
    rows = []
    for date, values in data.items():
        row = [date] + [f"{value:.2f}" if isinstance(value, (int, float)) else value for value in
                        values.values()]  # Format the values to 2 decimal places
        rows.append(row)

    # Determine column widths
    col_widths = [max(len(str(value)) for value in column) for column in zip(*([headers] + rows))]

    # Prepare the format string
    format_str = ' | '.join([f'{{:<{width}}}' for width in col_widths])

    # Print the table
    print(format_str.format(*headers))
    print('-+-'.join(['-' * width for width in col_widths]))
    for row in rows:
        print(format_str.format(*row))

    with open(file_path, 'w') as file:
        # Write headers
        file.write(format_str.format(*headers) + '\n')
        file.write('-+-'.join(['-' * width for width in col_widths]) + '\n')

        # Write rows
        for row in rows:
            file.write(format_str.format(*row) + '\n')

    print(f'Table written to {file_path}')

def _create_input_params(debug_mode: bool, manual_input: str):
    current_dir = pathlib.Path(__file__).parent
    path_to_lookup = current_dir / 'configurable_params' / 'lookup_values.yaml'
    path_to_allowed = current_dir / 'configurable_params' / 'allowed_values.yaml'
    lookup_values = _parse_simple_yaml(path_to_lookup)
    manual_selection = _parse_simple_yaml(manual_input)
    allowed_values = _parse_simple_yaml(path_to_allowed)
    if debug_mode:
        print(lookup_values)
        print(manual_selection)
    final_input = {}
    for item in manual_selection:
        if item not in ['from','to', 'api_key']:
            if manual_selection[item] not in lookup_values:
                raise Exception(f'Invalid value selected for {item}, possible values are - {allowed_values[item]}')
            else:
                final_input[item] = lookup_values[manual_selection[item]]
        elif item in ['api_key']:
            final_input[item] = manual_selection[item]
        else:
            pattern = lookup_values[item]
            if not re.match(pattern, manual_selection[item]):
                raise Exception(f'Invalid value provided for {item}, proper format is - {allowed_values[item]}')
            else:
                final_input[item] = manual_selection[item]
    if debug_mode:
        print(final_input)
    return final_input