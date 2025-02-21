# # from fpdf import FPDF
# # import os
# # import sys

# # class ExtratoPDF(FPDF):
# #     def header(self):
# #         # Adiciona logo
# #         caminho_imagem = self.recurso_caminho("assets/logo-empresa.png")
# #         self.ln(5)
# #         self.image(caminho_imagem, x=10, y=10, w=35)
# #         self.set_font("Arial", style='B', size=15)
# #         self.cell(0, 10, "EXTRATO DE APLICAÇÕES", ln=True, align='C')
# #         self.ln(5)

# #     def recurso_caminho(self, relativo):
# #         if getattr(sys, 'frozen', False):
# #             base_caminho = sys._MEIPASS
# #         else:
# #             base_caminho = os.path.abspath(".")
# #         return os.path.join(base_caminho, relativo)

# #     def gerar_extrato(self, dados):
# #         colunas = ["Data", "Valor Aplicado", "Selic", "Taxa", "Valor Bruto", "Juros", "Acumulado",
# #                    "IOF", "Líquido", "IR", "Rend. Líquido", "Aliq IOF"]
        
# #         self.set_font("Arial", size=9)
# #         col_widths = [22, 28, 18, 18, 28, 22, 28, 18, 28, 18, 30, 18]  
# #         row_height = 5 
        
# #         self.set_fill_color(200, 200, 200)
# #         self.set_font("Arial", style='B', size=9)
# #         for i, coluna in enumerate(colunas):
# #             self.cell(col_widths[i], row_height, coluna, border=0.2, align='C', fill=True)
# #         self.ln()
        
# #         self.set_font("Arial", size=9)
# #         for linha in dados:
# #             for i, chave in enumerate(colunas):
# #                 valor = linha.get(chave, "")
# #                 if isinstance(valor, float):
# #                     valor = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")  
# #                 self.cell(col_widths[i], row_height, str(valor), border=0.2, align='C')
# #             self.ln()
        
# #         if not os.path.exists("data"):
# #             os.makedirs("data")
        
# #         pdf_path = os.path.abspath("data/extrato.pdf")
# #         self.output(pdf_path)
# #         print(f"PDF gerado: {pdf_path}")
# #         os.startfile(pdf_path)

# # # Exemplo de uso
# # dados_exemplo = [
# #     {"Data": "07/02/2025", "Valor Aplicado": 10000.00, "Selic": 0.10, "Taxa": 0.15, "Valor Bruto": 10150.00,
# #      "Juros": 150.00, "Acumulado": 10200.00, "IOF": 5.00, "Líquido": 10195.00, "IR": 22.50, "Rend. Líquido": 100.00,
# #      "Aliq IOF": 0.5}
# # ]

# # extrato = ExtratoPDF(orientation='L', format='A4')
# # extrato.add_page()
# # extrato.gerar_extrato(dados_exemplo)
# from fpdf import FPDF
# import os
# import locale

# class geraDocumento:
#     def recurso_caminho(self, caminho_relativo):
#         return os.path.abspath(caminho_relativo)

#     def gerar_pdf_especifico(self, resultados):
#         if not resultados:
#             raise ValueError("A lista de resultados está vazia.")

#         # Configurar a localidade para o formato brasileiro
#         locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')

#         pdf = FPDF(orientation='L', format='A4')
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)

#         caminho_imagem = self.recurso_caminho("assets/logo-empresa.png")

#         # Adicionar logo
#         pdf.image(caminho_imagem, x=10, y=10, w=35)
#         pdf.ln(20)

#         # Cabeçalho principal
#         pdf.set_font("Arial", style='B', size=12)
#         pdf.cell(0, 10, "Resultado da Aplicação", ln=True, align='C')
#         pdf.ln(5)

#         # Cabeçalho com a data específica
#         data_abertura = resultados.get("Data", "")
#         pdf.set_font("Arial", style='B', size=10)
#         pdf.cell(0, 10, f"Posição de abertura {data_abertura}", ln=True, align='L')
#         pdf.ln(5)

#         # Definir a largura da tabela
#         margem = 10
#         largura_total = pdf.w - 2 * margem  # Considera as margens

#         # Filtrar apenas as chaves desejadas
#         chaves_desejadas = ["Data", "Valor Aplicado", "Selic", "Taxa", "Valor Bruto", "Juros", "Acumulado", "IOF", "Liquido", "IR", "Rend Liquido", "Aliq IOF"]
#         dados_filtrados = {chave: resultados[chave] for chave in chaves_desejadas if chave in resultados}

#         # Calcular largura ideal das colunas
#         pdf.set_font("Arial", size=10)
#         col_widths = []
#         for chave, valor in dados_filtrados.items():
#             largura_chave = pdf.get_string_width(chave) + 10
#             largura_valor = pdf.get_string_width(str(valor)) + 10
#             col_widths.append(max(largura_chave, largura_valor))

#         # Ajustar as larguras para caber na página
#         fator_ajuste = largura_total / sum(col_widths)
#         col_widths = [largura * fator_ajuste for largura in col_widths]
#         row_height = 6  # Reduzindo altura para evitar cortes

#         # Criar cabeçalho da tabela
#         pdf.set_font("Arial", style='B', size=10)
#         for i, chave in enumerate(dados_filtrados.keys()):
#             pdf.cell(col_widths[i], row_height, chave, border=1, align='C')
#         pdf.ln()

#         # Preencher dados da tabela
#         pdf.set_font("Arial", size=10)
#         for i, valor in enumerate(dados_filtrados.values()):
#             if isinstance(valor, (float, int)):
#                 valor = locale.format_string("%.2f", valor, grouping=True)
#             pdf.cell(col_widths[i], row_height, str(valor), border=1, align='C')
#         pdf.ln()

#         # Criar pasta "data" se não existir
#         if not os.path.exists("data"):
#             os.makedirs("data")

#         # Caminho do PDF
#         pdf_path = os.path.abspath("data/resultado.pdf")
#         pdf.output(pdf_path)

#         # Verifica se o arquivo foi realmente criado
#         if not os.path.exists(pdf_path):
#             raise FileNotFoundError(f"O arquivo PDF não foi encontrado em: {pdf_path}")

#         print(f"Tentando abrir o arquivo: {pdf_path}")
#         os.startfile(pdf_path)
        
# from datetime import date

# # Criando um dicionário com os dados da aplicação
# dados_aplicacao = {
#     "Data": "12/02/2025",
#     "Valor Aplicado": 10000.00,
#     "Selic": 11.25,
#     "Taxa": 0.85,
#     "Valor Bruto": 10500.45,
#     "Juros": 500.45,
#     "Acumulado": 10500.45,
#     "IOF": 0.00,
#     "Liquido": 10300.30,
#     "IR": 200.15,
#     "Rend Liquido": 300.30,
#     "Aliq IOF": "0%"
# }

# # Criando o gerador de PDF e passando os dados
# gerador = geraDocumento()
# gerador.gerar_pdf_especifico(dados_aplicacao)
from fpdf import FPDF
import os
import sys

class ExtratoPDF(FPDF):
    def header(self):
        # Adiciona logo
        caminho_imagem = self.recurso_caminho("assets/logo-empresa.png")
        self.ln(5)
        self.image(caminho_imagem, x=10, y=10, w=35)
        self.set_font("Arial", style='B', size=15)
        self.cell(0, 10, "EXTRATO DE APLICAÇÕES", ln=True, align='C')
        self.ln(5)

    def recurso_caminho(self, relativo):
        if getattr(sys, 'frozen', False):
            base_caminho = sys._MEIPASS
        else:
            base_caminho = os.path.abspath(".")
        return os.path.join(base_caminho, relativo)

    def gerar_extrato(self, dados):
        if not dados:
            raise ValueError("A lista de dados está vazia.")

        colunas = ["Data", "Valor Aplicado", "Selic", "Taxa", "Valor Bruto", "Juros", "Acumulado",
                   "IOF", "Líquido", "IR", "Rend. Líquido", "Aliq IOF"]

        self.set_font("Arial", size=9)
        col_widths = [22, 28, 18, 18, 28, 22, 28, 18, 28, 18, 30, 18]  
        row_height = 5 
        
        # Pegando a data da primeira aplicação para o título
        data_abertura = dados[0].get("Data", "Desconhecida")

        # Adiciona título com a data da aplicação
        self.set_font("Arial", style='B', size=10)
        self.cell(0, 10, f"Posição de abertura {data_abertura}", ln=True, align='C')
        self.ln(2)

        # Criar cabeçalho da tabela
        self.set_fill_color(200, 200, 200)
        self.set_font("Arial", style='B', size=9)
        for i, coluna in enumerate(colunas):
            self.cell(col_widths[i], row_height, coluna, border=0.2, align='C', fill=True)
        self.ln()
        
        # Preencher os dados
        self.set_font("Arial", size=9)
        for linha in dados:
            for i, chave in enumerate(colunas):
                valor = linha.get(chave, "")
                if isinstance(valor, float):
                    valor = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")  
                self.cell(col_widths[i], row_height, str(valor), border=0.2, align='C')
            self.ln()
        
        if not os.path.exists("data"):
            os.makedirs("data")
        
        pdf_path = os.path.abspath("data/extrato.pdf")
        self.output(pdf_path)
        print(f"PDF gerado: {pdf_path}")
        os.startfile(pdf_path)

# Exemplo de uso com várias aplicações
dados_exemplo = [
    {"Data": "12/02/2025", "Valor Aplicado": 1000000000.00, "Selic": 0.10, "Taxa": 0.15, "Valor Bruto": 100000150.00,
     "Juros": 150.00, "Acumulado": 10200.00, "IOF": 5.00, "Líquido": 10195.00, "IR": 22.50, "Rend. Líquido": 100.00,
     "Aliq IOF": 0.5}
]

extrato = ExtratoPDF(orientation='L', format='A4')
extrato.add_page()
extrato.gerar_extrato(dados_exemplo)
