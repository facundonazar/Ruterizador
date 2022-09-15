import pandas as pd


#Clase con información sobre unidades.
#inicialmente para uso como objeto estático.
class cUnidades(object):
    quantidade_cidades = 0 #cantidad total de ciudades
    liga_best_fit = 0
    consolida_cliente_cidade = 0 #consolida_cliente_cidade = 1 consolida por cliente, 2 por ciudad
    v_cidade_usina = 0
    vpercentual_frete_morto = 0
    vraio_consolidacao = 0
    quantidade_clientes_maximo_rota = 0
    
    def __init__(self, parent):
        self.parent = parent

    def load_data(self):
        df = self.parent.buffer_infos.df1
        self.quantidade_cidades = int(df.iloc[35][1]) #5566
        self.liga_best_fit = int(df.iloc[33][1]) #1
        self.consolida_cliente_cidade = int(df.iloc[34][1]) #1
        self.v_cidade_usina = int(df.iloc[10][5]) #4973 -> código de CD/ciudad
        self.vpercentual_frete_morto = int(df.iloc[20][10]) #100%
        self.vraio_consolidacao = int(df.iloc[18][10]) #100km -> distancia máxima entre clientes
        self.quantidade_clientes_maximo_rota = int(df.iloc[16][10]) #2 -> clientes máximos por viaje

        #carga el archivo cidades.txt (arquivo.txt en nuestra carpeta) en un dataframe de pandas, es una matriz [5565][5565]. Dá para usar directamente aqué en ese df mismo
        print('Abrindo arquivo com distância entre cidades - ARQUIVO.TXT')
        filename = 'C:\\Users\\diegog1\\source\\repos\\Python Consolid8\\Python Consolid8\\data\\arquivo.txt' #'data\\arquivo.txt'
        self.df_distancia_cidades = pd.read_csv(filename,sep='\t')