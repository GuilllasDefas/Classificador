"""Mixin para gerenciamento de atalhos de teclado"""

import tkinter as tk

class KeyboardMixin:
    """Mixin para adicionar funcionalidades de teclado"""
    
    def configurar_atalhos(self):
        """Configura os atalhos de teclado"""
        # Atalhos de movimento
        self.root.bind('<Right>', self._handle_right_key)
        self.root.bind('<Return>', self._handle_enter_key)
        self.root.bind('<Left>', self._handle_left_key)
        self.root.bind('<Escape>', self._handle_escape_key)
        
        # Atalhos de navegação
        self.root.bind('<space>', self._handle_space_key)
        self.root.bind('<Shift-space>', self._handle_shift_space_key)
        self.root.bind('<BackSpace>', self._handle_backspace_key)
        
        # Redimensionamento
        self.frame_imagem.bind('<Configure>', self._handle_resize)
    
    def _handle_right_key(self, event):
        """Manipula tecla direita (certo)"""
        if self.botao_certo['state'] == tk.NORMAL:
            self.mover_imagem("certo")
    
    def _handle_enter_key(self, event):
        """Manipula tecla Enter (certo)"""
        if self.botao_certo['state'] == tk.NORMAL:
            self.mover_imagem("certo")
    
    def _handle_left_key(self, event):
        """Manipula tecla esquerda (errado)"""
        if self.botao_errado['state'] == tk.NORMAL:
            self.mover_imagem("errado")
    
    def _handle_escape_key(self, event):
        """Manipula tecla Escape (errado)"""
        if self.botao_errado['state'] == tk.NORMAL:
            self.mover_imagem("errado")
    
    def _handle_space_key(self, event):
        """Manipula tecla Espaço (pular)"""
        if self.botao_pular['state'] == tk.NORMAL:
            self.pular_imagem()
    
    def _handle_shift_space_key(self, event):
        """Manipula Shift+Espaço (pular 10)"""
        if self.botao_pular10['state'] == tk.NORMAL:
            self.pular_10_imagens()
    
    def _handle_backspace_key(self, event):
        """Manipula tecla Backspace (voltar)"""
        if self.botao_voltar['state'] == tk.NORMAL:
            self.voltar_imagem()
    
    def _handle_resize(self, event):
        """Manipula redimensionamento da janela"""
        self.exibir_imagem_atual(redimensionar=True)
