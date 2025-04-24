import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string

class PasswordGenerator:
    def __init__(self):
        self.password_type = tk.StringVar()
        self.password_length = tk.IntVar()
        self.title_var = tk.StringVar()
        self.generated_password_var = tk.StringVar()
        self.password_history = []

    def generate_password(self):
        password_type = self.password_type.get()
        password_length = self.password_length.get()

        if password_type == "numeric":
            generated_password = ''.join(random.choices(string.digits, k=password_length))
        elif password_type == "text":
            characters = string.ascii_letters + string.digits + string.punctuation
            generated_password = ''.join(random.choices(characters, k=password_length))
        else:
            generated_password = "Tipo de senha inválido"

        self.generated_password_var.set(generated_password)

    def save_password(self):
        title = self.title_var.get()
        password = self.generated_password_var.get()

        if title and password:
            self.password_history.append({"title": title, "password": password})
            messagebox.showinfo("Senha Salva", "Senha salva com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Título e senha são obrigatórios para salvar.")

    def delete_password(self, title):
        for entry in self.password_history:
            if entry["title"] == title:
                self.password_history.remove(entry)
                break

    def edit_password(self, title, new_password):
        for entry in self.password_history:
            if entry["title"] == title:
                entry["password"] = new_password
                break

    def get_password_titles(self):
        return [entry["title"] for entry in self.password_history]

    def get_password_by_title(self, title):
        for entry in self.password_history:
            if entry["title"] == title:
                return entry["password"]
        return ""

class PasswordManagerApp:
    def __init__(self, master, password_generator):
        self.master = master
        self.master.title("Gerenciador de Senhas")

        self.password_generator = password_generator

        self.create_widgets()

    def create_widgets(self):
        # Criação de widgets para seleção do tipo de senha
        self.create_password_type_widgets()

        # Criação de widgets para seleção do comprimento da senha
        self.create_password_length_widgets()

        # Criação de widgets para entrada de título
        self.create_title_widgets()

        # Botão para gerar senha
        generate_button = tk.Button(self.master, text="Gerar Senha", command=self.password_generator.generate_password)
        generate_button.pack(pady=20)

        # Bloco de texto para exibir a senha gerada
        password_display = tk.Entry(self.master, textvariable=self.password_generator.generated_password_var, state="readonly", width=30)
        password_display.pack(pady=10)

        # Botões para salvar, excluir e editar
        self.create_action_buttons()

        # Botão para abrir o histórico
        history_button = tk.Button(self.master, text="Histórico", command=self.show_password_history)
        history_button.pack(side="left", padx=10)

    def create_password_type_widgets(self):
        label_type = tk.Label(self.master, text="Selecione o tipo de senha:")
        label_type.pack(pady=10)

        numeric_button = tk.Radiobutton(self.master, text="Numérica", variable=self.password_generator.password_type, value="numeric")
        numeric_button.pack()
        text_button = tk.Radiobutton(self.master, text="Texto", variable=self.password_generator.password_type, value="text")
        text_button.pack()

    def create_password_length_widgets(self):
        label_length = tk.Label(self.master, text="Selecione o comprimento da senha:")
        label_length.pack(pady=10)

        lengths = [4, 6, 8, 10]
        for length in lengths:
            length_button = tk.Radiobutton(self.master, text=str(length), variable=self.password_generator.password_length, value=length)
            length_button.pack()

    def create_title_widgets(self):
        label_title = tk.Label(self.master, text="Título:")
        label_title.pack(pady=10)
        entry_title = tk.Entry(self.master, textvariable=self.password_generator.title_var)
        entry_title.pack()

    def create_action_buttons(self):
        save_button = tk.Button(self.master, text="Salvar", command=self.save_password)
        save_button.pack(side="left", padx=10)

        delete_button = tk.Button(self.master, text="Excluir", command=self.delete_password)
        delete_button.pack(side="left", padx=10)

        edit_button = tk.Button(self.master, text="Editar", command=self.edit_password)
        edit_button.pack(side="left", padx=10)

    def save_password(self):
        self.password_generator.save_password()

    def delete_password(self):
        title = self.password_generator.title_var.get()
        self.password_generator.delete_password(title)

    def edit_password(self):
        title = self.password_generator.title_var.get()
        new_password = self.password_generator.generated_password_var.get()
        self.password_generator.edit_password(title, new_password)

    def show_password_history(self):
        # Criação de uma nova janela para exibir o histórico
        history_window = tk.Toplevel(self.master)
        history_window.title("Histórico de Senhas")

        # Lista de senhas no histórico
        passwords_listbox = tk.Listbox(history_window, selectmode=tk.SINGLE)
        passwords_listbox.pack(pady=10)

        # Preenche a lista com os títulos das senhas
        for title in self.password_generator.get_password_titles():
            passwords_listbox.insert(tk.END, title)

        # Botões para visualizar, excluir e salvar senhas do histórico
        view_button = tk.Button(history_window, text="Visualizar", command=lambda: self.view_history_password(passwords_listbox))
        view_button.pack(side="left", padx=10)

        delete_button = tk.Button(history_window, text="Excluir", command=lambda: self.delete_history_password(passwords_listbox))
        delete_button.pack(side="left", padx=10)

        save_button = tk.Button(history_window, text="Salvar", command=lambda: self.save_history_password(passwords_listbox))
        save_button.pack(side="left", padx=10)

    def view_history_password(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_title = listbox.get(selected_index)
            password = self.password_generator.get_password_by_title(selected_title)
            messagebox.showinfo("Senha Selecionada", f"A senha para '{selected_title}' é:\n\n{password}")

    def delete_history_password(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_title = listbox.get(selected_index)
            self.password_generator.delete_password(selected_title)
            listbox.delete(selected_index)

    def save_history_password(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_title = listbox.get(selected_index)
            password = self.password_generator.get_password_by_title(selected_title)

            # Solicita um novo título para salvar a senha
            new_title = simpledialog.askstring("Salvar Senha", "Digite um novo título para a senha:")
            if new_title:
                # Adiciona a senha ao histórico com o novo título
                self.password_generator.password_history.append({"title": new_title, "password": password})
                messagebox.showinfo("Senha Salva", f"A senha foi salva com o título '{new_title}'.")

if __name__ == "__main__":
    root = tk.Tk()
    password_generator = PasswordGenerator()
    app = PasswordManagerApp(root, password_generator)
    root.mainloop()
