import weakref, copy
#facundo
class cBinPack(object):
    '''
    Este objeto conservará las bins precargados con los items obtenidos de la lista de SAP.
    Esta lista de items provenientes de SAP será cargada en el objeto de clase cItens.
    El foco de esta clase es poblar las listas siguiendo los algoritmos desarrollados por Leandro.
    '''
    
    def __init__(self, parent):
        '''
        Cada item de estos arrays representa un bin. En cada bin entrarán N objetos
        que podrán ser de uno o más clientes/ciudades.
        Aquí solo inicializamos las listas y variables.
        '''
        self.parent = parent
        self.conteiner_cacambas = [] # este objeto contendrá los bins (CACAMBAS = BINS)
        self.conteiner_entregas_consolidadas = []

    def best_f_decreasing(self): # lista_itens es un array proveniente de objeto de tipo (cItens)variavel -> itens2route - LA INSTÂNCIA E NÃO A ESTATICA, DA CLASE.
        '''
        Efectivamente poblará los arrays con la lista de items cargada en otro objeto (dataframe pandas lista_itens),
        y provista como argumento.
        Crearé los bins en un objeto propio, y las otras listas apuntarán a la posición de cada bin (index).
        '''
        lista_itens = self.parent.lista_itens.itens2route
        binCap = self.parent.info_veiculos.binCap
        metodo_consolidar = self.parent.info_unidades.consolida_cliente_cidade
        compatibilidade_familia = self.parent.info_materiais.compatibilidade_familia
        qt_clientes_max_rota = self.parent.info_unidades.quantidade_clientes_maximo_rota

        cliente_anterior = '0' #TO DO creo que puedo eliminar esta y contagem_bins, ver si uso esto para algo
        itemIndex = 0
        self.contagem_bins = 0

        while itemIndex < len(lista_itens):
            itemRecord = lista_itens[itemIndex]

            if (itemRecord.index == 210): # Probablemente se pueda volar
                a = 1

            if (itemRecord.peso <= binCap): # ¿el bin soporta ese peso?
                item_alocado = False # TO DO creo que puedo incluir en el itemRecord la propriedad bool alocado y excluir eso de aquí.
                cacambaIndex = 0
                for cacambaRecord in self.conteiner_cacambas: # calcular diversos datos DE CADA BIN
                    if (cacambaRecord.testa_item_entra_cacamba(itemRecord, binCap)):
                        if(cacambaRecord.valida_mistura_de_familias(itemRecord.familia, compatibilidade_familia)):
                            if(cacambaRecord.soma_entregas() < qt_clientes_max_rota):
                                self.conteiner_cacambas[cacambaIndex].lista_itens.append(itemRecord) #para economizar memória paso solo la referencia. Si precisa manipular los items de entrada posteriormente, cambiar a deepcopy.
                                item_alocado = True
                                break # interrumpir el loop FOR de los bins
                    cacambaIndex += 1
                    
                if (not item_alocado): #ciclo todos los bins y no consegui ubicar ese item en ninguno. Tendré que generar un bin nuevo para él.
                    self.conteiner_cacambas.append(cBin()) # creo nuevo bin
                    self.conteiner_cacambas[cacambaIndex].lista_itens.append(itemRecord) # guardo el item en este nuevo bin

            else: # peso del item > bincap - ciclar creando nuevos bins para n.int
                bins2create = int(itemRecord.peso // binCap) # división entera
                for i in range(bins2create):
                    self.conteiner_cacambas.append(cBin()) # creo nuevo bin
                    cacambaIndex = len(self.conteiner_cacambas) - 1
                    self.conteiner_cacambas[cacambaIndex].lista_itens.append(copy.deepcopy(itemRecord)) # guardo el item en este nuevo bin
                    self.conteiner_cacambas[cacambaIndex].lista_itens[0].peso = binCap;
                    self.conteiner_cacambas[cacambaIndex].lista_itens[0].volume = binCap/self.conteiner_cacambas[cacambaIndex].lista_itens[0].fator_ajuste;

                lista_itens[itemIndex].peso = itemRecord.peso % binCap # resto para que entre en un bin incompleto
                lista_itens[itemIndex].volume = lista_itens[itemIndex].peso / lista_itens[itemIndex].fator_ajuste

                itemIndex -= 1 # ver si hay un forma de volver 1 step en el for, si existe adecuo el peso del item para ese resto y corro el for de nuevo
            
            itemIndex += 1
               
            if (itemIndex < len(lista_itens)):
                cliente_anterior = itemRecord.cliente # guardo el cliente para el próximo loop
                # testeo si consolidó ese cliente/ciudad
                cliente_posterior = lista_itens[itemIndex].cliente
                meso_anterior = itemRecord.meso_regiao
                meso_posterior = lista_itens[itemIndex].meso_regiao

                if ((metodo_consolidar == 1) and (cliente_posterior != cliente_anterior)) or ((metodo_consolidar == 2) and (meso_posterior != meso_anterior)):
                    # cerramos la consolidación, colocar los datos parciale en el array correspondiente y limpar la fila
                    self.consolida(itemRecord.meso_regiao)
            else:
                self.consolida(itemRecord.meso_regiao) # si consolida por cliente, ¿por qué pasamos región como parámetro?

    def consolida(self, cidade):
        # ¿tenemos bin asignado?
        for binRecord in self.conteiner_cacambas:
            binRecord.indice = self.contagem_bins
            binRecord.rota = -1
            self.conteiner_entregas_consolidadas.append([cidade, binRecord]) # como consolida al cambiar de cliente, solo habrá bins de un cliente, igual que parciales
                                                                             # de esa forma, basta obtener el bin.item.cidade. Al igual que si hubiera más de un item, todas las ciudades serán iguales
            self.contagem_bins += 1
        self.conteiner_cacambas = [] # limpio la lista anterior de bins

    def outputCSV(self):
        buffer = [] # buffer para escribir en el disco
        buffer.append(['CIDADE','INDICE','ROTA','CLIENTE','DESTINO','FAMILIA','FAMILIA_MACRO','FATOR_AJUSTE','INDICE','MESO','PESO','VOLUME'])
        for entrega in self.conteiner_entregas_consolidadas:
            for itemRecord in entrega[1].lista_itens:
                buffer.append([entrega[0], entrega[1].indice, entrega[1].rota, itemRecord.cliente, itemRecord.destino, itemRecord.familia, itemRecord.familia_macro, itemRecord.fator_ajuste, itemRecord.index, itemRecord.meso_regiao, itemRecord.peso, itemRecord.volume])
        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv
        with open('c:\\temp\\fdecreasing2.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)

    def outputBPP(self):
        # BPP
        buffer = [] # buffer para escribir en el disco
        buffer.append(['CONTADOR','MASSA','CIDADE','ITENS'])
        for entrega in self.conteiner_entregas_consolidadas:
            indexes = []
            for itemRecord in entrega[1].lista_itens:
                # indexes.append(itemRecord.index)
                # necesito localizar la posición de ese item en la lista usando el index, y después insertar la posición y no el index.
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

        with open('C:\\Users\\diegog1\\source\\repos\\Python Consolid8\\Python Consolid8\\data\\BPP.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)
        
        #BPP MASSA
        buffer = [] #buffer para escrever no disco
        buffer.append(['CONTADOR', 'MASSA','CIDADE','MASSA DOS ITENS'])
        for entrega in self.conteiner_entregas_consolidadas:
            indexes = []
            for itemRecord in entrega[1].lista_itens:
                indexes.append(str(itemRecord.peso))
                if (itemRecord.index == 364): # Esto probablemente se pueda volar
                    a = 123
            buffer.append([entrega[1].indice + 1, entrega[1].get_carga(), entrega[0]] + indexes)

        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv

        with open('C:\\Users\\diegog1\\source\\repos\\Python Consolid8\\Python Consolid8\\data\\BPPMASSA.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)
        
        #BPP MASSA_REAL
        buffer = [] # buffer para guardar en el disco
        buffer.append(['CONTADOR','MASSA','CIDADE','MASSA DOS ITENS'])
        for entrega in self.conteiner_entregas_consolidadas:
            indexes = []
            for itemRecord in entrega[1].lista_itens:
                indexes.append(str(itemRecord.volume))
            buffer.append([entrega[1].indice + 1, entrega[1].get_volume(), entrega[0]] + indexes)

        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv

        with open('C:\\Users\\diegog1\\source\\repos\\Python Consolid8\\Python Consolid8\\data\\BPPMASSAREAL.txt', 'w') as myfile:
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
                return (False) #chegamos a algum item que no entrará en la sumatoria de los bins
        return (True) #ciclamos tudo e a lista inteira fornecida entra na caçamba testada
    '''

    # calcula el peso real absorbido por el bin + el item que queremos insertar, considerando los factores de ajuste, etc.
    def testa_item_entra_cacamba(self, item_test, binCap):
        # voy a correr todos los items haciendo una sumatoria del peso total y peso por familia.
        volumes = {} # este objeto retendrá los cálculos de peso ajustado
        volumes['total'] = 0 # almaceno a sumatoria total de volume
        volumes['familia'] = {} # almaceno a sumatoria por família
        volumes['familia'] = {1:0, 2:0, 3:0, '#N/D':0}
        
        volumes_real = {} #este objeto retendrá los valores de peso real/volume (no se cuál es el término termino correcto, Leando mezcló los terminos.
        volumes_real['total'] = 0
        volumes_real['familia'] = {}
        volumes_real['familia'] = {1:0, 2:0, 3:0, '#N/D':0}
        
        # TO DO no conseguí identificar para qué Leandro usaba esas diferencias. Estudiar el código y si no se usa para nada, eliminar.
        diferencas = {}
        diferencas['familia'] = {1:0, 2:0, 3:0, '#N/D':0}

        for item_bin in self.lista_itens: # ciclo todos los itens del bin, calculando la sumatoria de pesos, pesos corregidos y por familia
            volumes['total'] += item_bin.peso
            volumes['familia'][item_bin.familia_macro] += item_bin.peso
            volumes_real['total'] += item_bin.volume
            volumes_real['familia'][item_bin.familia_macro] += item_bin.peso/item_bin.fator_ajuste
        
        if (volumes['total'] + item_test.peso < binCap):
            return(True)
        else:
            return(False)

    def get_familias(self):
        familias = []
        for item in self.lista_itens:
            familias.append(item.familia)
        return(set(familias)) # unique familias

    def valida_mistura_de_familias(self, familia, compatibilidade_familia): #vou testar a 'família' fornecida contra todas as familias da bin
        validado = True
        familias_bin = self.get_familias()
        for familia_bin_record in familias_bin:
            if validado:
                if (familia_bin_record == '#N/D') or (familia == '#N/D') or (compatibilidade_familia[familia_bin_record][familia] == 2): # originalmente él hacia -1, pero creo que en C++ él no cargaba los rótulos así que testear sin [familia_bin_record-1][familia-1]
                    return False # incompatibles, interrumpe y retorna
        return(True) # fue hasta el final y todas son compatibles

    def soma_entregas(self): # retorna la sumatoria de entregas (destinos diferentes) en el bin actual
        entregas = []
        for item in self.lista_itens:
            entregas.append(item.meso_regiao)
        cont = len(set(entregas))
        return(cont) # set = unique

    def get_carga(self):
        carga = 0;
        for item_bin in self.lista_itens: # ciclo todos los items en el bin, calculando la sumatoria de pesos, pesos corregidos y por familia
            carga += item_bin.peso
        return(carga)

    def get_volume(self):
        volume = 0;
        for item_bin in self.lista_itens: # ciclo todos los items en el bin, calculando la sumatoria de pesos, pesos corregidos y por familia
            volume += item_bin.volume
        return(volume)