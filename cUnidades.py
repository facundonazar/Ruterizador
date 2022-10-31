import pandas as pd

# Clase con informacion sobre unidades.
class cUnidades(object):
    quantidade_cidades = 0 # cantidad total de ciudades
    liga_best_fit = 0
    v_cidade_usina = 0
    vpercentual_frete_morto = 0
    vraio_consolidacao = 0
    cantidad_max_rutas_bsas = 0
    cantidad_max_rutas_arg = 0
    
    def __init__(self, parent):
        self.parent = parent

    def load_data(self):
        df = self.parent.buffer_infos.df1
        self.quantidade_cidades = int(df.iloc[35][1]) # 5566
        self.liga_best_fit = int(df.iloc[33][1]) # 1
        self.v_cidade_usina = df.iloc[10][5] # 4973 -> codigo de CD/ciudad
        self.vpercentual_frete_morto = int(df.iloc[20][10]) # 100%
        self.vraio_consolidacao = int(df.iloc[18][10]) # 100km -> distancia maxima entre clientes
        self.cantidad_max_rutas_bsas = int(df.iloc[16][10]) # 2 -> Cantidad maxima de rutas por BSAS
        self.cantidad_max_rutas_arg = int(df.iloc[17][10]) # 5 -> Cantidad maxima de rutas por ARG
        
        # carga el archivo localidad.txt en un dataframe de pandas, es una matriz [5565][5565]. Da para usar directamente aqué en ese df mismo
        print('Abriendo archivo con distancia entre ciudades - localidades.txt')
        filename = self.parent.buffer_infos.path + '\\localidades.txt'
        self.df_distancia_cidades = pd.read_csv(filename,sep='\t')

