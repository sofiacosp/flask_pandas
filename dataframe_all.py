import bisect
import pandas as pd
import numpy as np

# Función para obtener el baremo adecusado según el sexo y la edad del sujeto
def get_dataframe_p1(baremo, edad):
    if baremo == "General" and edad < 5:
        df2 = pd.read_pickle('baremos/P1_Gral_3_4.pkl')

    elif baremo == "Mujeres" and edad < 5:
        df2 = pd.read_pickle('baremos/P1_Muj_3_4.pkl')

    elif baremo == "Varones" and edad < 5:
        df2 = pd.read_pickle('baremos/P1_Var_3_4.pkl')

    elif baremo == "General" and edad < 7:
        df2 = pd.read_pickle('baremos/P1_Gral_5_6.pkl')

    elif baremo == "Varones" and edad < 7:
        df2 = pd.read_pickle('baremos/P1_Var_5_6.pkl')

    elif baremo == "Mujeres" and edad < 7:
        df2 = pd.read_pickle('baremos/P1_Muj_5_6.pkl')

    return df2


def transforma_a_numero(x):
    if x=="Nunca":
        return 0
    elif x=="Alguna vez":
        return 1
    elif x=="Frecuentemente":
        return 2
    elif x=="Casi siempre":
        return 3
    else:
        return 0


# De acuerdo a la nota T de la persona se obtienen los niveles
def get_niveles(df_final,dimension):
    opciones_niveles_adapta = ['Clínicamente significativo', 'En riesgo', 'Medio', 'Alto', 'Muy alto']
    opciones_niveles_clinico = ['Muy bajo', 'Bajo', 'Medio', 'En riesgo', 'Clínicamente significativo']
    clinico= ["Agresividad", "Ansiedad", "Atipicidad", "Depresion", "Hiperactividad", "Problemas de atencion", "Retraimiento", "Somatizacion"]
    adaptable= ["Adaptabilidad", "Habilidades sociales"]
    condiciones = [df_final[f'T {dimension}'] <= 30, df_final[f'T {dimension}'] <= 40, df_final[f'T {dimension}'] <= 59,
                   df_final[f'T {dimension}'] <= 69, df_final[f'T {dimension}'] <= 129]
    if dimension in clinico:
        df_final[f'Nivel {dimension}'] = np.select(condiciones, opciones_niveles_clinico)
    else:
        df_final[f'Nivel {dimension}'] = np.select(condiciones, opciones_niveles_adapta)

    return df_final[f'Nivel {dimension}']

# De una lista de dimensiones se obtienen todos los niveles aplicando la funcion get_niveles
def niveles_all(df_final):
    dimensiones= ["Adaptabilidad","Agresividad", "Atipicidad", "Ansiedad", "Depresion", "Hiperactividad", "Habilidades sociales", "Problemas de atencion", "Retraimiento", "Somatizacion" ]
    for x in dimensiones:
        get_niveles(df_final,x)

# Se obtiene la nota T de las personas de acuerdo a su puntaje en una dimensión
def puntaje_p1(valores, edades, baremos, columna_comparar, columna_recuperar):

    resultado= []
    for j in range(len(valores)):

        if baremos[j] == "General" and edades[j]< 5:
            df2 = pd.read_pickle('baremos/P1_Gral_3_4.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 5:
            df2 = pd.read_pickle('baremos/P1_Muj_3_4.pkl')

        elif baremos[j] == "Varones" and edades[j] < 5:
            df2 = pd.read_pickle('baremos/P1_Var_3_4.pkl')

        elif baremos[j] == "General" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/P1_Gral_5_6.pkl')

        elif baremos[j] == "Varones" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/P1_Var_5_6.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/P1_Muj_5_6.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado

# Transforma los valores de texto a numeros (se podría cambiar por la función map
"""
def recodifica_var(df_columns):
    # print(df.iloc[:,1].map({"Nunca":0, "Alguna vez":1, "Frecuentemente":2,"Casi siempre":3}))
    for i in range(df_columns):
        df.iloc[:, i] = df.iloc[:, i].apply(transforma_a_numero)
    return df
"""
# Se obtiene la edad de una persona según el calendario gregoriano
def date_diff(date1, date2):
    return (date1 - date2).days / 365.2425


def cargar_dataframe():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrEpOBKtTnticMTM5BSb2MbsMpkU9hkaAVIjNhUz" \
          "-cWbMEvAINexTz7aL1ql0rfYGBcT0PQxh88MyC/pubhtml?gid=74737359&single=true "

    # Se lee la página web, el argumento header=1 indica que el nombre de las columnas está en la segunda fila
    # El encoding="UTF-8" asegura que se reconozca los acentos y la ñ
    tablas = pd.read_html(url, header=1, encoding="UTF-8")
    df = tablas[0]
    return df

def dataframe_p1():
    # Se declara la url de la cual se va a leer los datos
    df= cargar_dataframe()
    df_info = df.iloc[1:, :8]

    # Convertir a formato datetime
    df_info['Fecha de nacimiento'] = pd.to_datetime(df_info['Fecha de nacimiento'], format="%d/%m/%Y")
    df_info['Fecha'] = pd.to_datetime(df_info['Fecha'], format="%d/%m/%Y")

    # Calculamos la edad
    df_info['dias'] = (df_info['Fecha'] - df_info['Fecha de nacimiento']).dt.days
    df_info['Edad'] = df_info['dias'] / 365.2425
    df_info['Edad'] = df_info['Edad'].astype(int)


    # Añadimos la columna baremo en función del sexo de la persona mediante map
    df_info['Baremo'] = df_info['Sexo'].map({'Varón': 'Varones',
                                             'Mujer': 'Mujeres'})

    # Se selecciona solo las columnas de los items
    df = df.iloc[1:, 8:]

    # Se recodifican todas las columnas
    for i in range(len(df.columns)):
        df.iloc[:, i] = df.iloc[:, i].apply(transforma_a_numero)
    #df = recodifica_var(len(df.columns))

    # Se calculan los puntajes directos
    puntaje_directo = {
        "PD Agresividad": df.iloc[:, 1] + df.iloc[:, 11] + df.iloc[:, 19] + df.iloc[:, 27] + df.iloc[:, 31] + df.iloc[:,
                          42] + df.iloc[:, 52] + df.iloc[:, 64] + df.iloc[:, 75] + df.iloc[:, 85] + df.iloc[:, 96] + df.iloc[:,
                          105] + df.iloc[:, 115],
        "PD Adaptabilidad": df.iloc[:, 0] + (3 - df.iloc[:, 10]) + (3 - df.iloc[:, 30]) + df.iloc[:, 41] + df.iloc[:,
                            63] + df.iloc[:, 74] + df.iloc[:, 84] + (3 - df.iloc[:, 95]) + df.iloc[:, 104] + df.iloc[:, 114]
                            + df.iloc[:, 125],
        "PD Ansiedad": df.iloc[:, 20] + df.iloc[:, 32] + df.iloc[:, 43] + df.iloc[:, 53] + df.iloc[:, 65] + df.iloc[:, 76]
                       + df.iloc[:, 86] + df.iloc[:, 106] + df.iloc[:,116],
        "PD Atipicidad": df.iloc[:, 3] + df.iloc[:, 13] + df.iloc[:, 21] + df.iloc[:, 34] + df.iloc[:, 45] + df.iloc[:, 54]
                         + df.iloc[:, 67] + df.iloc[:, 78] + df.iloc[:, 87] + df.iloc[:,108] + df.iloc[:,117],
        "PD Depresion": df.iloc[:, 4] + df.iloc[:, 14] + df.iloc[:, 22] + df.iloc[:, 35] + df.iloc[:, 46] + df.iloc[:, 55]
                        + df.iloc[:, 60] + df.iloc[:, 68] + df.iloc[:, 79] + df.iloc[:, 88] + df.iloc[:, 98]
                        + df.iloc[:,109] + df.iloc[:,118],
        "PD Hiperactividad": df.iloc[:, 5] + df.iloc[:, 15] + df.iloc[:, 23] + df.iloc[:, 28] + df.iloc[:, 36] + df.iloc[:, 47]
                             + df.iloc[:, 56] + df.iloc[:, 61] + df.iloc[:, 69] + df.iloc[:, 80] + df.iloc[:, 93] + df.iloc[:,99]
                             + df.iloc[:, 110] + df.iloc[:, 119] + df.iloc[:, 124] + df.iloc[:, 127],
        "PD Habilidades sociales": df.iloc[:, 6] + df.iloc[:, 16] + df.iloc[:, 24] + df.iloc[:, 37] + df.iloc[:, 48]
                                   + df.iloc[:,57] + df.iloc[:, 70] + df.iloc[:, 81] + df.iloc[:, 90] + df.iloc[:,100]
                                   + df.iloc[:,111] + df.iloc[:,120] + df.iloc[:,123] + df.iloc[:, 129],
        "PD Problemas de atencion": df.iloc[:, 2] + (3 - df.iloc[:, 33]) + df.iloc[:, 44] + df.iloc[:, 66]
                                    + df.iloc[:, 77] + df.iloc[:, 97] + df.iloc[:, 107] + df.iloc[:,126],
        "PD Retraimiento": df.iloc[:, 8] + df.iloc[:, 39] + df.iloc[:, 50] + df.iloc[:, 59] + df.iloc[:, 72]
                           + df.iloc[:,83] + df.iloc[:,92] + (3 - df.iloc[:, 102]) + df.iloc[:, 113] + df.iloc[:, 122]
                           + df.iloc[:, 128],
        "PD Somatizacion": df.iloc[:, 7] + df.iloc[:, 17] + df.iloc[:, 25] + df.iloc[:, 29] + df.iloc[:, 38]
                           + df.iloc[:,49] + df.iloc[:, 58] + df.iloc[:, 62] + df.iloc[:, 71] + df.iloc[:,82]
                           + df.iloc[:, 91] + df.iloc[:, 101] + df.iloc[:, 112] + df.iloc[:, 121],

    }

    #inicio=time.time()
    # Convertir a lista los baremos, edad y los puntajes directos de cada dimensión
    baremo1 = df_info['Baremo'].values.tolist()
    edad1 = df_info['Edad'].values.tolist()
    df_puntaje = pd.DataFrame(puntaje_directo)
    adaptabilidad= df_puntaje['PD Adaptabilidad'].values.tolist()
    agresividad= df_puntaje['PD Agresividad'].values.tolist()
    ansiedad= df_puntaje['PD Ansiedad'].values.tolist()
    atipicidad= df_puntaje['PD Atipicidad'].values.tolist()
    depresion= df_puntaje['PD Depresion'].values.tolist()
    hiperactividad= df_puntaje['PD Hiperactividad'].values.tolist()
    habilidades_sociales= df_puntaje['PD Habilidades sociales'].values.tolist()
    problemas_atencion= df_puntaje['PD Problemas de atencion'].values.tolist()
    retraimiento= df_puntaje['PD Retraimiento'].values.tolist()
    somatizacion= df_puntaje['PD Somatizacion'].values.tolist()

    # Declarar una variable para los valores de una columna en base a la funcion puntaje_p1
    somatizacion_valores= puntaje_p1(somatizacion,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Somatización')
    # Crear un diccionario con el nombre de las columnas y los puntajes T
    puntaje_T= {
        "T Agresividad": puntaje_p1(agresividad,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Agresividad'),
        "T Adaptabilidad":puntaje_p1(adaptabilidad,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Adaptabilidad'),
        "T Ansiedad":puntaje_p1(ansiedad,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Ansiedad'),
        "T Atipicidad":puntaje_p1(atipicidad,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Atipicidad'),
        "T Depresion":puntaje_p1(depresion,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Depresión'),
        "T Hiperactividad":puntaje_p1(hiperactividad,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Hiperactividad'),
        "T Habilidades sociales":puntaje_p1(habilidades_sociales,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Habilidades sociales'),
        "T Problemas de atencion":puntaje_p1(problemas_atencion,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Problemas de atención'),
        "T Retraimiento":puntaje_p1(retraimiento,edades=edad1,baremos=baremo1,columna_comparar='PD',columna_recuperar='T Retraimiento'),
        "T Somatizacion":somatizacion_valores,
    }
    # Se convierte a dataframe el diccionario creado anteriormente
    df_T = pd.DataFrame(puntaje_T)
    #print(time.time()-inicio)

    # Se resetea los indices de todos los dataframes
    df_info= df_info.reset_index(drop=True)
    df= df.reset_index(drop=True)
    df_puntaje= df_puntaje.reset_index(drop=True)
    df_T= df_T.reset_index(drop=True)

    # Se unen todos los dataframes
    df_final = pd.concat([df_info, df, df_puntaje, df_T], axis=1)

    # Se generan las columnas de los niveles basados en el puntaje T con la funcion niveles_all()
    niveles_all(df_final)

    # Guardar en csv
    #df_final.to_csv('resultados1.csv', encoding='utf-8')
    return df_final