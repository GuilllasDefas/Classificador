"""Constantes da aplicação"""

class WindowConfig:
    """Configurações da janela principal"""
    TITLE = "Classificador de Imagens"
    GEOMETRY = "1600x900"
    ICON_PATH = "assets/icon.ico"

class Colors:
    """Cores da interface"""
    BACKGROUND = "#23272e"
    FOREGROUND = "#f0f0f0"
    BUTTON_CORRECT = "#2ecc40"
    BUTTON_WRONG = "#e74c3c"
    BUTTON_CORRECT_HOVER = "#27ae60"
    BUTTON_WRONG_HOVER = "#c0392b"
    BUTTON_HOVER = "#555"
    BUTTON_NEUTRAL = "#444"
    STATUS_BACKGROUND = "#181a1b"
    IMAGE_LABEL_BACKGROUND = "#181a1b"
    IMAGE_LABEL_FOREGROUND = "#ffd700"

class Fonts:
    """Configurações de fontes"""
    DEFAULT = ("Arial", 12)
    BUTTON = ("Arial", 14, "bold")
    IMAGE_NAME = ("Arial", 16, "bold")

class Padding:
    """Valores de padding e margem"""
    MAIN = 30
    BUTTON = 12
    IMAGE_FRAME = 20
    TOP_LABEL = 10

class ButtonConfig:
    """Configurações dos botões"""
    HEIGHT = 2
    WIDTH_NORMAL = 12
    WIDTH_SELECT = 16
    RELIEF = "raised"
    BORDER_WIDTH = 2

class Messages:
    """Mensagens da aplicação"""
    SELECT_FOLDER = "Selecione uma pasta para começar a classificar imagens"
    NO_IMAGES = "Nenhuma imagem encontrada na pasta selecionada."
    ALL_CLASSIFIED = "Todas as imagens foram classificadas!"
    NO_FOLDER_SELECTED = "Nenhuma pasta foi selecionada ainda."
    IMAGE_ERROR = "Não foi possível abrir a imagem: {}"
    ICON_ERROR = "Não foi possível carregar o ícone: {}"
