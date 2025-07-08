import os
# Fix for clipboard provider error on Linux. Must be set before Kivy imports.
os.environ['KIVY_CLIPBOARD'] = 'kivy'

import json
from datetime import datetime
import matplotlib.pyplot as plt

# Kivy imports
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import DictProperty
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase


# --- IMPORTANT FONT SETUP ---
# You can find NotoEmoji here: https://fonts.google.com/noto/specimen/Noto+Emoji
FONT_EMOJI = './assets/fonts/NotoEmoji-Regular.ttf'


# Import for integrating Matplotlib with Kivy
# This can fail if the garden package is not installed correctly.
try:
    from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
except ImportError:
    # Provide a helpful error message and instructions if the module is not found.
    print("="*80)
    print("ERRO: O módulo Matplotlib do Kivy Garden não foi encontrado.")
    print("Este é um problema comum de instalação.")
    print("Por favor, instale-o usando o seguinte comando no seu terminal:")
    print("pip install kivy-garden.matplotlib")
    print("="*80)
    # Exit gracefully or raise an exception to stop the app from crashing later.
    raise


# Path to the data file
DATA_FILE = "dados_imc.json"

# Available emojis
EMOJIS = ["😵", "😒", "😅", "😉", "🤩"]

# --- Helper Functions (from original code) ---
def carregar_dados():
    """Loads saved data from the JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []  # Return empty list if file is corrupted or unreadable
    return []

def salvar_dados(dados):
    """Saves data to the JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def calcular_imc(peso, altura):
    """Calculates BMI."""
    return round(peso / (altura ** 2), 2)

def classificar_imc(imc):
    """Classifies BMI according to standard ranges."""
    if imc < 18.5:
        return "Abaixo do Peso"
    elif 18.5 <= imc < 25:
        return "Peso Ideal"
    elif 25 <= imc < 30:
        return "Pré-obesidade"
    elif 30 <= imc < 35:
        return "Obesidade Grau I"
    elif 35 <= imc < 40:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"

# --- Custom Widgets ---
class IMCRecordRow(ButtonBehavior, GridLayout):
    """Represents a single clickable row in the history list."""
    record_data = DictProperty({})

class DetailsPopup(Popup):
    """Custom popup to display the details of a record. It holds the record data."""
    record = DictProperty({})

class MainLayout(BoxLayout):
    """The root widget of the application."""
    pass

# --- Main Application Class ---
class IMCWolfByteApp(App):
    def build(self):
        if os.path.exists(FONT_EMOJI):
            LabelBase.register(name='EmojiFont', fn_regular=FONT_EMOJI)
        else:
            print(f"AVISO: Arquivo de fonte para emoji não encontrado em '{FONT_EMOJI}'. Emojis podem não ser exibidos.")

        self.title = "IMC-WolfByte"
        self.registros = carregar_dados()
        self.emoji_selecionado = ""
        self.emoji_botoes = {}

        self.main_layout = MainLayout()
        
        self.create_emoji_buttons()
        self.atualizar_lista()
        
        return self.main_layout

    def create_emoji_buttons(self):
        """Dynamically creates the emoji selection buttons."""
        emoji_box = self.main_layout.ids.emoji_box
        for e in EMOJIS:
            btn = Button(
                text=e, 
                font_size='20sp',
                # Use the emoji font for the buttons as well
                font_name='EmojiFont',
                on_release=self.selecionar_emoji,
                background_normal='', 
                background_color=get_color_from_hex('#0b0b26')
            )
            emoji_box.add_widget(btn)
            self.emoji_botoes[e] = btn

    def selecionar_emoji(self, instance):
        """Handles emoji selection, updating the UI."""
        self.emoji_selecionado = instance.text
        for button in self.emoji_botoes.values():
            button.background_color = get_color_from_hex('#0b0b26')
        instance.background_color = get_color_from_hex('#025e73')

    def adicionar_registro(self):
        """Adds a new BMI record."""
        try:
            peso_str = self.main_layout.ids.entry_peso.text.replace(",", ".")
            altura_str = self.main_layout.ids.entry_altura.text.replace(",", ".")
            
            if not peso_str or not altura_str:
                raise ValueError("Campos de peso e altura são obrigatórios.")

            peso = float(peso_str)
            altura = float(altura_str)

            if not (0.5 <= altura <= 2.5):
                raise ValueError("Altura inválida (deve ser entre 0.5m e 2.5m).")
            if not (20 <= peso <= 300):
                raise ValueError("Peso inválido (deve ser entre 20kg e 300kg).")

            novo_dado = {
                "data": datetime.now().strftime("%Y-%m-%d"), 
                "peso": peso, 
                "altura": altura,
                "nota": self.emoji_selecionado, 
                "comentario": self.main_layout.ids.entry_comentario.text,
                "imc": calcular_imc(peso, altura), 
                "classificacao": classificar_imc(calcular_imc(peso, altura)),
            }

            self.registros.append(novo_dado)
            salvar_dados(self.registros)
            self.atualizar_lista()
            
            self.main_layout.ids.entry_peso.text = ""
            self.main_layout.ids.entry_altura.text = ""
            self.main_layout.ids.entry_comentario.text = ""
            
            self.show_popup("IMC Salvo", f"IMC: {novo_dado['imc']}\nClassificação: {novo_dado['classificacao']}")

        except ValueError as e:
            self.show_popup("Erro de Validação", str(e))
        except Exception as e:
            self.show_popup("Erro Inesperado", f"Ocorreu um erro: {e}")

    def atualizar_lista(self):
        """Updates the history list on the screen with the current data."""
        history_list = self.main_layout.ids.history_list
        history_list.clear_widgets()
        
        self.registros.sort(key=lambda x: x.get("data", ""), reverse=True)
        
        for item in self.registros:
            row = IMCRecordRow(record_data=item)
            history_list.add_widget(row)

    def mostrar_detalhes(self, record):
        popup = DetailsPopup(record=record)
        popup.open()

    def mostrar_grafico(self):
        """Shows a popup with the BMI evolution graph."""
        if len(self.registros) < 2:
            self.show_popup("Dados Insuficientes", "São necessários pelo menos 2 registros para exibir um gráfico.")
            return

        dados_ordenados = sorted(self.registros, key=lambda x: x['data'])
        ultimos_14_registros = dados_ordenados[-14:]
        datas = [item['data'] for item in ultimos_14_registros]
        imcs = [item['imc'] for item in ultimos_14_registros]

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0b0b26')
        ax.set_facecolor('#06061b')
        ax.plot(datas, imcs, marker='o', color='#00ffff')
        
        ax.set_title("Evolução do IMC (Últimos 14)", color='white')
        ax.set_xlabel("Data", color='white')
        ax.set_ylabel("IMC", color='white')
        ax.tick_params(axis='x', colors='white', rotation=45)
        ax.tick_params(axis='y', colors='white')
        ax.spines['top'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.grid(True, color='#151570', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        canvas = FigureCanvasKivyAgg(plt.gcf())
        popup = Popup(title="Evolução do IMC", content=canvas, size_hint=(0.9, 0.8))
        popup.open()

    def show_popup(self, title, text):
        """Generic function to show a simple popup message."""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=text, halign='center'))
        close_button = Button(text="Ok", size_hint_y=None, height=dp(44))
        content.add_widget(close_button)
        
        popup = Popup(title=title, content=content, size_hint=(0.75, 0.4))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    IMCWolfByteApp().run()
