import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

from models.image_manager import ImageManager
from utils.image_utils import ImageProcessor

def resource_path(relative_path):
    """Obter caminho absoluto para recurso, funciona para dev e para PyInstaller"""
    try:
        # PyInstaller cria uma pasta temp e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class MainWindow:
    """Classe principal da interface gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Classificador de Imagens")
        self.root.geometry("1600x900")
        
        # Carregar ícone com tratamento de erro
        try:
            icon_path = resource_path("assets/icon.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Não foi possível carregar o ícone: {e}")
        
        # Cores e estilo
        self.bg_color = "#23272e"
        self.fg_color = "#f0f0f0"
        self.button_certo_color = "#2ecc40"
        self.button_errado_color = "#e74c3c"
        self.button_hover = "#555"
        self.status_bg = "#181a1b"
        self.label_img_bg = "#181a1b"
        self.label_img_fg = "#ffd700"
        
        # Inicializa o gerenciador de imagens
        self.image_manager = ImageManager()
        
        # Configurar a interface
        self.configurar_interface()
        
        # Atalhos de teclado
        self.configurar_atalhos()
    
    def configurar_interface(self):
        """Configura os componentes da interface gráfica"""
        # Label do nome da imagem acima da imagem
        self.label_nome_imagem = tk.Label(
            self.root, text="", font=("Arial", 16, "bold"),
            bg=self.label_img_bg, fg=self.label_img_fg, pady=10
        )
        self.label_nome_imagem.pack(side=tk.TOP, fill=tk.X, padx=0, pady=(10, 0))

        # Frame para exibição da imagem
        self.frame_imagem = tk.Frame(self.root, bg=self.bg_color)
        self.frame_imagem.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 10))

        # Label para exibir a imagem
        self.label_imagem = tk.Label(self.frame_imagem, bg=self.bg_color)
        self.label_imagem.pack(fill=tk.BOTH, expand=True)

        # Frame para botões centralizados abaixo da imagem
        self.frame_botoes = tk.Frame(self.root, bg=self.bg_color)
        self.frame_botoes.pack(fill=tk.X, padx=30, pady=(0, 25))

        # Configurar botões
        self.configurar_botoes()

        # Label de status
        self.label_status = tk.Label(
            self.root, text="Selecione uma pasta para começar a classificar imagens",
            bd=1, relief=tk.SUNKEN, anchor=tk.W,
            bg=self.status_bg, fg=self.fg_color, font=("Arial", 12)
        )
        self.label_status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def configurar_botoes(self):
        """Configura os botões da interface"""
        # Botão Voltar
        self.botao_voltar = tk.Button(
            self.frame_botoes, text="⟵ Voltar\n[Backspace]", bg="#444", fg=self.fg_color,
            command=self.voltar_imagem, state=tk.DISABLED,
            activebackground=self.button_hover, activeforeground=self.fg_color,
            font=("Arial", 14, "bold"), height=2, width=12, relief=tk.RAISED, bd=2
        )
        self.botao_voltar.pack(side=tk.LEFT, padx=12, pady=0, expand=True)

        # Botão de selecionar pasta
        self.botao_selecionar = tk.Button(
            self.frame_botoes, text="Selecionar Pasta", command=self.selecionar_pasta,
            bg=self.bg_color, fg=self.fg_color, activebackground=self.button_hover, activeforeground=self.fg_color,
            font=("Arial", 14, "bold"), height=2, width=16, relief=tk.RAISED, bd=2
        )
        self.botao_selecionar.pack(side=tk.LEFT, padx=12, pady=0, expand=True)
        
        # Botão para abrir a pasta no explorador
        self.botao_abrir_pasta = tk.Button(
            self.frame_botoes, text="Abrir Pasta", command=self.abrir_pasta,
            bg="#444", fg=self.fg_color, activebackground=self.button_hover, activeforeground=self.fg_color,
            font=("Arial", 14, "bold"), height=2, width=12, relief=tk.RAISED, bd=2
        )
        self.botao_abrir_pasta.pack(side=tk.LEFT, padx=12, pady=0, expand=True)

        # Botão Certo
        self.botao_certo = tk.Button(
            self.frame_botoes, text="✔ Certo\n[Enter/→]", bg=self.button_certo_color, fg="white",
            command=lambda: self.mover_imagem("certo"), state=tk.DISABLED,
            activebackground="#27ae60", activeforeground="white",
            font=("Arial", 14, "bold"), height=2, width=12, relief=tk.RAISED, bd=2
        )
        self.botao_certo.pack(side=tk.LEFT, padx=12, pady=0, expand=True)

        # Botão Errado
        self.botao_errado = tk.Button(
            self.frame_botoes, text="✖ Errado\n[Esc/←]", bg=self.button_errado_color, fg="white",
            command=lambda: self.mover_imagem("errado"), state=tk.DISABLED,
            activebackground="#c0392b", activeforeground="white",
            font=("Arial", 14, "bold"), height=2, width=12, relief=tk.RAISED, bd=2
        )
        self.botao_errado.pack(side=tk.LEFT, padx=12, pady=0, expand=True)

        # Botão Pular
        self.botao_pular = tk.Button(
            self.frame_botoes, text="Pular\n[Espaço]", bg="#444", fg=self.fg_color,
            command=self.pular_imagem, state=tk.DISABLED,
            activebackground=self.button_hover, activeforeground=self.fg_color,
            font=("Arial", 14, "bold"), height=2, width=12, relief=tk.RAISED, bd=2
        )
        self.botao_pular.pack(side=tk.LEFT, padx=12, pady=0, expand=True)

        # Botão Pular 10
        self.botao_pular10 = tk.Button(
            self.frame_botoes, text="Pular 10\n[Shift+Espaço]", bg="#444", fg=self.fg_color,
            command=self.pular_10_imagens, state=tk.DISABLED,
            activebackground=self.button_hover, activeforeground=self.fg_color,
            font=("Arial", 14, "bold"), height=2, width=12, relief=tk.RAISED, bd=2
        )
        self.botao_pular10.pack(side=tk.LEFT, padx=12, pady=0, expand=True)
    
    def configurar_atalhos(self):
        """Configura os atalhos de teclado"""
        self.root.bind('<Right>', lambda event: self.mover_imagem("certo") if self.botao_certo['state'] == tk.NORMAL else None)
        self.root.bind('<Return>', lambda event: self.mover_imagem("certo") if self.botao_certo['state'] == tk.NORMAL else None)
        self.root.bind('<Left>', lambda event: self.mover_imagem("errado") if self.botao_errado['state'] == tk.NORMAL else None)
        self.root.bind('<Escape>', lambda event: self.mover_imagem("errado") if self.botao_errado['state'] == tk.NORMAL else None)
        self.root.bind('<space>', lambda event: self.pular_imagem() if self.botao_pular['state'] == tk.NORMAL else None)
        self.root.bind('<Shift-space>', lambda event: self.pular_10_imagens() if self.botao_pular10['state'] == tk.NORMAL else None)
        self.root.bind('<BackSpace>', lambda event: self.voltar_imagem() if self.botao_voltar['state'] == tk.NORMAL else None)
        self.frame_imagem.bind('<Configure>', lambda event: self.exibir_imagem_atual(redimensionar=True))
    
    def selecionar_pasta(self):
        """Abre diálogo para selecionar pasta e inicializa o gerenciador de imagens"""
        pasta = filedialog.askdirectory(title="Selecionar Pasta com Imagens")
        if not pasta:
            return
            
        if self.image_manager.selecionar_pasta(pasta):
            self.atualizar_botoes(True)
            self.exibir_imagem_atual()
        else:
            messagebox.showinfo("Sem Imagens", "Nenhuma imagem encontrada na pasta selecionada.")
    
    def exibir_imagem_atual(self, redimensionar=False):
        """Exibe a imagem atual na interface"""
        if not self.image_manager.arquivos_imagem:
            self.label_imagem.config(image=None)
            self.label_nome_imagem.config(text="")
            self.atualizar_status_final()
            self.atualizar_botoes(False)
            return
            
        # Exibir nome da imagem acima da imagem
        nome_img = self.image_manager.obter_nome_imagem_atual()
        self.label_nome_imagem.config(text=nome_img)
        
        # Exibir imagem atual
        try:
            max_width = self.frame_imagem.winfo_width() - 20
            max_height = self.frame_imagem.winfo_height() - 20
            
            self.photo = ImageProcessor.carregar_e_redimensionar(
                self.image_manager.imagem_atual_caminho, 
                max_width, 
                max_height
            )
            
            self.label_imagem.config(image=self.photo, bg=self.bg_color)
            self.atualizar_status()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {str(e)}")
            # Remove a imagem com problema
            self.image_manager.arquivos_imagem.pop(self.image_manager.indice_atual)
            if self.image_manager.arquivos_imagem:
                if self.image_manager.indice_atual >= len(self.image_manager.arquivos_imagem):
                    self.image_manager.indice_atual = 0
                self.image_manager.atualizar_imagem_atual()
                self.exibir_imagem_atual()
            else:
                self.label_imagem.config(image=None)
                self.label_nome_imagem.config(text="")
                self.atualizar_status_final()
                self.atualizar_botoes(False)
    
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
            text=f"Todas as imagens foram classificadas!   |   Certo: {stats['certo']}   Errado: {stats['errado']}"
        )
    
    def atualizar_botoes(self, estado):
        """Ativa ou desativa os botões de interação"""
        novo_estado = tk.NORMAL if estado else tk.DISABLED
        self.botao_certo.config(state=novo_estado)
        self.botao_errado.config(state=novo_estado)
        self.botao_pular.config(state=novo_estado)
        self.botao_pular10.config(state=novo_estado)
        self.botao_voltar.config(state=novo_estado)
        
        # O botão de abrir pasta deve estar ativo se houver uma pasta selecionada
        self.botao_abrir_pasta.config(state=tk.NORMAL if self.image_manager.pasta_origem else tk.DISABLED)
    
    def mover_imagem(self, destino):
        """Move a imagem atual para a pasta especificada (certo/errado)"""
        if self.image_manager.mover_imagem(destino):
            if self.image_manager.arquivos_imagem:
                self.exibir_imagem_atual()
            else:
                self.label_imagem.config(image=None)
                self.label_nome_imagem.config(text="")
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
            messagebox.showinfo("Aviso", "Nenhuma pasta foi selecionada ainda.")
