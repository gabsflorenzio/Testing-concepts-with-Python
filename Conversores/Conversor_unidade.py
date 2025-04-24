import tkinter as tk
from tkinter import ttk

class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Unidades")
        self.root.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        # Configuração da fonte
        font_style = ("Arial", 12)

        # Rótulo de entrada
        self.input_label = ttk.Label(self.root, text="Valor:", font=font_style)
        self.input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Entrada para o valor a ser convertido
        self.input_entry = ttk.Entry(self.root, width=15, font=font_style)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)

        # Combobox para selecionar a unidade de entrada
        self.input_unit_combobox = ttk.Combobox(self.root, values=self.get_length_units(), font=font_style)
        self.input_unit_combobox.set("Metros")
        self.input_unit_combobox.grid(row=0, column=2, padx=10, pady=10)

        # Rótulo de saída
        self.output_label = ttk.Label(self.root, text="Resultado:", font=font_style)
        self.output_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Rótulo para exibir o resultado
        self.result_label = ttk.Label(self.root, text="", font=font_style)
        self.result_label.grid(row=1, column=1, padx=10, pady=10)

        # Combobox para selecionar a unidade de saída
        self.output_unit_combobox = ttk.Combobox(self.root, values=self.get_length_units(), font=font_style)
        self.output_unit_combobox.set("Metros")
        self.output_unit_combobox.grid(row=1, column=2, padx=10, pady=10)

        # Combobox para selecionar a categoria de conversão
        self.category_combobox = ttk.Combobox(self.root, values=["Comprimento", "Peso", "Temperatura", "Área", "Volume", "Dados", "Desconto", "Tempo", "IMC"], font=font_style)
        self.category_combobox.set("Comprimento")
        self.category_combobox.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
        self.category_combobox.bind("<<ComboboxSelected>>", self.update_units)

        # Botão de conversão
        self.convert_button = ttk.Button(self.root, text="Converter", command=self.convert_units, style="TButton")
        self.convert_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Estilo para o botão
        self.style = ttk.Style()
        self.style.configure("TButton", font=font_style)

        # Atualiza as unidades com base na categoria inicial
        self.update_units(None)

    def update_units(self, event):
        selected_category = self.category_combobox.get()

        if selected_category == "Comprimento":
            units = self.get_length_units()
        elif selected_category == "Peso":
            units = self.get_weight_units()
        elif selected_category == "Temperatura":
            units = self.get_temperature_units()
        elif selected_category == "Área":
            units = self.get_area_units()
        elif selected_category == "Volume":
            units = self.get_volume_units()
        elif selected_category == "Dados":
            units = self.get_data_units()
        elif selected_category == "Desconto":
            units = self.get_discount_units()
        elif selected_category == "Tempo":
            units = self.get_time_units()
        elif selected_category == "IMC":
            units = self.get_imc_units()
        else:
            units = []

        self.input_unit_combobox["values"] = units
        self.output_unit_combobox["values"] = units
        self.input_unit_combobox.set(units[0])
        self.output_unit_combobox.set(units[0])

    def get_length_units(self):
        return ["Metros", "Quilômetros", "Milhas", "Polegadas"]

    def get_weight_units(self):
        return ["Quilogramas", "Gramas", "Libras", "Onças"]

    def get_temperature_units(self):
        return ["Celsius", "Fahrenheit", "Kelvin"]

    def get_area_units(self):
        return ["Metros Quadrados", "Acres", "Hectares"]

    def get_volume_units(self):
        return ["Litros", "Mililitros", "Galões", "Pints"]

    def get_data_units(self):
        return ["Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte", "Petabyte"]

    def get_discount_units(self):
        return ["Preço Original", "Desconto (%)", "Preço Final"]

    def get_time_units(self):
        return ["Segundo", "Minuto", "Hora", "Dia"]

    def get_imc_units(self):
        return ["IMC"]

    def convert_units(self):
        try:
            # Obtém o valor de entrada e as unidades selecionadas
            value = float(self.input_entry.get())
            input_unit = self.input_unit_combobox.get()
            output_unit = self.output_unit_combobox.get()
            selected_category = self.category_combobox.get()

            # Converte o valor para a unidade padrão da categoria
            value_in_standard_unit = self.convert_to_standard_unit(value, input_unit, selected_category)

            # Converte o valor da unidade padrão para a unidade de saída
            result = self.convert_from_standard_unit(value_in_standard_unit, output_unit, selected_category)

            # Exibe o resultado na interface
            self.result_label.config(text=f"{result:.2f} {output_unit}")
        except ValueError:
            self.result_label.config(text="Valor inválido")

    def convert_to_standard_unit(self, value, unit, category):
        if category == "Comprimento":
            return self.convert_length_to_meters(value, unit)
        elif category == "Peso":
            return self.convert_weight_to_kilograms(value, unit)
        elif category == "Temperatura":
            return self.convert_temperature_to_celsius(value, unit)
        elif category == "Área":
            return self.convert_area_to_square_meters(value, unit)
        elif category == "Volume":
            return self.convert_volume_to_liters(value, unit)
        elif category == "Dados":
            return self.convert_data_to_bytes(value, unit)
        elif category == "Desconto":
            return value  # Nenhuma conversão necessária para cálculos de desconto
        elif category == "Tempo":
            return self.convert_time_to_seconds(value, unit)
        elif category == "IMC":
            return value  # Nenhuma conversão necessária para cálculos de IMC

    def convert_from_standard_unit(self, value, unit, category):
        if category == "Comprimento":
            return self.convert_length_from_meters(value, unit)
        elif category == "Peso":
            return self.convert_weight_from_kilograms(value, unit)
        elif category == "Temperatura":
            return self.convert_temperature_from_celsius(value, unit)
        elif category == "Área":
            return self.convert_area_from_square_meters(value, unit)
        elif category == "Volume":
            return self.convert_volume_from_liters(value, unit)
        elif category == "Dados":
            return self.convert_data_from_bytes(value, unit)
        elif category == "Desconto":
            return value  # Nenhuma conversão necessária para cálculos de desconto
        elif category == "Tempo":
            return self.convert_time_from_seconds(value, unit)
        elif category == "IMC":
            return value  # Nenhuma conversão necessária para cálculos de IMC

    def convert_length_to_meters(self, value, unit):
        if unit == "Metros":
            return value
        elif unit == "Quilômetros":
            return value * 1000
        elif unit == "Milhas":
            return value * 1609.34
        elif unit == "Polegadas":
            return value * 0.0254

    def convert_length_from_meters(self, value, unit):
        if unit == "Metros":
            return value
        elif unit == "Quilômetros":
            return value / 1000
        elif unit == "Milhas":
            return value / 1609.34
        elif unit == "Polegadas":
            return value / 0.0254

    def convert_weight_to_kilograms(self, value, unit):
        if unit == "Quilogramas":
            return value
        elif unit == "Gramas":
            return value / 1000
        elif unit == "Libras":
            return value * 0.453592
        elif unit == "Onças":
            return value * 0.0283495

    def convert_weight_from_kilograms(self, value, unit):
        if unit == "Quilogramas":
            return value
        elif unit == "Gramas":
            return value * 1000
        elif unit == "Libras":
            return value / 0.453592
        elif unit == "Onças":
            return value / 0.0283495

    def convert_temperature_to_celsius(self, value, unit):
        if unit == "Celsius":
            return value
        elif unit == "Fahrenheit":
            return (value - 32) * 5/9
        elif unit == "Kelvin":
            return value - 273.15

    def convert_temperature_from_celsius(self, value, unit):
        if unit == "Celsius":
            return value
        elif unit == "Fahrenheit":
            return value * 9/5 + 32
        elif unit == "Kelvin":
            return value + 273.15

    def convert_area_to_square_meters(self, value, unit):
        if unit == "Metros Quadrados":
            return value
        elif unit == "Acres":
            return value * 4046.86
        elif unit == "Hectares":
            return value * 10000

    def convert_area_from_square_meters(self, value, unit):
        if unit == "Metros Quadrados":
            return value
        elif unit == "Acres":
            return value / 4046.86
        elif unit == "Hectares":
            return value / 10000

    def convert_volume_to_liters(self, value, unit):
        if unit == "Litros":
            return value
        elif unit == "Mililitros":
            return value / 1000
        elif unit == "Galões":
            return value * 3.78541
        elif unit == "Pints":
            return value * 0.473176

    def convert_volume_from_liters(self, value, unit):
        if unit == "Litros":
            return value
        elif unit == "Mililitros":
            return value * 1000
        elif unit == "Galões":
            return value / 3.78541
        elif unit == "Pints":
            return value / 0.473176

    def convert_data_to_bytes(self, value, unit):
        if unit == "Byte":
            return value
        elif unit == "Kilobyte":
            return value * 1024
        elif unit == "Megabyte":
            return value * 1024 ** 2
        elif unit == "Gigabyte":
            return value * 1024 ** 3
        elif unit == "Terabyte":
            return value * 1024 ** 4
        elif unit == "Petabyte":
            return value * 1024 ** 5

    def convert_data_from_bytes(self, value, unit):
        if unit == "Byte":
            return value
        elif unit == "Kilobyte":
            return value / 1024
        elif unit == "Megabyte":
            return value / (1024 ** 2)
        elif unit == "Gigabyte":
            return value / (1024 ** 3)
        elif unit == "Terabyte":
            return value / (1024 ** 4)
        elif unit == "Petabyte":
            return value / (1024 ** 5)

    def convert_discount(self, value, unit):
        # Converte percentagem para fração
        if unit == "Desconto (%)":
            return value / 100
        else:
            return value

    def convert_time_to_seconds(self, value, unit):
        if unit == "Segundo":
            return value
        elif unit == "Minuto":
            return value * 60
        elif unit == "Hora":
            return value * 3600
        elif unit == "Dia":
            return value * 86400

    def convert_time_from_seconds(self, value, unit):
        if unit == "Segundo":
            return value
        elif unit == "Minuto":
            return value / 60
        elif unit == "Hora":
            return value / 3600
        elif unit == "Dia":
            return value / 86400

    def calculate_imc(self, value):
        # IMC é uma medida única
        return value

def main():
    root = tk.Tk()
    app = UnitConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
