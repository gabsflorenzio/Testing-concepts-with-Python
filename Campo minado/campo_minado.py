import tkinter as tk
from tkinter import ttk, messagebox
import random

class ConfiguracaoInicial:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuração Inicial")

        self.label = tk.Label(root, text="Escolha a Dificuldade:")
        self.label.pack(pady=10)

        dificuldades = ["Fácil", "Médio", "Difícil", "Impossível"]
        self.dificuldade_var = tk.StringVar()
        self.dificuldade_var.set(dificuldades[0])

        dificuldade_menu = ttk.Combobox(root, textvariable=self.dificuldade_var, values=dificuldades)
        dificuldade_menu.pack(pady=10)

        iniciar_button = tk.Button(root, text="Iniciar Jogo", command=self.iniciar_jogo)
        iniciar_button.pack(pady=10)

    def iniciar_jogo(self):
        dificuldade = self.dificuldade_var.get()
        if dificuldade == "Fácil":
            linhas, colunas, minas = 8, 8, 10
        elif dificuldade == "Médio":
            linhas, colunas, minas = 12, 12, 20
        elif dificuldade == "Difícil":
            linhas, colunas, minas = 16, 16, 40
        elif dificuldade == "Impossível":
            linhas, colunas, minas = 20, 20, 80
        else:
            messagebox.showerror("Erro", "Dificuldade inválida.")
            return

        self.root.destroy()
        iniciar_jogo(linhas, colunas, minas)

class CampoMinado:
    def __init__(self, root, linhas, colunas, minas):
        self.root = root
        self.linhas = linhas
        self.colunas = colunas
        self.minas = minas
        self.botoes = [[None for _ in range(colunas)] for _ in range(linhas)]
        self.bombas_restantes = minas
        self.criar_menu()
        self.criar_tabuleiro()
        self.plantar_minas()

    def criar_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        jogo_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Jogo", menu=jogo_menu)
        jogo_menu.add_command(label="Reiniciar", command=self.reiniciar_jogo)

    def criar_tabuleiro(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                button = tk.Button(self.root, width=4, height=2, command=lambda i=i, j=j: self.clicar(i, j))
                button.grid(row=i, column=j, padx=2, pady=2)
                self.botoes[i][j] = button

        self.bombas_restantes_label = tk.Label(self.root, text=f"Bombas Restantes: {self.bombas_restantes}")
        self.bombas_restantes_label.grid(row=self.linhas, columnspan=self.colunas, pady=5)

        reiniciar_button = tk.Button(self.root, text="Reiniciar Jogo", command=self.reiniciar_jogo)
        reiniciar_button.grid(row=self.linhas + 1, columnspan=self.colunas, pady=5)

    def plantar_minas(self):
        minas = random.sample(range(self.linhas * self.colunas), self.minas)
        for mina in minas:
            linha = mina // self.colunas
            coluna = mina % self.colunas
            self.botoes[linha][coluna].mina = True

    def clicar(self, linha, coluna):
        if hasattr(self.botoes[linha][coluna], 'mina') and self.botoes[linha][coluna].mina:
            self.botoes[linha][coluna].config(text="X", state=tk.DISABLED, disabledforeground="red")
            messagebox.showinfo("Fim de jogo", "Você atingiu uma mina! Fim de jogo.")
            self.reiniciar_jogo()
        else:
            count_minas = self.contar_minas_vizinhas(linha, coluna)
            self.botoes[linha][coluna].config(text=str(count_minas), state=tk.DISABLED, disabledforeground="black")
            if count_minas == 0:
                self.revelar_vizinhanca(linha, coluna)
            if self.verificar_vitoria():
                messagebox.showinfo("Parabéns", "Você venceu! Parabéns!")
                self.reiniciar_jogo()

    def contar_minas_vizinhas(self, linha, coluna):
        count = 0
        for i in range(max(0, linha - 1), min(self.linhas, linha + 2)):
            for j in range(max(0, coluna - 1), min(self.colunas, coluna + 2)):
                if hasattr(self.botoes[i][j], 'mina') and self.botoes[i][j].mina:
                    count += 1
        return count

    def revelar_vizinhanca(self, linha, coluna):
        for i in range(max(0, linha - 1), min(self.linhas, linha + 2)):
            for j in range(max(0, coluna - 1), min(self.colunas, coluna + 2)):
                if not hasattr(self.botoes[i][j], 'mina') and self.botoes[i][j]['state'] == tk.NORMAL:
                    self.clicar(i, j)

    def verificar_vitoria(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if not hasattr(self.botoes[i][j], 'mina') and self.botoes[i][j]['state'] == tk.NORMAL:
                    return False
        return True

    def reiniciar_jogo(self):
        self.root.destroy()
        iniciar_jogo(self.linhas, self.colunas, self.minas)

def iniciar_jogo(linhas, colunas, minas):
    root = tk.Tk()
    root.title("Campo Minado")
    campo_minado = CampoMinado(root, linhas, colunas, minas)
    root.mainloop()

if __name__ == "__main__":
    root_config = tk.Tk()
    configuracao_inicial = ConfiguracaoInicial(root_config)
    root_config.mainloop()
