from fpdf import FPDF
import os
import sys

class geraDocumento():
    def __init__(self):
        pass

    def recurso_caminho(self, relativo):
        if getattr(sys, 'frozen', False):  # Se estiver rodando como .exe
            base_caminho = sys._MEIPASS
        else: 
            base_caminho = os.path.abspath(".")

        return os.path.join(base_caminho, relativo)

    def formatar_valor_brasileiro(self, valor, chave=None):
        if isinstance(valor, float):
            if chave in ["Selic", "Percentual CDI", "Aliq IOF"]:
                return f"{valor:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return str(valor)

    def ajustar_largura_colunas(self, pdf, colunas, dados):
        max_largura = pdf.w - 20  # Largura máxima da página com margens
        col_widths = [pdf.get_string_width(col) + 10 for col in colunas]

        for linha in dados:
            for i, valor in enumerate(linha):
                largura_valor = pdf.get_string_width(str(valor)) + 10
                if largura_valor > col_widths[i]:
                    col_widths[i] = largura_valor

        largura_total = sum(col_widths)
        if largura_total > max_largura:
            proporcao = max_largura / largura_total
            col_widths = [largura * proporcao for largura in col_widths]

        return col_widths

    def gerar_pdf(self, resultados):
        if not resultados:
            raise ValueError("A lista de resultados está vazia.")

        ultimo_resultado = resultados[-1]
        
        if "Valor Aplicado" in ultimo_resultado:
            del ultimo_resultado["Valor Aplicado"]
        
        colunas = list(ultimo_resultado.keys())

        pdf = FPDF(orientation='L', format='A4')  # Alterar para paisagem e formato A3
        pdf.add_page()
        pdf.set_font("Arial", size=9)
        
        caminho_imagem = self.recurso_caminho("assets/logo-empresa.png")
        pdf.image(caminho_imagem, x=10, y=10, w=35)
        pdf.ln(20)
        
        data_abertura = ultimo_resultado.get("Data", "Desconhecida")
        pdf.set_font("Arial", style='B', size=15)
        pdf.cell(0, 10, f"RESULTADO DA APLICAÇÃO FINANCEIRA", ln=True, align='C')
        pdf.ln(2)
        
        dados = [[self.formatar_valor_brasileiro(ultimo_resultado.get(chave, ""), chave) for chave in colunas]]
        col_widths = self.ajustar_largura_colunas(pdf, colunas, dados)
        row_height = 5 
        
        pdf.set_fill_color(200, 200, 200)
        pdf.set_font("Arial", style='B', size=9)
        for i, coluna in enumerate(colunas):
            pdf.cell(col_widths[i], row_height, coluna, border=0.2, align='C', fill=True)
        pdf.ln()
        
        pdf.set_font("Arial", size=9)
        for i, chave in enumerate(colunas):
            valor = ultimo_resultado.get(chave, "")
            valor = self.formatar_valor_brasileiro(valor, chave)
            pdf.cell(col_widths[i], row_height, valor, border=0.2, align='C')
        pdf.ln()
        
        if not os.path.exists("data"):
            os.makedirs("data")
        
        pdf_path = os.path.abspath("data/extrato.pdf")
        pdf.output(pdf_path)
        print(f"PDF gerado: {pdf_path}")
        os.startfile(pdf_path)
    
    def gerar_pdf_especifico(self, resultado):
        if not resultado:
            raise ValueError("O resultado está vazio.")

        if "Selic" in resultado:
            del resultado["Selic"]
            
        if "Juros" in resultado:
            del resultado["Juros"]
        
        if "Valor Aplicado" in resultado:
            del resultado["Valor Aplicado"]

        colunas = [chave for chave in resultado.keys() if chave != "Selic"]

        pdf = FPDF(orientation='L', format='A4')  # Alterar para paisagem e formato A3
        pdf.add_page()
        pdf.set_font("Arial", size=9)
        
        caminho_imagem = self.recurso_caminho("assets/logo-empresa.png")
        pdf.image(caminho_imagem, x=10, y=10, w=35)
        pdf.ln(20)
        
        data_abertura = resultado.get("Data", "Desconhecida")
        pdf.set_font("Arial", style='B', size=15)
        pdf.cell(0, 10, f"Posição de abertura {data_abertura}", ln=True, align='C')
        pdf.ln(2)
        
        dados = [[self.formatar_valor_brasileiro(resultado.get(chave, ""), chave) for chave in colunas]]
        col_widths = self.ajustar_largura_colunas(pdf, colunas, dados)
        row_height = 5 
        
        # Centralizar tabela
        largura_total = sum(col_widths)
        x_offset = (pdf.w - largura_total) / 2
        pdf.set_x(x_offset)
        
        pdf.set_fill_color(200, 200, 200)
        pdf.set_font("Arial", style='B', size=9)
        for i, coluna in enumerate(colunas):
            pdf.cell(col_widths[i], row_height, coluna, border=0.2, align='C', fill=True)
        pdf.ln()
        
        pdf.set_x(x_offset)
        pdf.set_font("Arial", size=9)
        for i, chave in enumerate(colunas):
            valor = resultado.get(chave, "")
            valor = self.formatar_valor_brasileiro(valor, chave)
            pdf.cell(col_widths[i], row_height, valor, border=0.2, align='C')
        pdf.ln()
        
        if not os.path.exists("data"):
            os.makedirs("data")
        
        pdf_path = os.path.abspath("data/resultado.pdf")
        pdf.output(pdf_path)
        print(f"PDF gerado: {pdf_path}")
        os.startfile(pdf_path)
