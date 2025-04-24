import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


class CadastroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Funcionários")

        # Carregar a planilha diretamente
        self.df = pd.read_excel(r'diterório da planilha')

        self.label_status = ttk.Label(
            root, text="Planilha carregada: Cadastro.xlsx")
        self.label_status.pack(pady=10)

        self.frame_cadastro = ttk.LabelFrame(
            root, text="Cadastro de Funcionários")
        self.frame_cadastro.pack(pady=10)

        # Remova o campo de entrada para o ID
        self.labels = ["Matrícula", "Nome",
                       "Data Nascimento", "Cargo", "Setor", "Salário"]
        self.entries = {}

        for label in self.labels:
            ttk.Label(self.frame_cadastro, text=label).grid(
                row=self.labels.index(label), column=0, sticky="w", padx=10, pady=5)
            self.entries[label] = ttk.Entry(self.frame_cadastro)
            self.entries[label].grid(row=self.labels.index(
                label), column=1, padx=10, pady=5)

        self.button_cadastrar = ttk.Button(
            root, text="Cadastrar Funcionário", command=self.cadastrar_funcionario)
        self.button_cadastrar.pack(pady=10)

    def cadastrar_funcionario(self):
        novo_registro = {}

        # Gere um ID automático baseado no número de registros existentes
        novo_registro["Id"] = len(self.df) + 1

        for label in self.labels:
            novo_registro[label] = self.entries[label].get()

        try:
            # Utilizar o método concat para adicionar uma nova linha ao DataFrame
            self.df = pd.concat([self.df, pd.DataFrame(
                [novo_registro])], ignore_index=True)
            self.atualizar_planilha()
            self.limpar_campos()
            self.mostrar_mensagem("Cadastro efetuado com sucesso!")
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao cadastrar funcionário: {str(e)}")

    def atualizar_planilha(self):
        self.df.to_excel(r'Diretório da Planilha', index=False)
        self.label_status.config(text="Cadastro atualizado na planilha.")

    def limpar_campos(self):
        for label in self.labels:
            self.entries[label].delete(0, tk.END)

    def mostrar_mensagem(self, mensagem):
        messagebox.showinfo("Mensagem", mensagem)


if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroGUI(root)
    root.mainloop()
