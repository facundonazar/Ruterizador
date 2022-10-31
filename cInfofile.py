import pandas as pd

class cInfos(object):
    filename = 'input.xlsx'
    filename2 = 'Parametros_entrada_Consolid8.xlsx'
    path = '//azrwcfs01acbr/Sectores/Ruteador_DLI/Data/'

    def __init__(self):
       
        print('Abriendo archivo emitido por la macro PREPARA MODELO - INPUT.XLS')

        self.xl = pd.ExcelFile(type(self).path + type(self).filename)
        if (self.xl == 0):
            raise FileNotFoundError
            
        self.xl2 = pd.ExcelFile(type(self).path + type(self).filename2)
        if (self.xl2 == 0):
            raise FileNotFoundError

        # cargo las cuatro pestanas de interes en el dataframes de pandas
        self.df1 = self.xl2.parse('InfosUnidades', header=None, index_col=None)
        self.df2 = self.xl.parse('txt',index_col=None)
        self.df3 = self.xl2.parse('Mallas',index_col=None)
        self.df4 = self.xl2.parse('Familia',index_col=None)
        self.df5 = self.xl2.parse('TF', index_col=None)
        
        self.df = pd.merge(self.df2, self.df4 [['cod Material', 'Familia Micro', 'Familia Macro']], left_on='N_MATERIAL', right_on='cod Material', how= 'left')
        self.df = pd.merge(self.df, self.df3[['Codigo','Peso_Max_Camion(t)']], left_on='N_MATERIAL', right_on='Codigo', how='left')
        self.df = pd.merge(self.df, self.df5[['Itin.','Destino']], left_on='RUTA', right_on='Itin.', how='left')
        
        #Ruta+Destinatario
        self.df['CONCAT']= self.df['DESTINATARIO']+self.df['RUTA']
        
        self.df.sort_values(by=['CONCAT'])
        
        #Indice
        self.df['indice'] = self.df.reset_index().index+1
        
        #N°Cliente
        self.df['nro_cliente'] = pd.factorize(self.df['CONCAT'])[0] + 1
        
        #Output DF
        self.df.to_excel(r'//azrwcfs01acbr/Sectores/Ruteador_DLI/Data/outputcompleto.xlsx', sheet_name="output", index= None, header= True)
        
    def seta_path(self, path): # Suministrar el path SIN BARRA FINAL
        self.path = self.path + '\\'
        

output= cInfos()
