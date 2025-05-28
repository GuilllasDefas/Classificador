"""Manipulador de erros da aplicação"""

from tkinter import messagebox
from utils.app_constants import Messages

class ErrorHandler:
    """Classe para gerenciar erros da aplicação"""
    
    @staticmethod
    def handle_image_error(error, image_manager, callback):
        """Trata erros ao carregar imagens"""
        messagebox.showerror("Erro", Messages.IMAGE_ERROR.format(str(error)))
        
        # Remove a imagem com problema
        if image_manager.arquivos_imagem:
            image_manager.arquivos_imagem.pop(image_manager.indice_atual)
            
            if image_manager.arquivos_imagem:
                if image_manager.indice_atual >= len(image_manager.arquivos_imagem):
                    image_manager.indice_atual = 0
                image_manager.atualizar_imagem_atual()
                callback()
            else:
                return False
        return True
    
    @staticmethod
    def handle_icon_error(error):
        """Trata erro ao carregar ícone"""
        print(Messages.ICON_ERROR.format(error))
    
    @staticmethod
    def show_no_images_warning():
        """Mostra aviso de nenhuma imagem encontrada"""
        messagebox.showinfo("Sem Imagens", Messages.NO_IMAGES)
    
    @staticmethod
    def show_no_folder_warning():
        """Mostra aviso de nenhuma pasta selecionada"""
        messagebox.showinfo("Aviso", Messages.NO_FOLDER_SELECTED)
