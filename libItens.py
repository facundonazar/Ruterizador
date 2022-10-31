class cItens(object):
    itens2route = [] # conservara una lista de items a roteirizar. En C++ era matriz_dados_dos_itens.

    def __init__(self, parent):
        self.parent = parent
        self.itens2route = []

    def load_data(self):
        df = self.parent.buffer_infos.df
        linhas_size = len(df) - 1 #Cambio la celda que señala por un count
        for x in range (linhas_size): # linhas_size viene de var. logo acima, senala un resultado de formula de contagem de valores. É só o número de itens que teremos que varrer.
            self.itens2route.append(cItemRecord(df,x)) # tal vez tenga que usar copy.copy(cItemRecord(df,x) ou então fazer uma linha  a mais buffer = cItemrecord... e append(buffer)

class cItemRecord(object):
    index = 0;
    peso = 0          #peso real - ex volume
    ruta_item = 0
    cliente = 0
    familia = 0
    familia_macro = 0
    peso_max = 0

    def __init__(self, df, offset):
        
        self.index = int(df.iloc[1+offset][22])
        self.peso = float(df.iloc[1+offset][8])     #peso_item_real -> ex volumen
        self.ruta_item = df.iloc[1+offset][19]    #ruta
        self.cliente = int(df.iloc[1+offset][23])

        if (str(df.iloc[1+offset][15])=='nan'):
            self.familia = "#N/D"
        else:
            self.familia = int(df.iloc[1+offset][15])
        
            
        if (str(df.iloc[1+offset][16])=='nan'):
            self.familia_macro = "#N/D" #0
        else:
            self.familia_macro = int(df.iloc[1+offset][16])
        
        # A DESARROLLAR
        if (self.familia != 8):      #peso max
            self.peso_max= self.peso
        else:
            self.peso_max= int(df.iloc[1+offset][8])