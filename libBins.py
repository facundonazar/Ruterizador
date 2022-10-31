import copy
import os

class cBinPack(object):
    '''
    Este objeto conservara las bins precargados con los items obtenidos de la lista de SAP.
    Esta lista de items provenientes de SAP sera cargada en el objeto de clase cItens.
    El foco de esta clase es poblar las listas siguiendo los algoritmos desarrollados por Leandro.
    '''
    path = '//azrwcfs01acbr/Sectores/Ruteador_DLI/Data/'
    
    def __init__(self, parent):
        '''
        Cada item de estos arrays representa un bin. En cada bin entraran N objetos
        que podran ser de uno o mas clientes/ciudades.
        Aqui solo inicializamos las listas y variables.
        '''
        self.parent = parent
        self.conteiner_cacambas = [] # este objeto contendra los bins (CACAMBAS = BINS)
        self.conteiner_entregas_consolidadas = []

    def best_f_decreasing(self): # lista_itens es un array proveniente de objeto de tipo (cItens)variavel -> itens2route - LA INSTÂNCIA E NÃO A ESTATICA, DA CLASE.
        '''
        Efectivamente poblara los arrays con la lista de items cargada en otro objeto (dataframe pandas lista_itens),
        y provista como argumento.
        Creare los bins en un objeto propio, y las otras listas apuntaran a la posicion de cada bin (index).
        '''
        lista_itens = self.parent.lista_itens.itens2route
        binCap = self.parent.info_veiculos.binCap
        compatibilidade_familia = self.parent.info_materiais.compatibilidade_familia
        qt_max_rutas_bsas = self.parent.info_unidades.cantidad_max_rutas_bsas
        qt_max_rutas_arg = self.parent.info_unidades.cantidad_max_rutas_arg

        cliente_anterior = '0' #TO DO creo que puedo eliminar esta y contagem_bins, ver si uso esto para algo
        itemIndex = 0
        self.contagem_bins = 0

        while itemIndex < len(lista_itens):
            itemRecord = lista_itens[itemIndex]

            if (itemRecord.peso <= binCap): # ¿el bin soporta ese peso?
                item_alocado = False # TO DO creo que puedo incluir en el itemRecord la propriedad bool alocado y excluir eso de aqui.
                cacambaIndex = 0
                for cacambaRecord in self.conteiner_cacambas: # calcular diversos datos DE CADA BIN
                    if (cacambaRecord.testa_item_entra_cacamba(itemRecord, binCap)):
                        if(cacambaRecord.valida_mistura_de_familias(itemRecord.familia, compatibilidade_familia)):
                            
                            #if(cacambaRecord.soma_entregas() < qt_max_rutas):
                                
                                #COMENTO LA LINEA ANTERIOR PORQUE NO TIENE USO, YA QUE CONSOLIDA POR CLIENTE Y NO VA A HABER DIFERENTES RUTAS EN UN MISMO BIN
                                
                                self.conteiner_cacambas[cacambaIndex].lista_itens.append(itemRecord) 
                                item_alocado = True
                                break # interrumpir el loop FOR de los bins
                    cacambaIndex += 1
                    
                if (not item_alocado): #ciclo todos los bins y no consegui ubicar ese item en ninguno. Tendre que generar un bin nuevo para el.
                    self.conteiner_cacambas.append(cBin()) # creo nuevo bin
                    self.conteiner_cacambas[cacambaIndex].lista_itens.append(itemRecord) # guardo el item en este nuevo bin, ya que no entró ninguno de los anteriores.

            else: # peso del item > bincap - ciclar creando nuevos bins para n.int
                bins2create = int(itemRecord.peso // binCap) # division entera
                for i in range(bins2create):
                    self.conteiner_cacambas.append(cBin()) # creo nuevo bin
                    cacambaIndex = len(self.conteiner_cacambas) - 1
                    self.conteiner_cacambas[cacambaIndex].lista_itens.append(copy.deepcopy(itemRecord)) # guardo el item en este nuevo bin
                    self.conteiner_cacambas[cacambaIndex].lista_itens[0].peso = binCap;

                lista_itens[itemIndex].peso = itemRecord.peso % binCap # resto para que entre en un bin incompleto

                itemIndex -= 1 # ver si hay un forma de volver 1 step en el for, si existe adecuo el peso del item para ese resto y corro el for de nuevo
            
            itemIndex += 1
               
            if (itemIndex < len(lista_itens)):
                cliente_anterior = itemRecord.cliente # guardo el cliente para el proximo loop
                cliente_posterior = lista_itens[itemIndex].cliente

                if cliente_posterior != cliente_anterior:
                    # cerramos la consolidacion, guardo datos de item record en un bin de container cacambas
                    self.consolida(itemRecord.ruta_item)
            else:
                self.consolida(itemRecord.ruta_item) # si consolida por cliente, ¿por que pasamos region como parametro?

    def consolida(self, cidade):
        # ¿tenemos bin asignado?
        for binRecord in self.conteiner_cacambas:
            binRecord.indice = self.contagem_bins
            binRecord.rota = -1
            self.conteiner_entregas_consolidadas.append([cidade, binRecord]) # como consolida al cambiar de cliente, solo habra bins de un cliente, igual que parciales
                                                                             # de esa forma, basta obtener el bin.item.cidade. Al igual que si hubiera mas de un item, todas las ciudades seran iguales
            self.contagem_bins += 1
        self.conteiner_cacambas = [] # limpio la lista anterior de bins

    def outputCSV(self):
        buffer = [] # buffer para escribir en el disco
        buffer.append(['RUTA','INDICE_BIN','CLIENTE','FAMILIA','FAMILIA_MACRO','INDICE_ITEM','PESO'])
        for entrega in self.conteiner_entregas_consolidadas:
            for itemRecord in entrega[1].lista_itens:
                buffer.append([entrega[0], entrega[1].indice + 1, itemRecord.cliente, itemRecord.familia, itemRecord.familia_macro, itemRecord.index, itemRecord.peso])
        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv
        with open(self.path + '\\fdecreasing2.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)

    def outputBPP(self):
        # BPP
        buffer = [] # buffer para escribir en el disco
        buffer.append(['INDICE_BIN','PESO','RUTA','ITEMS'])
        for entrega in self.conteiner_entregas_consolidadas:
            indexes = []
            for itemRecord in entrega[1].lista_itens:
                # indexes.append(itemRecord.index)
                # necesito localizar la posicion de ese item en la lista usando el index, y despues insertar la posicion y no el index.
                indice_loop = 0
                for buffer_item in self.parent.lista_itens.itens2route:
                    if buffer_item.index == itemRecord.index:
                        indice = indice_loop + 1
                        break
                    indice_loop += 1
                indexes.append(indice)
            buffer.append([entrega[1].indice + 1, entrega[1].get_carga(), entrega[0]] + indexes)
        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv

        with open(self.path + '\\BPP.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)
        
        #BPP MASSA
        buffer = [] #buffer para escrever no disco
        buffer.append(['INDICE_BIN', 'PESO','CIUDAD','PESO_ITEMS'])
        for entrega in self.conteiner_entregas_consolidadas:
            indexes = []
            for itemRecord in entrega[1].lista_itens:
                indexes.append(str(itemRecord.peso))
            buffer.append([entrega[1].indice + 1, entrega[1].get_carga(), entrega[0]] + indexes)

        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv

        with open(self.path + '\\BPPMASSA.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)
        


class cBin(object):
    
    def __init__(self):
        self.lista_itens = [] # almacena todos los items por ID. Es la lista de contenido del bin.

    # calcula el peso real absorbido por el bin + o la lista de items de otro bin que queremos insertar, considerando los factores de ajuste, etc.
    '''
    def testa_lista_peso_entra_cacamba(self, item_list, binCap):
        for item in item_list:
            if not self.testa_item_entra_cacamba(item, binCap):
                return (False) #chegamos a algum item que no entrara en la sumatoria de los bins
        return (True) #ciclamos tudo e a lista inteira fornecida entra na caçamba testada
    '''
    # sumo los pesos de todos los items en el bin y el del item a ingresar y comparo con binCap
    def testa_item_entra_cacamba(self, item_test, binCap):
        peso_bin = {} # este objeto retendra los calculos de peso ajustado
        peso_bin['total'] = 0 # almaceno a sumatoria total de volume
        for item_bin in self.lista_itens: # ciclo todos los itens del bin, calculando la sumatoria de pesos, pesos corregidos y por familia
            peso_bin['total'] += item_bin.peso
            
        if (peso_bin['total'] + item_test.peso < binCap):
            return(True)
        else:
            return(False)


    def get_familias(self):
        familias = []
        for item in self.lista_itens:
            familias.append(item.familia)
        return(set(familias)) # unique familias

    def valida_mistura_de_familias(self, familia, compatibilidade_familia): #vou testar a 'familia' fornecida contra todas as familias da bin
        validado = True
        familias_bin = self.get_familias()
        for familia_bin_record in familias_bin:
            if validado:
                if (familia_bin_record == '#N/D') or (familia == '#N/D') or (compatibilidade_familia[familia_bin_record-1][familia-1] == 2): # originalmente el hacia -1, pero creo que en C++ el no cargaba los rotulos asi que testear sin [familia_bin_record-1][familia-1]
                    return False # incompatibles, interrumpe y retorna
        return(True) # fue hasta el final y todas son compatibles

    def soma_entregas(self): # retorna la cantidad de rutas distintas en el bin actual.
        entregas = []
        for item in self.lista_itens:
            entregas.append(item.ruta_item)
        cont = len(set(entregas))
        return(cont) # set = unique

    def get_carga(self):
        carga = 0;
        for item_bin in self.lista_itens: # ciclo todos los items en el bin, calculando la sumatoria de pesos, pesos corregidos y por familia
            carga += item_bin.peso
        return(carga)
