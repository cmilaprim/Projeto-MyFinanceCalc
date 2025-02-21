import datetime
from gera_documento import geraDocumento

class Aplicacao:
    def __init__(self, valor, taxa, porcentagem, data_inicial, data_final):
        self.valor = valor  
        self.taxa = taxa 
        self.porcentagem = porcentagem 
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.resultados = []

    def calcula_periodo(self):
        data_inicial = datetime.datetime.strptime(self.data_inicial, '%d/%m/%Y')
        data_final = datetime.datetime.strptime(self.data_final, '%d/%m/%Y')
        dias = (data_final - data_inicial).days
        return dias, data_inicial

    def calcular_iof(self, dias):
        tabela_iof = {
            1: 0.96, 2: 0.93, 3: 0.90, 4: 0.86, 5: 0.83, 6: 0.80, 7: 0.76, 8: 0.73, 9: 0.70, 10: 0.66, 11: 0.63,
            12: 0.60, 13: 0.56, 14: 0.53, 15: 0.50, 16: 0.46, 17: 0.43, 18: 0.40, 19: 0.36, 20: 0.33, 21: 0.30, 
            22: 0.26, 23: 0.23, 24: 0.20, 25: 0.16, 26: 0.13, 27: 0.10, 28: 0.06, 29: 0.03, 30: 0.00
        }
        
        if dias in tabela_iof:
            return tabela_iof[dias]
        else:
            return 0.0
    
    def calcular_ir(self, dias):    
        if dias <= 180:
            return 0.225
        elif 181 <= dias <= 360:
            return 0.20
        elif 361 <= dias <= 720:
            return 0.175
        else:
            return 0.15
        
    def calcula_aplicacao(self, nova_taxa=None, data_taxa_nova=None):
        dias, data_inicial = self.calcula_periodo()
        taxa_diaria = ((1 + self.taxa / 100) ** (1 / 252) - 1)  
        forumula = taxa_diaria * (self.porcentagem / 100)
        valor_aplicado = self.valor
        acumulado = 0

        self.resultados = []  # Reinicia a lista de resultados

        for i in range(dias+1):
            data_atual = data_inicial + datetime.timedelta(days=i)
            if data_atual.weekday() >= 5:  # Pula fins de semana
                continue

            # Verifica se a taxa deve ser alterada no dia atual
            if data_taxa_nova and data_atual.strftime('%d/%m/%Y') == data_taxa_nova:
                self.taxa = nova_taxa
                taxa_diaria = ((1 + self.taxa / 100) ** (1 / 252) - 1)
                forumula = taxa_diaria * (self.porcentagem / 100)
                # O valor aplicado no dia da mudança de taxa é o valor bruto do dia anterior
                if i > 0:
                    valor_aplicado = float(self.resultados[-1]["Valor Aplicado"])

            if i == 0:
                juros = 0
                valor_bruto = valor_aplicado
            else:
                valor_aplicado += juros
                juros = valor_aplicado * forumula
                valor_bruto = valor_aplicado + juros
            
            acumulado += juros

            aliquota_iof = self.calcular_iof(i) if i < 30 else 0
            iof_dia = acumulado * aliquota_iof

            liquido = acumulado - iof_dia
            ir = liquido * self.calcular_ir(i)
            rendimento_liquido = liquido - ir
            aliquota_iof = aliquota_iof * 100

            resultado = {
                "Data": data_atual.strftime('%d/%m/%Y'),
                "Valor inicial": self.valor,
                "Valor Aplicado": valor_aplicado,
                "Selic": self.taxa,
                "Percentual CDI": self.porcentagem,
                "Valor Bruto": valor_bruto,
                "Juros": juros,
                "Acumulado": acumulado,
                "IOF": iof_dia,
                "Liquido": liquido,
                "IR": ir,
                "Rend Liquido": rendimento_liquido,
                "Aliq IOF": aliquota_iof 
            }

            self.resultados.append(resultado)
        
        return self.resultados
    
# aplicacao = Aplicacao(250, 12.15, 100, "09/01/2025", "05/03/2025")
# resultados = aplicacao.calcula_aplicacao()

# for resultado in resultados:
#     print(resultado)