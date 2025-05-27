"""Funções auxiliares para a interface do usuário"""

import tkinter as tk
from constants.app_constants import Colors, Fonts, ButtonConfig

class UIHelpers:
    """Classe com métodos auxiliares para UI"""
    
    @staticmethod
    def create_styled_button(parent, text, command=None, state=tk.NORMAL, 
                           bg_color=Colors.BUTTON_NEUTRAL, fg_color=Colors.FOREGROUND,
                           hover_color=Colors.BUTTON_HOVER, width=None):
        """Cria um botão com estilo padrão"""
        button_config = {
        "text": text, "command": command, "state": state,
        "bg": bg_color, "fg": fg_color,
        "activebackground": hover_color, "activeforeground": fg_color,
        "font": Fonts.BUTTON, "height": ButtonConfig.HEIGHT,
        "relief": ButtonConfig.RELIEF, "bd": ButtonConfig.BORDER_WIDTH
        }
        
        if width is None:
            width = ButtonConfig.WIDTH_NORMAL

        return tk.Button(parent, **button_config)
    
    @staticmethod
    def create_styled_label(parent, text="", bg_color=Colors.BACKGROUND, 
                          fg_color=Colors.FOREGROUND, font=Fonts.DEFAULT, **kwargs):
        """Cria um label com estilo padrão"""
        return tk.Label(parent, text=text, bg=bg_color, fg=fg_color, font=font, **kwargs)
    
    @staticmethod
    def create_styled_frame(parent, bg_color=Colors.BACKGROUND):
        """Cria um frame com estilo padrão"""
        return tk.Frame(parent, bg=bg_color)
