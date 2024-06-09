import requests
import json
from datetime import datetime
import pytz
import meteo_de_muy_cold.auxiliary_functions as aux
import meteo_de_muy_cold.configurable_params.config as conf

def api_main(mainual_input_full_path, output_file_folder_only_path):
    try:
        debug_mode = conf.debug_mode
        message = ''
        result = False
        final_file_path = ''
        # Convert manual input to proper values
        final_input = aux._create_input_params(debug_mode, mainual_input_full_path)
        granularity = int(final_input['granularity'])

        # Dictionaries to hold the aggregated data
        aggregated_data_hour = {}
        aggregated_data_day = {}
        aggregated_data_month = {}
        non_aggreagated_data = {}

        # Model of the response - to only keep needed cols
        predefined_model = conf.predefined_model
        # Api Key (usually pulled from a credentials safe, but... :)
        api_key = final_input['api_key']

        # URL of the API endpoint
        url = conf.endpoint.format(final_input['from'],final_input['to'],final_input['station'])

        # Headers to be included in the request
        headers = {
            "api_key": api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Timezone setting
        cet_zone = pytz.timezone('Europe/Berlin')

        # Get the initial json file name
        response = requests.get(url = url, headers=headers)
        if response.status_code == 200:
            json_object = json.loads(response.text)
            if 'datos' not in json_object:
                message = json_object['descripcion']
                result = False
                raise Exception(f'API failed - {message}')
            json_address = json_object['datos']
        else:
            message = f'{response.status_code} - {response.text}'
            result = False
            raise Exception(f'API failed - {message}')
        if debug_mode:
            print(json_address)

        # Get the contents of the Json file
        response = requests.get(json_address)
        if debug_mode:
            print(response.text)
        raw_data = json.loads(response.text)

        # Leave only fields from the model
        filtered_data = [
            {field: entry[field] for field in predefined_model["fields"]}
            for entry in raw_data
        ]
        if debug_mode:
            print(filtered_data)

        # Aggregate data
        for row in filtered_data:
            temp_utc_str = row['fhora']
            temp_utc_ts = datetime.strptime(temp_utc_str, "%Y-%m-%dT%H:%M:%S%z")
            temp_cet_ts = temp_utc_ts.astimezone(cet_zone)
            temp_cet_ts_str = str(temp_cet_ts.strftime('%Y-%m-%dT%H:%M:%S')) + 'CET'
            row['temp_cet_ts_str'] = temp_cet_ts_str
            row['fhora_cet'] = str(temp_cet_ts)
            row['hour_cet_tz'] = aux._round_down_to_hour(temp_cet_ts)
            row['day_cet_tz'] = aux._round_down_to_day(temp_cet_ts)
            row['month_cet_tz'] = aux._round_down_to_month(temp_cet_ts)

        sorted_data = sorted(filtered_data, key=lambda x: x["fhora_cet"])
        for row in sorted_data:
            if granularity == 0:
                if str(row['temp_cet_ts_str']) not in non_aggreagated_data:
                    non_aggreagated_data[str(row['temp_cet_ts_str'])] = []
                non_aggreagated_data[str(row['temp_cet_ts_str'])].append({'temp': row['temp'], 'pres': row['pres'], 'vel': row['vel'], 'nombre': row['nombre']})
            elif granularity == 3:
                if str(row['month_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET') not in aggregated_data_month:
                    aggregated_data_month[str(row['month_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET')] = []
                aggregated_data_month[str(row['month_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET')].append({'temp': row['temp'], 'pres': row['pres'], 'vel': row['vel'], 'nombre': row['nombre']})
            elif granularity == 2:
                if str(row['day_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET') not in aggregated_data_day:
                    aggregated_data_day[str(row['day_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET')] = []
                aggregated_data_day[str(row['day_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET')].append({'temp': row['temp'], 'pres': row['pres'], 'vel': row['vel'], 'nombre': row['nombre']})
            elif granularity == 1:
                if str(row['hour_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET') not in aggregated_data_hour:
                    aggregated_data_hour[str(row['hour_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET')] = []
                aggregated_data_hour[str(row['hour_cet_tz'].strftime('%Y-%m-%dT%H:%M:%S') + 'CET')].append({'temp': row['temp'], 'pres': row['pres'], 'vel': row['vel'], 'nombre': row['nombre']})



        # Fill the aggregated data into the new dicts
        averages_hourly = {}
        averages_daily = {}
        averages_monthly = {}
        averages_regular = {}
        dataset = {}

        if granularity == 3:
            for month, readings in aggregated_data_month.items():
                avg_temp = sum(r['temp'] for r in readings) / len(readings)
                avg_press = sum(r['pres'] for r in readings) / len(readings)
                avg_vel = sum(r['vel'] for r in readings) / len(readings)
                nombre = readings[0]['nombre']
                averages_monthly[month] = {'nombre': nombre, 'avg_temp': avg_temp, 'avg_pres': avg_press, 'avg_vel': avg_vel}

        elif granularity == 2:
            for day, readings in aggregated_data_day.items():
                avg_temp = sum(r['temp'] for r in readings) / len(readings)
                avg_press = sum(r['pres'] for r in readings) / len(readings)
                avg_vel = sum(r['vel'] for r in readings) / len(readings)
                nombre = readings[0]['nombre']
                averages_daily[day] = {'nombre': nombre, 'avg_temp': avg_temp, 'avg_pres': avg_press, 'avg_vel': avg_vel}

        elif granularity == 1:
            for hour, readings in aggregated_data_hour.items():
                avg_temp = sum(r['temp'] for r in readings) / len(readings)
                avg_press = sum(r['pres'] for r in readings) / len(readings)
                avg_vel = sum(r['vel'] for r in readings) / len(readings)
                nombre = readings[0]['nombre']
                averages_hourly[hour] = {'nombre': nombre, 'avg_temp': avg_temp, 'avg_pres': avg_press, 'avg_vel': avg_vel}

        elif granularity == 0:
            for ten_min, readings in non_aggreagated_data.items():
                avg_temp = sum(r['temp'] for r in readings) / len(readings)
                avg_press = sum(r['pres'] for r in readings) / len(readings)
                avg_vel = sum(r['vel'] for r in readings) / len(readings)
                nombre = readings[0]['nombre']
                averages_regular[ten_min] = {'nombre': nombre, 'avg_temp': avg_temp, 'avg_pres': avg_press, 'avg_vel': avg_vel}

        if debug_mode:
            print(filtered_data)
            print(aggregated_data_hour)
            print(averages_hourly)

        timestamp_for_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        if granularity == 0:
            filename = 'non-aggreagated-'+timestamp_for_name+'.txt'
            dataset = averages_regular.copy()
        elif granularity == 1:
            filename = 'hourly_avg-' + timestamp_for_name + '.txt'
            dataset = averages_hourly.copy()
        elif granularity == 2:
            filename = 'daily_avg-' + timestamp_for_name + '.txt'
            dataset = averages_daily.copy()
        elif granularity == 3:
            filename = 'monthly_avg-' + timestamp_for_name + '.txt'
            dataset = averages_monthly.copy()
        else:
            filename = 'non-aggreagated-'+timestamp_for_name+'.txt'
            dataset = averages_regular.copy()

        aux._print_json_as_table(dataset, str(output_file_folder_only_path+ '\\' +filename))

        message = f'Success'
        result = True
        final_file_path = f'{output_file_folder_only_path}\{filename}'
    except Exception as ex:
        message = str(ex)
        result = False
    return result, message, final_file_path
