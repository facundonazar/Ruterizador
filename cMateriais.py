import pandas as pd

class cMateriais(object):
    # tenemos dos matrices referentes a los materiales.
    # la macro-micro y la de compatibilidad de familia.
    # ambas son, inicialmente, cuadradas 21x21 (compatflia) y 20x2 (macro-micro).
    # En caso de haber adición de materiales será necesario redimensionar esa matriz.

    # TO DO: cuando eliminamos el paso intermedio de excel en el medio del camino,
    # será posible crear esas matrices sin limitación hard-coded.
    familia_macro_micro = 0 #matriz_familia_macro_micro
    compatibilidade_familia = 0 #matriz_compatibilidade_familia
    
    def __init__(self, parent):
        self.parent = parent
        # para poder usar las matrices, 1ro es necesario inicializarlas. En python no tenemos asignación.
        w, h = 2, 19; # TAMAÑO DE MATRIZ - 20 líneas (height), 2 columnas (width)
        self.familia_macro_micro = [[0 for x in range(w)] for y in range(h)] # -> rellena de ceros
        w, h = 20, 20; # TAMAÑO DE MATRIZ
        self.compatibilidade_familia = [[0 for x in range(w)] for y in range(h)] # -> rellena de ceros

    # Definir rutina para poblar las matrices a partir del pandas dataframe con el contenido de Excel.
    # La rutina equivalente a esa en el projecto original es la facessa_matriz
    def load_data_familia(self):
        df = self.parent.buffer_infos.df1
        # voy a recibir un dataframe de pandas y tratarlo adecuadamente
        w, h = 20, 20; # TAMAÑO DE LA MATRIZ
        for x in range (w): # x es la fila, y es la columna
            for y in range (h):
                self.compatibilidade_familia[y][x] = df.iloc[29+y][5+x]
        #compatibilidade_familia[x][y] = df1.iloc[29+x][5+y]
        #self.compatibilidade_familia = [[0 for x in range(w)] for y in range(h)]

    def load_data_macro_micro(self):
        df = self.parent.buffer_infos.df1
        w, h = 2, 19; #TAMANHO DA MATRIZ
        for x in range (w): #x é a linha, y é a coluna
            for y in range (h):
                self.familia_macro_micro[y][x] = df.iloc[54+y][7+x]
'''
Pienso que conviene hacer ndarrays con la 1ra fila y la 1ra columna al cargar los datos
para buscar y pensar cuál es el índice de la matriz de forma rápida y limpia.
'''