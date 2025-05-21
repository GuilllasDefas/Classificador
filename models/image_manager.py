import os
import shutil
from tkinter import messagebox
import subprocess
import platform

class ImageManager:
    """Classe responsável pelo gerenciamento de imagens e operações com arquivos"""
    
    def __init__(self):
        self.pasta_origem = ""
        self.arquivos_imagem = []
        self.indice_atual = 0
        self.imagem_atual_caminho = None
    
    def selecionar_pasta(self, pasta):
        """Seleciona a pasta contendo as imagens e configura as pastas de destino"""
        # Normalizar o caminho para evitar mistura de / e \
        pasta = os.path.normpath(pasta)
        self.pasta_origem = pasta
        
        # Criar diretórios de classificação se não existirem
        self.pasta_certo = os.path.join(pasta, 'certo')
        self.pasta_errado = os.path.join(pasta, 'errado')
        
        try:
            # Verificar se o diretório pai realmente existe
            if not os.path.exists(pasta):
                raise FileNotFoundError(f"O diretório selecionado não existe: {pasta}")
            
            # Criar diretórios com verificação de existência
            if not os.path.exists(self.pasta_certo):
                os.makedirs(self.pasta_certo, exist_ok=True)
            
            if not os.path.exists(self.pasta_errado):
                os.makedirs(self.pasta_errado, exist_ok=True)
                
            # Carregar os arquivos de imagem da pasta
            self.carregar_imagens()
            return len(self.arquivos_imagem) > 0
            
        except Exception as e:
            print(f"Erro ao configurar pastas: {e}")
            messagebox.showerror("Erro", f"Não foi possível configurar as pastas: {str(e)}")
            return False
    
    def carregar_imagens(self):
        """Carrega as imagens da pasta selecionada"""
        self.arquivos_imagem = [
            f for f in os.listdir(self.pasta_origem)
            if os.path.isfile(os.path.join(self.pasta_origem, f)) and
            f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]
        self.indice_atual = 0
        if self.arquivos_imagem:
            self.atualizar_imagem_atual()
    
    def atualizar_imagem_atual(self):
        """Atualiza o caminho da imagem atual"""
        if self.arquivos_imagem:
            self.imagem_atual_caminho = os.path.join(
                self.pasta_origem, 
                self.arquivos_imagem[self.indice_atual]
            )
        else:
            self.imagem_atual_caminho = None
    
    def mover_imagem(self, destino):
        """Move a imagem atual para a pasta de destino especificada"""
        if not self.imagem_atual_caminho:
            return False
            
        pasta_destino = os.path.join(self.pasta_origem, destino)
        nome_arquivo = os.path.basename(self.imagem_atual_caminho)
        caminho_destino = os.path.join(pasta_destino, nome_arquivo)
        
        try:
            shutil.move(self.imagem_atual_caminho, caminho_destino)
            self.arquivos_imagem.pop(self.indice_atual)
            
            if self.arquivos_imagem:
                if self.indice_atual >= len(self.arquivos_imagem):
                    self.indice_atual = 0
                self.atualizar_imagem_atual()
            
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao mover o arquivo: {str(e)}")
            return False
    
    def pular_imagem(self, qtd=1):
        """Avança para a próxima imagem"""
        if not self.arquivos_imagem:
            return False
            
        self.indice_atual += qtd
        if self.indice_atual >= len(self.arquivos_imagem):
            self.indice_atual = self.indice_atual % len(self.arquivos_imagem)
            
        self.atualizar_imagem_atual()
        return True
    
    def voltar_imagem(self):
        """Volta para a imagem anterior"""
        if not self.arquivos_imagem:
            return False
            
        self.indice_atual -= 1
        if self.indice_atual < 0:
            self.indice_atual = len(self.arquivos_imagem) - 1
            
        self.atualizar_imagem_atual()
        return True
    
    def obter_estatisticas(self):
        """Retorna estatísticas sobre as imagens classificadas"""
        if not self.pasta_origem:
            return {"total": 0, "certo": 0, "errado": 0, "restantes": 0}
            
        n_certo = len([
            f for f in os.listdir(os.path.join(self.pasta_origem, "certo")) 
            if os.path.isfile(os.path.join(self.pasta_origem, "certo", f))
        ])
        
        n_errado = len([
            f for f in os.listdir(os.path.join(self.pasta_origem, "errado")) 
            if os.path.isfile(os.path.join(self.pasta_origem, "errado", f))
        ])
        
        return {
            "total": n_certo + n_errado + len(self.arquivos_imagem),
            "certo": n_certo,
            "errado": n_errado,
            "restantes": len(self.arquivos_imagem)
        }
    
    def obter_nome_imagem_atual(self):
        """Retorna o nome da imagem atual"""
        if not self.arquivos_imagem:
            return ""
        return self.arquivos_imagem[self.indice_atual]
    
    def obter_indice_atual(self):
        """Retorna o índice atual e o total de imagens"""
        if not self.arquivos_imagem:
            return 0, 0
        return self.indice_atual + 1, len(self.arquivos_imagem)
    
    def abrir_pasta_no_explorador(self):
        """Abre a pasta atual no explorador de arquivos do sistema"""
        if not self.pasta_origem:
            return False
            
        try:
            system = platform.system().lower()
            
            if system == 'windows':
                os.startfile(self.pasta_origem)
            elif system == 'darwin':  # macOS
                subprocess.call(['open', self.pasta_origem])
            else:  # Linux ou outros sistemas Unix-like
                subprocess.call(['xdg-open', self.pasta_origem])
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta: {str(e)}")
            return False
