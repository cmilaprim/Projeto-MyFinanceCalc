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

    def gerar_pdf(self, resultados):
        if not resultados:
            raise ValueError("A lista de resultados está vazia.")

        ultimo_resultado = resultados[-1]
        colunas = list(ultimo_resultado.keys())

        pdf = FPDF(orientation='L', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=9)
        
        caminho_imagem = self.recurso_caminho("assets/logo-empresa.png")
        pdf.image(caminho_imagem, x=10, y=10, w=35)
        pdf.ln(20)
        
        data_abertura = ultimo_resultado.get("Data", "Desconhecida")
        pdf.set_font("Arial", style='B', size=10)
        pdf.cell(0, 10, f"RESULTADO DA APLICAÇÃO FINANCEIRA", ln=True, align='C')
        pdf.ln(2)
        
        col_widths = [pdf.get_string_width(col) + 10 for col in colunas]
        row_height = 5 
        
        pdf.set_fill_color(200, 200, 200)
        pdf.set_font("Arial", style='B', size=9)
        for i, coluna in enumerate(colunas):
            pdf.cell(col_widths[i], row_height, coluna, border=0.2, align='C', fill=True)
        pdf.ln()
        
        pdf.set_font("Arial", size=9)
        for i, chave in enumerate(colunas):
            valor = ultimo_resultado.get(chave, "")
            if isinstance(valor, float):
                valor = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            pdf.cell(col_widths[i], row_height, str(valor), border=0.2, align='C')
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

        colunas = [chave for chave in resultado.keys() if chave != "Selic"]

        pdf = FPDF(orientation='L', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=9)
        
        caminho_imagem = self.recurso_caminho("assets/logo-empresa.png")
        pdf.image(caminho_imagem, x=10, y=10, w=35)
        pdf.ln(20)
        
        data_abertura = resultado.get("Data", "Desconhecida")
        pdf.set_font("Arial", style='B', size=10)
        pdf.cell(0, 10, f"Posição de abertura {data_abertura}", ln=True, align='C')
        pdf.ln(2)
        
        col_widths = [pdf.get_string_width(col) + 10 for col in colunas]
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
            if isinstance(valor, float):
                valor = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            pdf.cell(col_widths[i], row_height, str(valor), border=0.2, align='C')
        pdf.ln()
        
        if not os.path.exists("data"):
            os.makedirs("data")
        
        pdf_path = os.path.abspath("data/resultado.pdf")
        pdf.output(pdf_path)
        print(f"PDF gerado: {pdf_path}")
        os.startfile(pdf_path)
