tipoSistema = "Trifásico"
tabla_capacidad_conduccion_PVC = {
    1.0: {"Monofásico": 13.5, "Trifásico": 12},
    1.5: {"Monofásico": 17.5, "Trifásico": 15.5},
    2.5: {"Monofásico": 24, "Trifásico": 21},
    4: {"Monofásico": 32, "Trifásico": 28},
    6: {"Monofásico": 41, "Trifásico": 36},
    10: {"Monofásico": 57, "Trifásico": 50},
    16: {"Monofásico": 76, "Trifásico": 68},
    25: {"Monofásico": 101, "Trifásico": 89},
    35: {"Monofásico": 125, "Trifásico": 111},
    50: {"Monofásico": 151, "Trifásico": 134},
    70: {"Monofásico": 192, "Trifásico": 171},
    95: {"Monofásico": 232, "Trifásico": 207},
    120: {"Monofásico": 269, "Trifásico": 239},
    150: {"Monofásico": 309, "Trifásico": 272},
    185: {"Monofásico": 353, "Trifásico": 310},
    240: {"Monofásico": 415, "Trifásico": 364},
    300: {"Monofásico": 473, "Trifásico": 419},
    400: {"Monofásico": 566, "Trifásico": 502},
    500: {"Monofásico": 651, "Trifásico": 578}, 
}

tabla_k = {
    1: {"Monofásico": 34.00, "Trifásico": 29.00},
    1.5: {"Monofásico": 23.00, "Trifásico": 20.00},
    2.5: {"Monofásico": 14.00, "Trifásico": 12.00},
    4: {"Monofásico": 8.70, "Trifásico": 7.50},
    6: {"Monofásico": 5.80, "Trifásico": 5.10},
    10: {"Monofásico": 3.50, "Trifásico": 3.00},
    16: {"Monofásico": 3.31, "Trifásico": 1.96},
    25: {"Monofásico": 1.52, "Trifásico": 1.28},
    35: {"Monofásico": 1.12, "Trifásico": 0.96},
    50: {"Monofásico": 0.82, "Trifásico": 0.73},
    70: {"Monofásico": 0.63, "Trifásico": 0.54},
    95: {"Monofásico": 0.49, "Trifásico": 0.42},
    120: {"Monofásico": 0.41, "Trifásico": 0.35},
    150: {"Monofásico": 0.36, "Trifásico": 0.31},
    185: {"Monofásico": 0.32, "Trifásico": 0.27},
    240: {"Monofásico": 0.26, "Trifásico": 0.23},
    300: {"Monofásico": 0.23, "Trifásico": 0.20},
    400: {"Monofásico": 0.20, "Trifásico": 0.18},
    500: {"Monofásico": 0.19, "Trifásico": 0.16},
}

k = 0.60
aislamientoConductor = "PVC"

# Seleccionamos la tabla adecuada según el aislamiento
tabla_capacidad_conduccion = tabla_capacidad_conduccion_PVC
                
# Obtenemos la lista de secciones
lista_secciones = list(tabla_capacidad_conduccion.keys())

for seccion, valoresK in reversed(list(tabla_k.items())):
    print(valoresK[tipoSistema])

