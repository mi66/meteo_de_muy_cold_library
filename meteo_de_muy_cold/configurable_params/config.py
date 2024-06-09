debug_mode = False
endpoint = "https://opendata.aemet.es/opendata/api/antartida/datos/fechaini/{}/fechafin/{}/estacion/{}"
#endpoint = "https://opendata.aemet.es/opendata/api/antartida/datos/fechaini/2023-01-01T01%3A01%3A59UTC/fechafin/2023-01-03T06%3A01%3A59UTC/estacion/89070"
predefined_model = {
            "fields": ["nombre", "fhora", "temp", "pres", "vel"]
        }