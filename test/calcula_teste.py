import sys
sys.path.append('C:/Users/Administrador/Desktop/Projeto-MyFinanceCalc/src')
 
from calcula_aplicacao import Aplicacao
from gera_documento import geraDocumento

# Exemplo de uso

aplicacao = Aplicacao(250, 12.15, 100, '09/01/2025', '05/03/2025')
aplicacao.calcula_aplicacao()
geraDocumento = geraDocumento()

print("Aplicação de R$250,00 com taxa de 12.15% ao ano e 100% do CDI")
for resultado in aplicacao.resultados:
    print(resultado)

resultados = aplicacao.calcula_aplicacao(nova_taxa=10, data_taxa_nova='27/01/2025')
geraDocumento.gerar_pdf(resultados)