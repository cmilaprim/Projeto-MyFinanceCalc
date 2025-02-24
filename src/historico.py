import tkinter as tk
from tkinter import messagebox
from gera_documento import geraDocumento
import pickle
from calcula_aplicacao import Aplicacao
import os


class Historico:
    def __init__(self, root):
        self.root = root
        self.root.title("Histórico de Aplicações")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 750
        window_height = 400

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.lista_aplicacoes = tk.Listbox(root)
        self.lista_aplicacoes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.carregar_historico()

        # Botões
        tk.Button(root, text="Adicionar Nova Aplicação", command=self.adicionar_aplicacao).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text="Editar", command=self.editar_aplicacao).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text="Excluir", command=self.excluir_aplicacao).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text="Alterar Taxa Selic", command=self.alterar_taxa_selic).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text="Voltar", command=self.voltar).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text="Visualizar PDF", command=self.visualizar_pdf).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text="Visualizar por Data", command=self.visualizar_data).pack(side=tk.LEFT, padx=10, pady=10)


    def carregar_historico(self):
        try:
            with open("data/historico.pkl", "rb") as f:
                if os.path.getsize("data/historico.pkl") > 0:  # Verifica se o arquivo não está vazio
                    historico = pickle.load(f)
                    for aplicacao in historico:
                        self.lista_aplicacoes.insert(tk.END, aplicacao["Nome"])
                else:
                    messagebox.showinfo("Info", "Nenhum histórico encontrado.")
        except FileNotFoundError:
            messagebox.showinfo("Info", "Nenhum histórico encontrado.")

    def adicionar_aplicacao(self):
        from tela_inicial import TelaInicial 
        self.root.destroy()  
        root_inicial = tk.Tk()
        app_inicial = TelaInicial(root_inicial)
        root_inicial.mainloop()

    def editar_aplicacao(self):
        selecionado = self.lista_aplicacoes.curselection()
        if selecionado:
            index = selecionado[0]
            with open("data/historico.pkl", "rb") as f:
                historico = pickle.load(f)
            aplicacao = historico[index]
            self.abrir_editor(aplicacao, index, historico) 
        else:
            messagebox.showwarning("Aviso", "Nenhuma aplicação selecionada.")

    def abrir_editor(self, aplicacao, index, historico): 
        
        editor = tk.Toplevel(self.root)
        editor.title("Editar Aplicação")

        tk.Label(editor, text="Nome da Aplicação").grid(row=0, column=0, padx=10, pady=10)
        nome_aplicacao = tk.Entry(editor)
        nome_aplicacao.insert(0, aplicacao["Nome"])
        nome_aplicacao.grid(row=0, column=1, padx=10, pady=10)

        def salvar_edicao():
            aplicacao["Nome"] = nome_aplicacao.get()
            historico[index] = aplicacao
            with open("data/historico.pkl", "wb") as f:
                pickle.dump(historico, f)

            messagebox.showinfo("Sucesso", "Aplicação editada com sucesso!")
            editor.destroy()
            self.lista_aplicacoes.delete(0, tk.END)
            self.carregar_historico()

        tk.Button(editor, text="Salvar", command=salvar_edicao).grid(row=1, column=0, columnspan=2, pady=10)

    def excluir_aplicacao(self):
        selecionado = self.lista_aplicacoes.curselection()
        if selecionado:
            index = selecionado[0]
            with open("data/historico.pkl", "rb") as f:
                historico = pickle.load(f)
            historico.pop(index)
            with open("data/historico.pkl", "wb") as f:
                pickle.dump(historico, f)
            self.lista_aplicacoes.delete(0, tk.END)
            self.carregar_historico()
        else:
            messagebox.showwarning("Aviso", "Nenhuma aplicação selecionada.")

    def alterar_taxa_selic(self):
        selecionado = self.lista_aplicacoes.curselection()
        if selecionado:
            index = selecionado[0]
            with open("data/historico.pkl", "rb") as f:
                historico = pickle.load(f)
            aplicacao = historico[index]

            editor_taxa = tk.Toplevel(self.root)
            editor_taxa.title("Alterar Taxa Selic")

            tk.Label(editor_taxa, text="Nova Taxa Selic (%)").grid(row=0, column=0, padx=10, pady=10)
            nova_taxa = tk.Entry(editor_taxa)
            nova_taxa.grid(row=0, column=1, padx=10, pady=10)

            tk.Label(editor_taxa, text="Data da Mudança (dd/mm/aaaa)").grid(row=1, column=0, padx=10, pady=10)
            data_mudanca = tk.Entry(editor_taxa)
            data_mudanca.grid(row=1, column=1, padx=10, pady=10)

            def salvar_taxa():
                nova_taxa_valor = nova_taxa.get().replace(',', '.')
                nova_taxa_valor = float(nova_taxa_valor)
                data_mudanca_valor = data_mudanca.get()

                aplicacao_obj = Aplicacao(
                    aplicacao["Valor"], 
                    aplicacao["Taxa Selic"], 
                    aplicacao["Percentual CDI"], 
                    aplicacao["Data Inicial"], 
                    aplicacao["Data Final"]
                )
                for mudanca in aplicacao.get("Mudancas Taxa", []):
                    aplicacao_obj.adiciona_mudanca_taxa(mudanca[0], mudanca[1])
                aplicacao_obj.adiciona_mudanca_taxa(nova_taxa_valor, data_mudanca_valor)
                aplicacao["Resultados"] = aplicacao_obj.calcula_aplicacao()

                aplicacao["Mudancas Taxa"] = aplicacao_obj.mudancas_taxa

                with open("data/historico.pkl", "wb") as f:
                    pickle.dump(historico, f)

                messagebox.showinfo("Sucesso", "Taxa Selic alterada e PDF gerado com sucesso!")
                editor_taxa.destroy()

                gerador = geraDocumento()
                gerador.gerar_pdf(aplicacao["Resultados"])

                self.lista_aplicacoes.delete(0, tk.END)
                self.carregar_historico()

            tk.Button(editor_taxa, text="Salvar e Gerar PDF", command=salvar_taxa).grid(row=2, column=0, columnspan=2, pady=10)
        
        else:
            messagebox.showwarning("Aviso", "Nenhuma aplicação selecionada.")

                
    def visualizar_pdf(self):
        selecionado = self.lista_aplicacoes.curselection()
        if selecionado:
            index = selecionado[0]
            with open("data/historico.pkl", "rb") as f:
                historico = pickle.load(f)
            aplicacao = historico[index]
            gerador = geraDocumento()
            gerador.gerar_pdf(aplicacao["Resultados"])
        else:
            messagebox.showwarning("Aviso", "Nenhuma aplicação selecionada.")
    
    def visualizar_data(self):
        selecionado = self.lista_aplicacoes.curselection()
        if selecionado:
            index = selecionado[0]
            with open("data/historico.pkl", "rb") as f:
                historico = pickle.load(f)
            aplicacao = historico[index]
            inserir_data = tk.Toplevel(self.root)
            inserir_data.title("Visualizar aplicação por data")
            
            tk.Label(inserir_data, text="Dia da aplicação (dd/mm/aaaa): ").grid(row=0, column=0, padx=10, pady=10)
            data_aplicacao = tk.Entry(inserir_data)
            data_aplicacao.grid(row=0, column=1, padx=10, pady=10)
            
            def buscar_aplicacao():
                data = data_aplicacao.get()
                aplicacao_encontrada = None
                
                for resultado in aplicacao["Resultados"]:
                    if resultado["Data"] == data:
                        aplicacao_encontrada = resultado
                        break
                
                if aplicacao_encontrada:
                    if "Selic" in aplicacao_encontrada:
                        del aplicacao_encontrada["Selic"]
                    
                    gerador = geraDocumento()
                    gerador.gerar_pdf_especifico(aplicacao_encontrada)
                    messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")
                else:
                    messagebox.showwarning("Aviso", "Nenhuma aplicação encontrada para a data fornecida.")
            
            tk.Button(inserir_data, text="Buscar", command=buscar_aplicacao).grid(row=1, column=0, columnspan=2, pady=10)
        else:
            messagebox.showwarning("Aviso", "Nenhuma aplicação selecionada.")

    def voltar(self):
        from tela_inicial import TelaInicial
        self.root.destroy()  # Fecha a tela de histórico
        root_inicial = tk.Tk()
        app_inicial = TelaInicial(root_inicial)
        root_inicial.mainloop()
