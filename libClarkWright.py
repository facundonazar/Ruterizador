import itertools
import libBins, libItens, copy

class cRotasPack(object):    
    """
    Esta clase contiene los algoritmos necesarios para el cálculo de costo por el método de Clark & Wright.
    Las listas ordenadas con las rutas estarán dentro de este mismo objeto.
    El constructor solo va a crear los arrays de instancia.
    """

    def __init__(self):
        self.conteiner_economias = []   # va a retener una lista de items del tipo cEconomiaItem
        self.conteiner_rotas = []       # contendrá la población de Clark Wright
        self.conteiner_rotas_bins = []  # temporario para debug, después borrar

    # tendré un array con los N bins en main.lista_bins.conteiner_entregas_consolidadas
    # preciso hacer el ciclo por cada permutación posible

    def gera_combinacoes(self, conteiner_entregas_consolidadas, matriz_distancia_cidades, v_cidade_usina):
        for combo in itertools.combinations(conteiner_entregas_consolidadas, 2):  # aquí tendremos combo[0,1] con cada combinación posible de las entregas consolidadas
            recordEconomia = cEconomiaItem(combo, matriz_distancia_cidades, v_cidade_usina) # creo un registro para cada combinación de ciudades possible (dentro del universo de la lista de items)
            self.conteiner_economias.append(recordEconomia)
        self.conteiner_economias.sort(key=lambda econoRec: econoRec.economia, reverse = True)

    def constroe_populacao(self, conteiner_entregas_consolidadas, binCap, matriz_compatibilidade_familia, raio_consolidacao, qt_max_clientes):
        contador = -1
        for econoItem in self.conteiner_economias: # para cada item de la lista de economias (matriz con todas las combinaciones posibles entre entregas consolidadas)
            # econoItem traerá un par de bins en una supuesta ruta calculada
            contador += 1

            bin1 = conteiner_entregas_consolidadas[econoItem.indiceBin1][1]
            bin2 = conteiner_entregas_consolidadas[econoItem.indiceBin2][1]

            # if ((bin1.indice == 59 and bin2.indice == 58) or (bin1.indice == 58 and bin2.indice == 59)):
            #     a = 1
            # if ((bin1.indice == 59 and bin2.indice == 52) or (bin1.indice == 52 and bin2.indice == 59)):
            #     a = 1
            if ((bin1.rota == -1) and (bin2.rota == -1)):   # testea si uno de los bins ya fue asignado en una ruta previa
            # si ninguno está asignado crea nueva ruta.  # obtiene las cargas de los dos bins, qt de clientes de las dos y hace el testeo de si se pueden juntar las dos en uno solo
                cenario = 1
                quantidade_clientes_no1 = bin1.soma_entregas()
                quantidade_clientes_no2 = bin2.soma_entregas()
                if (self.valida_volume_absorvido(cenario, econoItem, conteiner_entregas_consolidadas, binCap)): # antiguo resultado_soma, se refiere al peso real de los dos nodos
                    if ((quantidade_clientes_no1 + quantidade_clientes_no2) <= qt_max_clientes):
                        if (econoItem.distancia < raio_consolidacao):
                            if (self.valida_mistura_de_familias(1, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia)):
                                roteiro = len(self.conteiner_rotas)
                                self.conteiner_rotas.append(cRota(roteiro))
                                self.conteiner_rotas[roteiro].insere_entregas(bin1.lista_itens)
                                self.conteiner_rotas[roteiro].insere_entregas(bin2.lista_itens)
                                
                                self.conteiner_rotas_bins.append(cRota(roteiro))
                                self.conteiner_rotas_bins[roteiro].insere_entregas(bin1)
                                self.conteiner_rotas_bins[roteiro].insere_entregas(bin2)
                                
                                bin1.rota = roteiro;
                                bin2.rota = roteiro;

                                # if (roteiro==11):
                                #     a = 666
             
            elif ((bin1.rota != -1) and (bin2.rota == -1)): # transporte 1 ya asignado
                cenario = 2
                roteiro_1 = bin1.rota
                rota1 = self.conteiner_rotas[roteiro_1];
                ponta_esquerda = rota1.entregas[0] # adquiero los bins de las esquinas de esta entrega
                ponta_direita = rota1.entregas[len(rota1.entregas)-1]
                quantidade_clientes_no1 = rota1.total_clientes(conteiner_entregas_consolidadas)
                quantidade_clientes_no2 = bin2.soma_entregas()
                if (self.valida_volume_absorvido(cenario, econoItem, conteiner_entregas_consolidadas, binCap)): # antiguo resultado_soma, se refiere al peso real de los dos nodos
                    if ((quantidade_clientes_no1 + quantidade_clientes_no2) <= qt_max_clientes):
                        if (econoItem.distancia < raio_consolidacao):
                            if (self.valida_mistura_de_familias(1, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia)):
                                if (econoItem.indiceBin1 == ponta_esquerda or econoItem.indiceBin1 == ponta_direita):
                                    self.conteiner_rotas[roteiro_1].insere_entregas(bin2.lista_itens)
                                    self.conteiner_rotas_bins[roteiro_1].insere_entregas(bin2)
                                    bin2.rota = roteiro;
                                    
            elif ((conteiner_entregas_consolidadas[econoItem.indiceBin1][1].rota == -1) and (conteiner_entregas_consolidadas[econoItem.indiceBin2][1].rota != -1)): # Transporte 2 ya alocado
                cenario = 3
                roteiro_2 = bin2.rota
                rota2 = self.conteiner_rotas[roteiro_2];
                ponta_esquerda = rota2.entregas[0]
                ponta_direita = rota2.entregas[len(rota2.entregas)-1]
                quantidade_clientes_no1 = bin1.soma_entregas()
                quantidade_clientes_no2 = rota2.total_clientes(conteiner_entregas_consolidadas)
                if (self.valida_volume_absorvido(cenario, econoItem, conteiner_entregas_consolidadas, binCap)): #antigo resultado_soma, se refere ao peso real dos dois nós
                    if ((quantidade_clientes_no1 + quantidade_clientes_no2) <= qt_max_clientes):
                        if (econoItem.distancia < raio_consolidacao):
                            if (self.valida_mistura_de_familias(1, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia)):
                                if (econoItem.indiceBin2 == ponta_esquerda or econoItem.indiceBin2 == ponta_direita):
                                    self.conteiner_rotas[roteiro_2].insere_entregas(bin1.lista_itens)
                                    self.conteiner_rotas_bins[roteiro_2].insere_entregas(bin1)
                                    bin1.rota = roteiro;

            else: # ambos asignados
                cenario = 4
                roteiro_1 = bin1.rota
                rota1 = self.conteiner_rotas[roteiro_1]
                rota1_bin = self.conteiner_rotas_bins[roteiro_1]
                ponta_esquerda_1 = rota1.entregas[0] # adquiero los bins de las esquinas de esta entrega
                ponta_direita_1 = rota1.entregas[len(rota1.entregas)-1]

                roteiro_2 = bin2.rota
                rota2 = self.conteiner_rotas[roteiro_2]
                rota2_bin = self.conteiner_rotas_bins[roteiro_2]
                ponta_esquerda_2 = rota2.entregas[0]
                ponta_direita_2 = rota2.entregas[len(rota2.entregas)-1]

                if (roteiro_1 < roteiro_2):
                    roteiro_atual = roteiro_1
                    roteiro_absorvido = roteiro_2
                else:
                    roteiro_atual = roteiro_2
                    roteiro_absorvido = roteiro_1
                
                quantidade_clientes_no1 = rota1.total_clientes(conteiner_entregas_consolidadas)
                quantidade_clientes_no2 = rota2.total_clientes(conteiner_entregas_consolidadas)

                if (self.valida_volume_absorvido(cenario, econoItem, conteiner_entregas_consolidadas, binCap)):
                    if ((quantidade_clientes_no1 + quantidade_clientes_no2) < qt_max_clientes):
                        if (econoItem.distancia < raio_consolidacao):
                            if (self.valida_mistura_de_familias(1, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia)): #
                                if (roteiro_absorvido != roteiro_atual): # junta las rotas que no excedan la capacidad de un bin, que no excedan el radio y que no estén en la misma ruta
                                    noesquerdo_absorvido = self.conteiner_rotas[roteiro_absorvido].roteiro;
                                    nodireito_absorvido = self.conteiner_rotas[roteiro_absorvido].size() - 1;
                                    noesquerdo_prevalece = self.conteiner_rotas[roteiro_atual].roteiro;
                                    nodireito_prevalece = self.conteiner_rotas[roteiro_atual].size() - 1;

                                    if ((roteiro_1 == ponta_esquerda_1 or roteiro_1 == ponta_direita_1) and (roteiro_1 == ponta_esquerda_2 or roteiro_1 == ponta_direita_2) or (roteiro_2 == ponta_esquerda_1 or roteiro_2 == ponta_direita_1) and (roteiro_2 == ponta_esquerda_2 or roteiro_2 == ponta_direita_2)):
                                        if (noesquerdo_prevalece == roteiro_1 or noesquerdo_prevalece == roteiro_2): # el enlace es con el nodo izquierdo
                                            if (noesquerdo_absorvido == roteiro_1 or noesquerdo_absorvido == roteiro_2): # izquierdo con izquierdo
                                                rota1.insert(0,rota2.entregas)
                                                rota1_bin.insere_entregas(rota2.entregas)#
                                            elif (nodireito_absorvido == roteiro_1 or nodireito_absorvido == roteiro_2): # si es izquierdo con derecho
                                                rota1.insert(0,rota2.entregas)
                                        elif (nodireito_prevalece == roteiro_1 or nodireito_prevalece == roteiro_2): # si es con derecho
                                            if (noesquerdo_absorvido == roteiro_1 or noesquerdo_absorvido == roteiro_2): # derecho con izquierdo
                                                rota1.insert(len(rota2.entregas),rota2.entregas)
                                            elif (nodireito_absorvido == roteiro_1 or nodireito_absorvido == roteiro_2): # derecho con derecho
                                                rota1.insert(len(rota2.entregas),rota2.entregas)
                                        
                                        for binIndex in rota1.entregas: # notifico las cargas que fueran movidas a la nueva ruta de la nueva ruta asimilada
                                            conteiner_entregas_consolidadas[binIndex].rota = roteiro_atual

                                        for binIndex in rota2.entregas: # notifico las cargas que fueran movidas a la nueva ruta de la nueva ruta asimilada
                                            conteiner_entregas_consolidadas[binIndex].rota = roteiro_atual

        for entrega in conteiner_entregas_consolidadas: # barrida final, quien quedó solo se lo asigna a una nueva ruta
            # entrega[1] es la entrega
            if (entrega[1].rota == -1):
                roteiro = len(self.conteiner_rotas)
                entrega[1].rota = roteiro
                self.conteiner_rotas.append(cRota(roteiro))
                self.conteiner_rotas[roteiro].insere_entregas(entrega[1].lista_itens)

                self.conteiner_rotas_bins.append(cRota(roteiro))
                self.conteiner_rotas_bins[roteiro].insere_entregas(entrega[1])

    def valida_mistura_de_familias(self, cenario, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia):
        if (cenario == 1): # ninguno de los bins asignados, bate bin x bin para ver compatibilidade
            familias_bin1 = conteiner_entregas_consolidadas[econoItem.indiceBin1][1].get_familias()
            for familia in familias_bin1:
                 if (familia == '#N/D') or not (conteiner_entregas_consolidadas[econoItem.indiceBin2][1].valida_mistura_de_familias(familia, matriz_compatibilidade_familia)):
                     return(False) # encontró alguna incompatibilid, paraliza y devuelve la incomptabilidad.
            return(True) # testeó todas y no dió ningún error
        if (cenario == 2): # Transporte 1 asignado, calcula compatibilidad de todas las familias de rota1 para bin2
            rota = self.conteiner_rotas[bin1.rota];
            for binIndex in rota.entregas:
                familias_bin = conteiner_entregas_consolidadas[binIndex].get_familias()
                for familia in familias_bin:
                    if (familia == '#N/D') or not (conteiner_entregas_consolidadas[econoItem.indiceBin2][1].valida_mistura_de_familias(familia, matriz_compatibilidade_familia)):
                        return(False) # encontró alguna incompatibilid, paraliza y devuelve la incomptabilidad.
            return (True)
        if (cenario == 3): # Transporte 2 asignado, calcula compatibilidad de todas las familias de rota2 para bin1
            rota = self.conteiner_rotas[bin2.rota];
            for binIndex in rota.entregas:
                familias_bin = conteiner_entregas_consolidadas[binIndex].get_familias()
                for familia in familias_bin:
                    if (familia == '#N/D') or not (conteiner_entregas_consolidadas[econoItem.indiceBin1][1].valida_mistura_de_familias(familia, matriz_compatibilidade_familia)):
                        return(False) # encontró alguna incompatibilid, paraliza y devuelve la incomptabilidad.
            return (True)
        if (cenario == 4): # ambos transportes asignados, calcula todos los items de remessa1 para todos los bins de transpote 2
            rota1 = self.conteiner_rotas[bin1.rota];
            rota2 = self.conteiner_rotas[bin2.rota];
            for binIndex_r1 in rota1.entregas:
                familias_bin_r1 = conteiner_entregas_consolidadas[binIndex_r1].get_familias()
                #p/cada familia de cada bin de la ruta 1, testear compatibilidad con todos los bins de la ruta 1
                for familia in familias_bin_r1:
                    for binIndex_r2 in rota2.entregas:
                        if (familia == '#N/D') or not (conteiner_entregas_consolidadas[binIndex_r2].valida_mistura_de_familias(familia, matriz_compatibilidade_familia)):
                            return(False) # encontró alguna incompatibilid, paraliza y devuelve la incomptabilidad.
            return (True)
        return(False)

    def valida_volume_absorvido(self, cenario, econoItem, conteiner_entregas_consolidadas, binCap): #verifica se todos os itens da 1a bin entram na 2a bin
        bin1 = conteiner_entregas_consolidadas[econoItem.indiceBin1][1]
        roteiro_1 = bin1.rota
        bin2 = conteiner_entregas_consolidadas[econoItem.indiceBin2][1]
        roteiro_2 = bin2.rota
        
        bin1_buffer = copy.deepcopy(bin1) # para efectuar las operaciones de testeo
        bin2_buffer = copy.deepcopy(bin2) # para efectuar las operaciones de testeo
        if (cenario == 1): # puedo testear si el volumen es suficiente sumando los dos bins en un esquema de items bin2 -> bin1
            for item in bin1.lista_itens:
                if (bin2_buffer.testa_item_entra_cacamba(item, binCap)): # entra, insertar el item y seguir al próximo
                    bin2_buffer.lista_itens.append(item) # guardo el item en este nuevo bin
                else:
                   return(False)
            return(True)
        elif (cenario == 2): # rota1 ya definida, verificar todos los bins de ruta 1 + a bin2
            rota1 = self.conteiner_rotas[roteiro_1]
            for binIndex_r1 in rota1.entregas:
                for item in binIndex_r1:
                    if bin2_buffer.testa_item_entra_cacamba(item, binCap):
                        bin2_buffer.lista_itens.append(item)
                    else:
                        return(False)
            return(True)
        elif (cenario == 3): # ruta 2 ya definida pero bin1 no asignado
            rota2 = self.conteiner_rotas[roteiro_2] # obtengo la ruta2 que ya está definida
            for binIndex_r2 in rota2.entregas:
                for item in binIndex_r2:
                    if bin1_buffer.testa_item_entra_cacamba(item, binCap):
                        bin1_buffer.lista_itens.append(item)
                    else:
                        return(False)
            return(True)
        elif (cenario == 4): #ambas
            # en las otras verificaba con el algoritmo implementado en testa_item_entra_cacamba.
            # en esta de aquí, Leandro hizo suma simple y directa. Como para llegar aquí el ajuste ya fue hecho en las otras, puede ser que sea adminisible.
            # pero creo que debería sumar las dos rutas en un bin virtual y testear
            rota1 = self.conteiner_rotas[roteiro_1]
            rota2 = self.conteiner_rotas[roteiro_2] # obtiene la ruta2 que ya está definida
            buffer_bin = libBins.cBin() # bin vacío

            for buffer_entrega in rota1.entregas: # meto todo de la ruta 1 en él
                for item in buffer_entrega:
                    if buffer_bin.testa_item_entra_cacamba(item, binCap):
                        buffer_bin.lista_itens.append(item)
                    else:
                        return(False)

            for buffer_entrega in rota2.entregas:
                for item in buffer_entrega:
                    if buffer_bin.testa_item_entra_cacamba(item, binCap):
                        buffer_bin.lista_itens.append(item)
                    else:
                        return(False)
            return(True)
        
    def dumpEconomiasCSV(self):
        buffer = [] # buffer para escribir en el disco
        
        buffer.append(['ECONOMIA','BIN1','BIN2','DIST','CID#1','CID#2'])
        for entrega in self.conteiner_economias:
            buffer.append([str(entrega.economia), str(entrega.indiceBin1 + 1), str(entrega.indiceBin2 + 1), str(entrega.distancia), str(entrega.cidade1), str(entrega.cidade2)])

        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv

        with open('c:\\temp\\economias.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)

    def dumpCKCSV(self):
        buffer = [] # buffer para grabar en el disco
        
        buffer.append(['ROTEIRO','ID ITEM','CLIENTE','DEST','FAM','FAM_MACRO','FAT.AJ','MESO','PESO','VOL'])
        for conteiner_entrega in self.conteiner_rotas:
            for entrega in conteiner_entrega.entregas:
                for item in entrega:
                    buffer.append([str(conteiner_entrega.roteiro), str(item.index), str(item.cliente), str(item.destino), str(item.familia), str(item.familia_macro), str(item.fator_ajuste), str(item.meso_regiao), str(item.peso), str(item.volume)])

        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv

        with open('c:\\temp\\ck.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)

    def outputCKCSV(self):
        buffer = [] # buffer para grabar en el disco
        
        buffer.append(['CONTADOR','MASSA','NÓS'])
        for conteiner_entrega in self.conteiner_rotas_bins:
            indexes = []
            carga = 0
            for entrega in conteiner_entrega.entregas:
                indexes.append(entrega.indice + 1)
                carga += entrega.get_carga() #TO DO posible bug, ver si debemos usar la carga real o la aparente
            buffer.append([str(conteiner_entrega.roteiro+1), str(carga)] + indexes)
        import csv
        with open('C:\\Users\\diegog1\\source\\repos\\Python Consolid8\\Python Consolid8\\data\\CK.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)

class cRota:
    def __init__(self, roteiro):
        self.roteiro = roteiro;
        self.entregas = []; # array con los índices de los bins

    def insere_entregas(self, indiceBin):   # insertar las entregas del bin en esta ruta
        self.entregas.append(indiceBin)     # las entregas de este bin ahora son de esta ruta 

    def total_clientes(self, conteiner_entregas_consolidadas):
        clientes = []
        for entrega in self.entregas:
            for item in entrega: #conteiner_entregas_consolidadas[entrega][1].lista_itens:
                clientes.append(item.cliente)
        return(len(set(clientes)))

    def testa_lista_peso_entra_rota(self, lista_itens_2_test, binCap):
        somatoria = 0
        for entrega in self.entregas:
            for item in conteiner_entregas_consolidadas[entrega][1].lista_itens:
                somatoria += item.peso
        for item in lista_itens:
            somatoria += item.peso
        if (somatoria <= binCap):
            return (True)
        else:
            return (False)

class cEconomiaItem:
    def __init__(self, combo, matriz_distancia_cidades, v_cidade_usina):
        # combo es un par de valores de entregas oriundas de main.lista_bins.conteiner_entregas_consolidadas
        # o sea, combo[0/1] serán dos bins, con sus respectivos internos como lista_itens
        self.cidade1 = combo[0][1].lista_itens[0].meso_regiao
        self.indiceBin1 = combo[0][1].indice
        self.cidade2 = combo[1][1].lista_itens[0].meso_regiao
        self.indiceBin2 = combo[1][1].indice
        self.distancia = int(matriz_distancia_cidades.iloc[self.cidade1-1][self.cidade2]) # distancia entre ciudades del item economía
        distancia_usina_cidade1 = int(matriz_distancia_cidades.iloc[v_cidade_usina-1][self.cidade1]); # distancia entre usina y ciudad 1
        distancia_usina_cidade2 = int(matriz_distancia_cidades.iloc[v_cidade_usina-1][self.cidade2]); # distancia entre usina y ciudad 2
        self.economia = distancia_usina_cidade1 + distancia_usina_cidade2 - self.distancia
        