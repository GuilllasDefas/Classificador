import tkinter as tk
from tkinter import filedialog
import os
import sys

from models.image_manager import ImageManager
from utils.image_utils import ImageProcessor
from utils.ui_helpers import UIHelpers
from utils.error_handler import ErrorHandler
from mixins.keyboard_mixin import KeyboardMixin
from constants.app_constants import (
    WindowConfig, Colors, Fonts, Padding, ButtonConfig, Messages
)

def resource_path(relative_path):
    """Obter caminho absoluto para recurso, funciona para dev e para PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MainWindow(KeyboardMixin):
    """Classe principal da interface gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.image_manager = ImageManager()
        
        self._configurar_janela()
        self._configurar_interface()
        self.configurar_atalhos()
    
    def _configurar_janela(self):
        """Configura as propriedades básicas da janela"""
        self.root.title(WindowConfig.TITLE)
        self.root.geometry(WindowConfig.GEOMETRY)
        self.root.resizable(True, True)
        self._carregar_icone()
    
    def _carregar_icone(self):
        """Carrega o ícone da aplicação"""
        try:
            icon_path = resource_path(WindowConfig.ICON_PATH)
            self.root.iconbitmap(icon_path)
        except Exception as e:
            ErrorHandler.handle_icon_error(e)
    
    def _configurar_interface(self):
        """Configura os componentes da interface gráfica"""
        self._criar_label_nome_imagem()
        self._criar_frame_imagem()
        self._criar_frame_botoes()
        self._criar_label_status()
    
    def _criar_label_nome_imagem(self):
        """Cria o label para o nome da imagem"""
        self.label_nome_imagem = UIHelpers.create_styled_label(
            self.root, bg_color=Colors.IMAGE_LABEL_BACKGROUND,
            fg_color=Colors.IMAGE_LABEL_FOREGROUND, font=Fonts.IMAGE_NAME,
            pady=Padding.TOP_LABEL
        )
        self.label_nome_imagem.pack(side=tk.TOP, fill=tk.X, padx=0, pady=(Padding.TOP_LABEL, 0))
    
    def _criar_frame_imagem(self):
        """Cria o frame para exibição da imagem"""
        self.frame_imagem = UIHelpers.create_styled_frame(self.root)
        self.frame_imagem.pack(fill=tk.BOTH, expand=True, padx=Padding.MAIN, pady=(0, Padding.TOP_LABEL))
        
        self.label_imagem = UIHelpers.create_styled_label(self.frame_imagem)
        self.label_imagem.pack(fill=tk.BOTH, expand=True)
    
    def _criar_frame_botoes(self):
        """Cria o frame para os botões"""
        self.frame_botoes = UIHelpers.create_styled_frame(self.root)
        self.frame_botoes.pack(fill=tk.X, padx=Padding.MAIN, pady=(0, 25))
        self._configurar_todos_botoes()
    
    def _get_button_configs(self):
        """Retorna configuração centralizada de todos os botões"""
        return [
            {
                'name': 'botao_voltar',
                'text': "⟵ Voltar\n[Backspace]",
                'command': self.voltar_imagem,
                'state': tk.DISABLED,
                'expand': True
            },
            {
                'name': 'botao_selecionar',
                'text': "Selecionar Pasta",
                'command': self.selecionar_pasta,
                'width': ButtonConfig.WIDTH_SELECT,
                'expand': True
            },
            {
                'name': 'botao_abrir_pasta',
                'text': "Abrir Pasta",
                'command': self.abrir_pasta,
                'expand': True
            },
            {
                'name': 'botao_certo',
                'text': "✔ Certo\n[Enter/→]",
                'command': lambda: self.mover_imagem("certo"),
                'state': tk.DISABLED,
                'bg_color': Colors.BUTTON_CORRECT,
                'fg_color': "white",
                'hover_color': Colors.BUTTON_CORRECT_HOVER,
                'expand': True
            },
            {
                'name': 'botao_errado',
                'text': "✖ Errado\n[Esc/←]",
                'command': lambda: self.mover_imagem("errado"),
                'state': tk.DISABLED,
                'bg_color': Colors.BUTTON_WRONG,
                'fg_color': "white",
                'hover_color': Colors.BUTTON_WRONG_HOVER,
                'expand': True
            },
            {
                'name': 'botao_pular',
                'text': "Pular\n[Espaço]",
                'command': self.pular_imagem,
                'state': tk.DISABLED,
                'expand': True
            },
            {
                'name': 'botao_pular10',
                'text': "Pular 10\n[Shift+Espaço]",
                'command': self.pular_10_imagens,
                'state': tk.DISABLED,
                'expand': True
            }
        ]
    
    def _configurar_todos_botoes(self):
        """Configura todos os botões da interface usando configuração centralizada"""
        button_configs = self._get_button_configs()
        
        for config in button_configs:
            self._criar_botao_generico(config)
    
    def _criar_botao_generico(self, config):
        """Cria um botão genérico baseado na configuração fornecida"""
        # Extrai configurações específicas do botão
        name = config.pop('name')
        expand = config.pop('expand', False)
        
        # Cria o botão com as configurações restantes
        button = UIHelpers.create_styled_button(self.frame_botoes, **config)
        
        # Aplica o pack layout
        button.pack(side=tk.LEFT, padx=Padding.BUTTON, pady=0, expand=expand)
        
        # Armazena referência do botão na instância
        setattr(self, name, button)
    
    def _criar_label_status(self):
        """Cria o label de status"""
        self.label_status = tk.Label(
            self.root, text=Messages.SELECT_FOLDER,
            bd=1, relief=tk.SUNKEN, anchor=tk.W,
            bg=Colors.STATUS_BACKGROUND, fg=Colors.FOREGROUND, font=Fonts.DEFAULT
        )
        self.label_status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def selecionar_pasta(self):
        """Abre diálogo para selecionar pasta e inicializa o gerenciador de imagens"""
        pasta = filedialog.askdirectory(title="Selecionar Pasta com Imagens")
        if not pasta:
            return
            
        if self.image_manager.selecionar_pasta(pasta):
            self.atualizar_botoes(True)
            self.exibir_imagem_atual()
        else:
            ErrorHandler.show_no_images_warning()
    
    def exibir_imagem_atual(self, redimensionar=False):
        """Exibe a imagem atual na interface"""
        if not self._verificar_imagens_disponiveis():
            return
            
        self._atualizar_nome_imagem()
        self._carregar_e_exibir_imagem()
    
    def _verificar_imagens_disponiveis(self):
        """Verifica se há imagens disponíveis"""
        if not self.image_manager.arquivos_imagem:
            self._limpar_interface()
            self.atualizar_status_final()
            self.atualizar_botoes(False)
            return False
        return True
    
    def _atualizar_nome_imagem(self):
        """Atualiza o nome da imagem no label"""
        nome_img = self.image_manager.obter_nome_imagem_atual()
        self.label_nome_imagem.config(text=nome_img)
    
    def _carregar_e_exibir_imagem(self):
        """Carrega e exibe a imagem atual"""
        try:
            max_width = self.frame_imagem.winfo_width() - Padding.IMAGE_FRAME
            max_height = self.frame_imagem.winfo_height() - Padding.IMAGE_FRAME
            
            self.photo = ImageProcessor.carregar_e_redimensionar(
                self.image_manager.imagem_atual_caminho, max_width, max_height
            )
            
            self.label_imagem.config(image=self.photo, bg=Colors.BACKGROUND)
            self.atualizar_status()
        except Exception as e:
            if not ErrorHandler.handle_image_error(e, self.image_manager, self.exibir_imagem_atual):
                self._limpar_interface()
                self.atualizar_status_final()
                self.atualizar_botoes(False)
    
    def _limpar_interface(self):
        """Limpa a interface quando não há mais imagens"""
        self.label_imagem.config(image=None)
        self.label_nome_imagem.config(text="")
    
    def atualizar_status(self):
        """Atualiza a barra de status com informações atuais"""
        stats = self.image_manager.obter_estatisticas()
        indice, total = self.image_manager.obter_indice_atual()
        nome = self.image_manager.obter_nome_imagem_atual()
        
        self.label_status.config(
            text=f"Imagem {indice} de {total}: {nome}   |   Certo: {stats['certo']}   Errado: {stats['errado']}"
        )
    
    def atualizar_status_final(self):
        """Atualiza a barra de status quando todas as imagens foram classificadas"""
        stats = self.image_manager.obter_estatisticas()
        self.label_status.config(
            text=f"{Messages.ALL_CLASSIFIED}   |   Certo: {stats['certo']}   Errado: {stats['errado']}"
        )
    
    def _get_interaction_buttons(self):
        """Retorna lista de botões de interação para controle de estado"""
        return [
            self.botao_certo, self.botao_errado, self.botao_pular,
            self.botao_pular10, self.botao_voltar
        ]
    
    def atualizar_botoes(self, estado):
        """Ativa ou desativa os botões de interação"""
        novo_estado = tk.NORMAL if estado else tk.DISABLED
        
        for botao in self._get_interaction_buttons():
            botao.config(state=novo_estado)
        
        self.botao_abrir_pasta.config(
            state=tk.NORMAL if self.image_manager.pasta_origem else tk.DISABLED
        )
    
    def mover_imagem(self, destino):
        """Move a imagem atual para a pasta especificada (certo/errado)"""
        if self.image_manager.mover_imagem(destino):
            if self.image_manager.arquivos_imagem:
                self.exibir_imagem_atual()
            else:
                self._limpar_interface()
                self.atualizar_status_final()
                self.atualizar_botoes(False)
    
    def pular_imagem(self):
        """Avança para a próxima imagem"""
        if self.image_manager.pular_imagem():
            self.exibir_imagem_atual()
    
    def pular_10_imagens(self):
        """Avança 10 imagens"""
        if self.image_manager.pular_imagem(10):
            self.exibir_imagem_atual()
    
    def voltar_imagem(self):
        """Volta para a imagem anterior"""
        if self.image_manager.voltar_imagem():
            self.exibir_imagem_atual()
    
    def abrir_pasta(self):
        """Abre a pasta selecionada no explorador de arquivos"""
        if self.image_manager.pasta_origem:
            self.image_manager.abrir_pasta_no_explorador()
        else:
            ErrorHandler.show_no_folder_warning()
