import tkinter as tk
from tkinter import ttk
from forex_python.converter import CurrencyRates
from babel.numbers import format_currency, get_currency_name


class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Moeda")
        self.root.geometry("800x250")

        self.create_widgets()

    def create_widgets(self):
        # Configuração da fonte
        font_style = ("Arial", 12)

        # Rótulo de entrada
        self.input_label = ttk.Label(
            self.root, text="Valor em USD para Moeda:", font=font_style)
        self.input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Entrada para o valor a ser convertido
        self.input_entry = ttk.Entry(self.root, width=15, font=font_style)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)

        # Combobox para selecionar a moeda
        self.currency_combobox = ttk.Combobox(
            self.root, values=self.get_currency_list_with_regions(), font=font_style)
        self.currency_combobox.set("Selecione a Moeda")
        self.currency_combobox.grid(row=0, column=2, padx=10, pady=10)
        self.currency_combobox.bind(
            "<<ComboboxSelected>>", self.update_input_label_and_direction)

        # Combobox para selecionar a direção da conversão
        self.direction_combobox = ttk.Combobox(self.root, values=(
            "USD para Moeda", "Moeda para USD"), font=font_style)
        self.direction_combobox.set("USD para Moeda")
        self.direction_combobox.grid(
            row=1, column=0, columnspan=3, padx=10, pady=10)
        self.direction_combobox.bind(
            "<<ComboboxSelected>>", self.update_input_label_and_direction)

        # Rótulo de saída
        self.output_label = ttk.Label(
            self.root, text="Resultado:", font=font_style)
        self.output_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Rótulo para exibir o resultado
        self.result_label = ttk.Label(self.root, text="", font=font_style)
        self.result_label.grid(row=2, column=1, padx=10, pady=10)

        # Botão de conversão
        self.convert_button = ttk.Button(
            self.root, text="Converter", command=self.convert_currency, style="TButton")
        self.convert_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Estilo para o botão
        self.style = ttk.Style()
        self.style.configure("TButton", font=font_style)

    def get_currency_list_with_regions(self):
        # Obtém a lista de moedas com regiões suportadas pela biblioteca forex-python e babel
        c = CurrencyRates()
        currency_list_with_regions = [f"{currency} ({get_currency_name(
            currency, locale='pt_BR')})" for currency in c.get_rates('USD')]
        # Adiciona o dólar americano como opção padrão
        currency_list_with_regions.insert(0, "USD (Estados Unidos)")
        # Adiciona o real brasileiro como segunda opção
        currency_list_with_regions.insert(1, "BRL (Brasil)")
        return currency_list_with_regions

    def update_input_label_and_direction(self, event):
        selected_currency = self.currency_combobox.get(
        ).split()[0]  # Obtém apenas o código da moeda
        selected_country = self.currency_combobox.get().split(
            "(")[-1].strip(")")
        self.input_label.config(text=f"Valor em USD para {
                                selected_currency} ({selected_country}):")

        if self.direction_combobox.get() == "USD para Moeda":
            self.direction_combobox.set(f"USD para {selected_currency}")
        else:
            self.direction_combobox.set(f"{selected_currency} para USD")

    def convert_currency(self):
        try:
            # Obtém o valor de entrada, a moeda selecionada e a direção da conversão
            value = float(self.input_entry.get())
            # Obtém apenas o código da moeda
            currency = self.currency_combobox.get().split()[0]
            direction = self.direction_combobox.get()

            # Obtém a taxa de câmbio da biblioteca forex-python
            c = CurrencyRates()
            exchange_rate = c.get_rate('USD', currency)

            # Calcula o valor convertido
            if direction.startswith("USD para"):
                result = value * exchange_rate
            else:
                result = value / exchange_rate

            # Exibe o resultado na interface
            self.result_label.config(
                text=f"{format_currency(result, currency, locale='pt_BR')}")
        except ValueError:
            self.result_label.config(text="Valor inválido")


def main():
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
