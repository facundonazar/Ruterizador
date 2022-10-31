
#-Begin-----------------------------------------------------------------
'''
Este proyecto es el puerto de Consolid8 original, escrito en C++.
<<<DESCREVER DETALHADAMENTE APOS 1o PROTOTIPO>>>
'''
#-Includes--------------------------------------------------------------

# ruta = '//azrwcfs01acbr/Sectores/Ruteador_DLI/Data/'



import cMateriais
import cUnidades
import cInfofile
import libVeiculos, libItens, libBins
import libClarkWright

class cRoteirizador(object):
    def __init__(self):
        self.path = '//azrwcfs01acbr/Sectores/Ruteador_DLI/Data/'
        self.buffer_infos = cInfofile.cInfos() # guarda los dataframes df1 ("InfosUnidades") y df2 ("txt") del Excel imput.xls
        self.info_unidades = cUnidades.cUnidades(self) # lee df1 y df2 y va guardando la informacion en variables, carga el archivo con distancias entre ciudades
        self.info_materiais = cMateriais.cMateriais(self) # lee df1 y va guardando compatibilidad Macro-Micro y por Familia
        self.info_veiculos = libVeiculos.cVeiculos(self) # lee df1, guarda los tipos de camiones disponibles y guarda capacidad maxima.
        self.lista_itens = libItens.cItens(self) # lista de items para enrutar
        self.lista_bins = libBins.cBinPack(self) # Genera el best_f_decreasing donde consolida items en bins


    def inicializa(self):
        self.info_unidades.load_data()
        self.info_materiais.load_data_familia()
        self.info_materiais.load_data_macro_micro()
        self.info_veiculos.load_data()
        self.lista_itens.load_data()

# roteirizador = cRoteirizador()

# roteirizador.inicializa()
# roteirizador.lista_bins.best_f_decreasing()

# A=roteirizador.lista_bins.conteiner_entregas_consolidadas

# aux=A[0][1]

# lista_itens=aux.lista_itens

# item_record=aux.lista_itens[0]

def Main():
    roteirizador = cRoteirizador()
    print('Proyecto Consolid8 Python')
    print('Instanciando clases de proceso')
    try:
        roteirizador.inicializa()
        #---=== Fin de carga de datos de configuracion ===---
        roteirizador.lista_bins.best_f_decreasing()
        # Hacer un output de la best decreasing para comparacion, excel vs excel
        roteirizador.lista_bins.outputCSV();
        roteirizador.lista_bins.outputBPP();
        
        print('62')
        cw = libClarkWright.cRotasPack()
        cw.genera_combinaciones(roteirizador.lista_bins.conteiner_entregas_consolidadas,
                                roteirizador.info_unidades.df_distancia_cidades, 
                                roteirizador.info_unidades.v_cidade_usina)
        
        print('65')
        cw.dumpEconomiasCSV();
        cw.construye_poblacion(roteirizador.lista_bins.conteiner_entregas_consolidadas,
                               roteirizador.info_veiculos.binCap,
                               roteirizador.info_materiais.compatibilidade_familia, 
                               roteirizador.info_unidades.vraio_consolidacao,
                               roteirizador.info_unidades.cantidad_max_rutas_bsas,
                               roteirizador.info_unidades.cantidad_max_rutas_arg)
        print('nico2')
        cw.outputCKCSV()

        # en este punto, tengo la lista organizada en lista de objetos del tipo cBin.
        # transformar eso en un pandas dataframe y exportar para eggs-cell.

        # for property, value in vars(lista_bins.conteiner_entregas_consolidadas[0][1].lista_itens[0]).keys().iteritems():
        #    print (property, ": ", value)
        #    buffer_df = PendingDeprecationWarning.DataFrame
    except Exception as er:
        print(er)
        pass
        #print(sys.exc_info()[0])
    else:
        pass
    finally:
        pass
#-Main------------------------------------------------------------------
# Si se ejecuta el script directamente, toma el nombre "main". Si es importado, toma el nombre desde donde se lo llama
if __name__ == "__main__":
    Main()

#-End-------------------------------------------------------------------

