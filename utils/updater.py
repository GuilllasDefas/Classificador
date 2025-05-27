import requests
import os
import zipfile
import subprocess
import sys
import tempfile
import shutil
import threading
from tkinter import messagebox

class AutoUpdater:
    def __init__(self):
        # Configurações do seu repositório GitHub
        self.repo_owner = "GuilllasDefas"  # Substitua pelo seu usuário
        self.repo_name = "Classificador"     # Substitua pelo nome do repo
        self.current_version = "1.0.0"          # Versão atual do app
        self.debug = True  # ← Ativar/desativar debug
        
    def verificar_atualizacao(self):
        """Verifica se tem atualização disponível"""
        try:
            # Pega informações da última release do GitHub
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                release_info = response.json()
                versao_nova = release_info['tag_name'].replace('v', '')  # Remove 'v' se tiver
                
                if self.debug:  # ← Adicione estas linhas de debug
                    print(f"DEBUG: Versão atual: {self.current_version}")
                    print(f"DEBUG: Versão no GitHub: {versao_nova}")
                
                # Compara versões (simplificado)
                if versao_nova != self.current_version:
                    if self.debug:
                        print("DEBUG: Atualização disponível!")
                    return True, release_info
                else:
                    if self.debug:  # ← Esta é a linha que você queria
                        print("DEBUG: Nenhuma atualização disponível - app está na versão mais recente")
                    return False, None
                    
            else:
                if self.debug:
                    print(f"DEBUG: Erro HTTP {response.status_code} ao verificar atualizações")
                return False, None
                
        except Exception as e:
            if self.debug:
                print(f"DEBUG: Erro ao verificar atualização: {e}")
            else:
                print(f"Erro ao verificar atualização: {e}")  # Esta linha já existia
            return False, None
    
    def perguntar_se_quer_atualizar(self, release_info):
        """Pergunta se o usuário quer atualizar"""
        versao = release_info['tag_name']
        
        resposta = messagebox.askyesno(
            "Atualização Disponível",
            f"Nova versão {versao} disponível!\n\n"
            f"Deseja baixar e instalar agora?",
            icon='question'
        )
        
        return resposta
    
    def baixar_e_instalar(self, release_info):
        """Baixa e instala a atualização"""
        try:
            # Encontra o arquivo ZIP para download
            download_url = None
            for arquivo in release_info['assets']:
                if arquivo['name'].endswith('.zip'):
                    download_url = arquivo['browser_download_url']
                    break
            
            if not download_url:
                messagebox.showerror("Erro", "Arquivo de atualização não encontrado!")
                return False
            
            # Mostra mensagem de download
            messagebox.showinfo("Download", "Baixando atualização...\nO aplicativo será reiniciado automaticamente.")
            
            # Baixa o arquivo
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "update.zip")
            
            response = requests.get(download_url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extrai o arquivo
            extract_dir = os.path.join(temp_dir, "extracted")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Cria script para substituir os arquivos
            self._criar_script_atualizacao(extract_dir)
            
            # Fecha o aplicativo (o script vai reiniciar)
            sys.exit(0)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar atualização: {e}")
            return False
    
    def _criar_script_atualizacao(self, pasta_nova_versao):
        """Cria um script que vai substituir os arquivos"""
        # Descobre onde está o executável atual
        if getattr(sys, 'frozen', False):
            pasta_atual = os.path.dirname(sys.executable)
        else:
            pasta_atual = os.path.dirname(os.path.abspath(__file__))
        
        # Cria script Python temporário
        script_path = os.path.join(tempfile.gettempdir(), "atualizar_app.py")
        
        script_conteudo = f'''
import time
import shutil
import os
import subprocess

# Espera 3 segundos para o app fechar completamente
time.sleep(3)

try:
    pasta_nova = r"{pasta_nova_versao}"
    pasta_app = r"{pasta_atual}"
    
    # Copia todos os arquivos novos
    for item in os.listdir(pasta_nova):
        origem = os.path.join(pasta_nova, item)
        destino = os.path.join(pasta_app, item)
        
        if os.path.isfile(origem):
            shutil.copy2(origem, destino)
        elif os.path.isdir(origem):
            if os.path.exists(destino):
                shutil.rmtree(destino)
            shutil.copytree(origem, destino)
    
    # Reinicia o aplicativo
    exe_path = os.path.join(pasta_app, "Classificador de Imagens.exe")
    if os.path.exists(exe_path):
        subprocess.Popen([exe_path])
        
except Exception as e:
    print(f"Erro na atualização: {{e}}")
'''
        
        # Salva o script
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_conteudo)
        
        # Executa o script
        subprocess.Popen([sys.executable, script_path], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)