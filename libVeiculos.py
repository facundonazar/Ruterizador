'''
Clase que retendrá informaiones referentes a los vehículos.
lista_veiculos => lista de vehículos regitrado con los que vamos a trabajar.
'''
class cVeiculos(object):
    lista_veiculos = [];
    binCap = 0 #variable usada para guardar el peso del bin usado en diversos calculos, aunque guarda la mayor capacidad del bin.
    max_itens_bin = 12 #número máximo de items por bin

    def __init__(self, parent):
        self.parent = parent

    def load_data(self):
        df = self.parent.buffer_infos.df1
        lista_size = 10
        for x in range (lista_size):
            buffer_tupla = (df.iloc[10+x][14], float(df.iloc[10+x][15])) #cargo modelo de capacidad de bin
            self.lista_veiculos.append(buffer_tupla)
            if (self.binCap < buffer_tupla[1]): #mantener variable de la instancia, así pruedo trabajar a futuro com más de un tipo de camión.
                self.binCap = buffer_tupla[1];
