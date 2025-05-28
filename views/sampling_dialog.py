import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys

from utils.app_constants import Colors, Fonts, WindowConfig
from utils.ui_helpers import UIHelpers
from utils.sampling_utils import ImageSampler

# Importa a função resource_path da main_window para consistência
def resource_path(relative_path):
    """Obter caminho absoluto para recurso, funciona para dev e para PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SamplingDialog:
    """Diálogo para configuração e execução de amostragem de imagens"""
    
    def __init__(self, parent):
        self.parent = parent
        self.source_folder = ""
        self.destination_folder = ""
        
        self.create_dialog()
    
    def create_dialog(self):
        """Cria a janela de diálogo"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Amostragem de Imagens para Auditoria")
        self.dialog.geometry("600x650")  # Aumentei a altura para acomodar os botões
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=Colors.DIALOG_BACKGROUND)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Configurar ícone
        try:
            icon_path = resource_path(WindowConfig.ICON_PATH)
            self.dialog.iconbitmap(icon_path)
        except Exception:
            pass  # Ignora erro de ícone
        
        # Centraliza a janela
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets do diálogo"""
        # Frame principal
        main_frame = UIHelpers.create_styled_frame(self.dialog, bg_color=Colors.DIALOG_BACKGROUND)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Configuração de Amostragem",
            font=("Segoe UI", 16, "bold"),
            bg=Colors.DIALOG_BACKGROUND,
            fg=Colors.FOREGROUND
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para seleção de pasta origem
        source_frame = UIHelpers.create_styled_frame(main_frame, bg_color=Colors.DIALOG_FRAME)
        source_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            source_frame, 
            text="Pasta de Origem:",
            font=Fonts.DEFAULT,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.source_path_var = tk.StringVar()
        source_entry = tk.Entry(
            source_frame, 
            textvariable=self.source_path_var,
            width=40,
            bg="#1e2227",
            fg=Colors.FOREGROUND,
            relief=tk.FLAT
        )
        source_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        source_button = UIHelpers.create_styled_button(
            source_frame,
            text="Selecionar",
            command=self.select_source_folder,
            width=12,
            bg_color="#17a2b8",  # Azul turquesa
            fg_color="white",
            hover_color="#138496"
        )
        source_button.pack(side=tk.LEFT, padx=10)
        
        # Frame para a pasta de destino
        dest_frame = UIHelpers.create_styled_frame(main_frame, bg_color=Colors.DIALOG_FRAME)
        dest_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            dest_frame, 
            text="Pasta de Destino:",
            font=Fonts.DEFAULT,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.dest_path_var = tk.StringVar()
        dest_entry = tk.Entry(
            dest_frame, 
            textvariable=self.dest_path_var,
            width=40,
            bg="#1e2227",
            fg=Colors.FOREGROUND,
            relief=tk.FLAT
        )
        dest_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        dest_button = UIHelpers.create_styled_button(
            dest_frame,
            text="Selecionar",
            command=self.select_destination_folder,
            width=12,
            bg_color="#17a2b8",  # Azul turquesa 
            fg_color="white",
            hover_color="#138496"
        )
        dest_button.pack(side=tk.LEFT, padx=10)
        
        # Frame para as informações de amostragem
        info_frame = UIHelpers.create_styled_frame(main_frame, bg_color=Colors.DIALOG_FRAME)
        info_frame.pack(fill=tk.X, pady=10)
        
        # Informações de contagem
        self.info_label = tk.Label(
            info_frame,
            text="Selecione uma pasta para contar as imagens.",
            font=Fonts.DEFAULT,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND
        )
        self.info_label.pack(pady=10)
        
        # Frame para configuração de amostragem
        sample_frame = UIHelpers.create_styled_frame(main_frame, bg_color=Colors.DIALOG_FRAME)
        sample_frame.pack(fill=tk.X, pady=10)
        
        # Modo de amostragem
        sampling_mode_frame = UIHelpers.create_styled_frame(sample_frame, bg_color=Colors.DIALOG_FRAME)
        sampling_mode_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            sampling_mode_frame,
            text="Modo de Amostragem:",
            font=Fonts.DEFAULT,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND
        ).pack(side=tk.LEFT, padx=10)
        
        self.sampling_mode = tk.StringVar(value="percentage")
        
        percentage_radio = tk.Radiobutton(
            sampling_mode_frame,
            text="Porcentagem",
            variable=self.sampling_mode,
            value="percentage",
            command=self.update_sample_frame,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND,
            selectcolor="#2c313a",
            activebackground=Colors.DIALOG_FRAME,
            activeforeground=Colors.FOREGROUND
        )
        percentage_radio.pack(side=tk.LEFT, padx=10)
        
        quantity_radio = tk.Radiobutton(
            sampling_mode_frame,
            text="Quantidade Fixa",
            variable=self.sampling_mode,
            value="quantity",
            command=self.update_sample_frame,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND,
            selectcolor="#2c313a",
            activebackground=Colors.DIALOG_FRAME,
            activeforeground=Colors.FOREGROUND
        )
        quantity_radio.pack(side=tk.LEFT, padx=10)
        
        # Frame para input de amostragem
        self.sample_input_frame = UIHelpers.create_styled_frame(sample_frame, bg_color=Colors.DIALOG_FRAME)
        self.sample_input_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Inicialmente mostra o campo de porcentagem
        self.create_percentage_input()
        
        # Opção para amostragem aleatória
        random_frame = UIHelpers.create_styled_frame(sample_frame, bg_color=Colors.DIALOG_FRAME)
        random_frame.pack(fill=tk.X, pady=5)
        
        self.random_var = tk.BooleanVar(value=True)
        random_check = tk.Checkbutton(
            random_frame,
            text="Amostragem Aleatória",
            variable=self.random_var,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND,
            selectcolor="#2c313a",
            activebackground=Colors.DIALOG_FRAME,
            activeforeground=Colors.FOREGROUND
        )
        random_check.pack(padx=10, pady=5, anchor=tk.W)
        
        # ADIÇÃO DE BOTÕES DE AÇÃO - Adiciona um separador visual
        separator = tk.Frame(main_frame, height=2, bg="#1c1f26")
        separator.pack(fill=tk.X, pady=15)
        
        # Frame para os botões de ação
        button_frame = UIHelpers.create_styled_frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Botão Cancelar
        cancel_button = UIHelpers.create_styled_button(
            button_frame,
            text="Cancelar",
            command=self.dialog.destroy,
            width=12,
            bg_color="#6c757d",  # Cor cinza para botão cancelar
            fg_color="white",
            hover_color="#5a6268"
        )
        cancel_button.pack(side=tk.RIGHT, padx=10)
        
        # Botão Gerar Amostra
        sample_button = UIHelpers.create_styled_button(
            button_frame,
            text="Gerar Amostra",
            command=self.generate_sample,
            width=15,
            bg_color="#28a745",  # Verde para confirmar
            fg_color="white",
            hover_color="#218838"
        )
        sample_button.pack(side=tk.RIGHT, padx=10)
        
        # Botão Contar Imagens
        count_button = UIHelpers.create_styled_button(
            button_frame,
            text="Contar Imagens",
            command=self.count_images,
            width=15,
            bg_color="#17a2b8",  # Azul turquesa
            fg_color="white",
            hover_color="#138496"
        )
        count_button.pack(side=tk.RIGHT, padx=10)
    
    def create_percentage_input(self):
        """Cria o input para porcentagem"""
        for widget in self.sample_input_frame.winfo_children():
            widget.destroy()
            
        tk.Label(
            self.sample_input_frame,
            text="Porcentagem (%):",
            font=Fonts.DEFAULT,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND
        ).pack(side=tk.LEFT, padx=10)
        
        self.percentage_var = tk.StringVar(value="10")
        percentage_entry = tk.Entry(
            self.sample_input_frame,
            textvariable=self.percentage_var,
            width=5,
            bg="#1e2227",
            fg=Colors.FOREGROUND,
            relief=tk.FLAT
        )
        percentage_entry.pack(side=tk.LEFT, padx=5)
    
    def create_quantity_input(self):
        """Cria o input para quantidade fixa"""
        for widget in self.sample_input_frame.winfo_children():
            widget.destroy()
            
        tk.Label(
            self.sample_input_frame,
            text="Quantidade de Imagens:",
            font=Fonts.DEFAULT,
            bg=Colors.DIALOG_FRAME,
            fg=Colors.FOREGROUND
        ).pack(side=tk.LEFT, padx=10)
        
        self.quantity_var = tk.StringVar(value="10")
        quantity_entry = tk.Entry(
            self.sample_input_frame,
            textvariable=self.quantity_var,
            width=5,
            bg="#1e2227",
            fg=Colors.FOREGROUND,
            relief=tk.FLAT
        )
        quantity_entry.pack(side=tk.LEFT, padx=5)
    
    def update_sample_frame(self):
        """Atualiza o frame de acordo com o modo de amostragem selecionado"""
        mode = self.sampling_mode.get()
        if mode == "percentage":
            self.create_percentage_input()
        else:
            self.create_quantity_input()
    
    def select_source_folder(self):
        """Abre diálogo para selecionar pasta de origem"""
        folder = filedialog.askdirectory(title="Selecionar Pasta de Origem das Imagens")
        if folder:
            self.source_folder = folder
            self.source_path_var.set(folder)
            self.count_images()
    
    def select_destination_folder(self):
        """Abre diálogo para selecionar pasta de destino"""
        folder = filedialog.askdirectory(title="Selecionar Pasta de Destino para Amostragem")
        if folder:
            self.destination_folder = folder
            self.dest_path_var.set(folder)
    
    def count_images(self):
        """Conta as imagens na pasta selecionada"""
        if not self.source_folder:
            messagebox.showwarning("Atenção", "Selecione uma pasta de origem primeiro.")
            return
            
        try:
            sampler = ImageSampler(self.source_folder)
            count = sampler.count_images()
            
            if count == 0:
                self.info_label.config(text="Nenhuma imagem encontrada na pasta selecionada.")
            else:
                self.info_label.config(text=f"Total de imagens encontradas: {count}")
                
                # Atualiza o valor padrão para quantidade fixa
                if hasattr(self, 'quantity_var'):
                    suggested_quantity = min(10, count)
                    self.quantity_var.set(str(suggested_quantity))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao contar imagens: {str(e)}")
    
    def generate_sample(self):
        """Gera a amostragem baseada nos parâmetros fornecidos"""
        if not self.source_folder:
            messagebox.showwarning("Atenção", "Selecione uma pasta de origem primeiro.")
            return
            
        if not self.destination_folder:
            messagebox.showwarning("Atenção", "Selecione uma pasta de destino primeiro.")
            return
        
        # Obter parâmetros de amostragem
        try:
            sampling_mode = self.sampling_mode.get()
            use_random = self.random_var.get()
            
            if sampling_mode == "percentage":
                try:
                    percentage = float(self.percentage_var.get())
                    if percentage <= 0 or percentage > 100:
                        raise ValueError("A porcentagem deve estar entre 0 e 100.")
                except ValueError:
                    messagebox.showwarning("Valor Inválido", "Informe uma porcentagem válida entre 0 e 100.")
                    return
                    
                sample_param = percentage
            else:  # quantity
                try:
                    quantity = int(self.quantity_var.get())
                    if quantity <= 0:
                        raise ValueError("A quantidade deve ser maior que zero.")
                except ValueError:
                    messagebox.showwarning("Valor Inválido", "Informe uma quantidade válida maior que zero.")
                    return
                    
                sample_param = quantity
            
            # Executar amostragem
            sampler = ImageSampler(self.source_folder)
            result = sampler.generate_sample(
                self.destination_folder, 
                sample_param, 
                sampling_mode,
                use_random
            )
            
            if result['success']:
                messagebox.showinfo(
                    "Sucesso", 
                    f"Amostragem concluída com sucesso!\n\n"
                    f"{result['copied']} imagens foram copiadas para:\n"
                    f"{self.destination_folder}"
                )
                self.dialog.destroy()
            else:
                messagebox.showerror("Erro", f"Erro ao gerar amostragem: {result['message']}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar amostragem: {str(e)}")