class cItens(object):
    itens2route = [] #conservar� una lista de items a roteirizar. En C++ era matriz_dados_dos_itens.

    def __init__(self, parent):
        self.parent = parent
        self.itens2route = []
 
    def load_data(self):
        df = self.parent.buffer_infos.df2
        linhas_size = df.iloc[7][0] #se�alo dos celdas que tienen f�rmulas cont. Cuando viene inMemory usar sizeof.
        colunas_size = df.iloc[7][14]
        for x in range (linhas_size): #linhas_size viene de var. logo acima, señala un resultado de fórmula de contagem de valores. É só o número de itens que teremos que varrer.
            self.itens2route.append(cItemRecord(df,x)) #talvez tenha que usar copy.copy(cItemRecord(df,x) ou então fazer uma linha  a mais buffer = cItemrecord... e append(buffer)

class cItemRecord(object):
    index = 0;
    peso = 0
    familia = 0
    volume = 0
    destino = 0
    familia_macro = 0
    meso_regiao = 0
    cliente = 0
    familia = 0
    familia_macro = 0

    def __init__(self, df, offset):
        self.index = int(df.iloc[9+offset][0])
        self.peso = float(df.iloc[9+offset][1])
        self.volume = float(df.iloc[9+offset][4]) # peso_item_real -> no código original vejo isso identificado como peso do item real
        self.destino = float(df.iloc[9+offset][5])
        self.fator_ajuste = float(df.iloc[9+offset][6])
        self.meso_regiao = int(df.iloc[9+offset][8]) #cidade
        self.cliente = int(df.iloc[9+offset][9])
        #TO DO verificar en que situaciones ocurre FAMILIA #N/D y DISTANCIA_USINA tmb.
        #dependiendo del tipo de comparaci�n posterior, usar alg�n valor num�rico.
        buffer = str(df.iloc[9+offset][2])
        if (buffer=='nan'):
            self.familia = "#N/D"
        else:
            self.familia = int(df.iloc[9+offset][2])
        
            
        if (str(df.iloc[9+offset][7])=='nan'):
            self.familia_macro = "#N/D" #0
        else:
            self.familia_macro = int(df.iloc[9+offset][7])        