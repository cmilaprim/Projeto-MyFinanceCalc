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

        pdf = FPDF(orientation='L', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        caminho_imagem = self.recurso_caminho("assets/logo-empresa.png")

        # Adicionar logo
        pdf.image(caminho_imagem, x=10, y=10, w=35)
        pdf.ln(20)  # Adiciona um espaço após a imagem

        # Cabeçalho
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 10, "Resultado da Aplicação", ln=True, align='C')
        pdf.ln(5)

        # Medidas da página
        margem = 10
        largura_total = pdf.w - 2 * margem  # Considera as margens
        num_colunas = len(ultimo_resultado)

        # Calcular largura ideal das colunas com base no maior conteúdo
        pdf.set_font("Arial", size=10)
        col_widths = []
        for chave, valor in ultimo_resultado.items():
            largura_chave = pdf.get_string_width(chave) + 10
            largura_valor = pdf.get_string_width(str(valor)) + 10
            col_widths.append(max(largura_chave, largura_valor))

        # Normalizar para não ultrapassar a página
        fator_ajuste = largura_total / sum(col_widths)
        col_widths = [largura * fator_ajuste for largura in col_widths]

        row_height = 8  # Altura padrão das linhas

        # Criar cabeçalho da tabela
        pdf.set_font("Arial", style='B', size=10)
        for i, chave in enumerate(ultimo_resultado.keys()):
            pdf.cell(col_widths[i], row_height, chave, border=1, align='C')
        pdf.ln()

        # Preencher dados da tabela
        pdf.set_font("Arial", size=10)
        for i, valor in enumerate(ultimo_resultado.values()):
            if isinstance(valor, float):
                valor = f"{valor:.2f}"  # Formata valores numéricos com 2 casas decimais
            pdf.cell(col_widths[i], row_height, str(valor), border=1, align='C')
        pdf.ln()

        # Criar pasta "data" se não existir
        if not os.path.exists("data"):
            os.makedirs("data")

        # Caminho do PDF
        pdf_path = os.path.abspath("data/resultado.pdf")
        pdf.output(pdf_path)

        # Verifica se o arquivo foi realmente criado
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"O arquivo PDF não foi encontrado em: {pdf_path}")

        print(f"Tentando abrir o arquivo: {pdf_path}")
        os.startfile(pdf_path)
