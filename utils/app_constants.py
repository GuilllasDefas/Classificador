"""Constantes da aplicação"""

class WindowConfig:
    """Configurações da janela principal"""
    TITLE = "Classificador de Imagens"
    GEOMETRY = "1600x900"
    ICON_PATH = "assets/icon.ico"

class Colors:
    """Cores da interface"""
    BACKGROUND = "#23272e"
    FOREGROUND = "#ffffff"
    BUTTON_BACKGROUND = "#373e4c"
    BUTTON_HOVER = "#4d5565"
    BUTTON_CORRECT = "#28a745"
    BUTTON_CORRECT_HOVER = "#218838"
    BUTTON_WRONG = "#dc3545"
    BUTTON_WRONG_HOVER = "#c82333"
    STATUS_BACKGROUND = "#1c1f26"
    IMAGE_LABEL_BACKGROUND = "#1c1f26"
    IMAGE_LABEL_FOREGROUND = "#dcdfe4"
    
    # Novas cores para botões especiais
    BUTTON_SPECIAL = "#17a2b8"  # Azul turquesa
    BUTTON_SPECIAL_HOVER = "#138496"  # Azul turquesa mais escuro
    DIALOG_BACKGROUND = "#282c34"  # Fundo do diálogo
    DIALOG_FRAME = "#21252b"  # Frames dentro do diálogo

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
