debug_mode = False
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtZGQwODBAYXViZ2FsdW1uaS5uZXQiLCJqdGkiOiI4NTE0ZDJhZC03ZDY4LTRhMzktYTgwNy1hZmJhODlkNTAyYmUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcxNzc4MDIwNSwidXNlcklkIjoiODUxNGQyYWQtN2Q2OC00YTM5LWE4MDctYWZiYTg5ZDUwMmJlIiwicm9sZSI6IiJ9.pk_x7-aZFv_FJM68ot4GdZhM-ZGHczpe2s2NETzee8k"
endpoint = "https://opendata.aemet.es/opendata/api/antartida/datos/fechaini/{}/fechafin/{}/estacion/{}"
#endpoint = "https://opendata.aemet.es/opendata/api/antartida/datos/fechaini/2023-01-01T01%3A01%3A59UTC/fechafin/2023-01-03T06%3A01%3A59UTC/estacion/89070"
predefined_model = {
            "fields": ["nombre", "fhora", "temp", "pres", "vel"]
        }