import tkinter as tk
from tkinter import messagebox
from calcula_aplicacao import Aplicacao
from gera_documento import geraDocumento
import pickle
import os
from historico import Historico

class TelaInicial:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação Financeira")
        self.root.geometry("400x300")

        # Campos de entrada
        tk.Label(root, text="Nome da Aplicação").grid(row=0, column=0, padx=10, pady=10)
        self.nome_aplicacao = tk.Entry(root)
        self.nome_aplicacao.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Data Inicial (dd/mm/aaaa)").grid(row=1, column=0, padx=10, pady=10)
        self.data_inicial = tk.Entry(root)
        self.data_inicial.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Data Final (dd/mm/aaaa)").grid(row=2, column=0, padx=10, pady=10)
        self.data_final = tk.Entry(root)
        self.data_final.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(root, text="Valor da Aplicação").grid(row=3, column=0, padx=10, pady=10)
        self.valor_aplicacao = tk.Entry(root)
        self.valor_aplicacao.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(root, text="Taxa Selic (%)").grid(row=4, column=0, padx=10, pady=10)
        self.taxa_selic = tk.Entry(root)
        self.taxa_selic.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(root, text="Percentual CDI (%)").grid(row=5, column=0, padx=10, pady=10)
        self.percentual_cdi = tk.Entry(root)
        self.percentual_cdi.grid(row=5, column=1, padx=10, pady=10)

        # Botões
        button_frame = tk.Frame(root)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="Calcular e Exportar PDF", command=self.calcular_exportar).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Ver Históricos", command=self.abrir_historico).pack(side=tk.LEFT, padx=5)

    def calcular_exportar(self):
        try:
            nome = self.nome_aplicacao.get()
            valor = self.valor_aplicacao.get().replace('.', '').replace(',', '.')
            valor = float(valor)
            data_inicial = self.data_inicial.get()
            data_final = self.data_final.get()
            taxa_selic = self.taxa_selic.get().replace(',', '.')
            taxa_selic = float(taxa_selic)
            percentual_cdi = self.percentual_cdi.get().replace(',', '.')
            percentual_cdi = float(percentual_cdi)

            aplicacao = Aplicacao(valor, taxa_selic, percentual_cdi, data_inicial, data_final)
            resultados = aplicacao.calcula_aplicacao()
            gerador = geraDocumento()
            gerador.gerar_pdf(resultados)

            caminho_historico = "data/historico.pkl"
            historico = []

            if os.path.exists(caminho_historico) and os.path.getsize(caminho_historico) > 0:
                with open(caminho_historico, "rb") as f:
                    historico = pickle.load(f)

            historico.append({"Nome": nome, "Valor": valor, "Data Inicial": data_inicial, "Data Final": data_final, "Taxa Selic": taxa_selic, "Percentual CDI": percentual_cdi, "Resultados": resultados})

            with open(caminho_historico, "wb") as f:
                pickle.dump(historico, f)

            messagebox.showinfo("Sucesso", "Cálculo realizado e PDF exportado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def abrir_historico(self):
        self.root.destroy()
        root_historico = tk.Tk()
        app_historico = Historico(root_historico)
        root_historico.mainloop()
