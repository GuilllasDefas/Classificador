import requests
import os
import zipfile
import subprocess
import sys
import tempfile
from tkinter import messagebox

class AutoUpdater:
    def __init__(self):
        self.repo = "GuilllasDefas/Classificador"
        
    def verificar_e_atualizar(self):
        """Verifica e atualiza se necessário"""
        try:
            # Pega a última release
            url = f"https://api.github.com/repos/{self.repo}/releases/latest"
            response = requests.get(url, timeout=5)
            
            if response.status_code != 200:
                return
                
            release = response.json()
            
            # Pergunta se quer atualizar
            if messagebox.askyesno("Atualização", "Nova versão disponível! Atualizar agora?"):
                self._baixar_e_instalar(release)
                
        except:
            pass  # Falha silenciosa
    
    def _baixar_e_instalar(self, release):
        """Baixa e instala"""
        try:
            # Pega o arquivo ZIP
            download_url = release['assets'][0]['browser_download_url']
            
            # Baixa
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "update.zip")
            
            response = requests.get(download_url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extrai
            extract_dir = os.path.join(temp_dir, "app")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Cria script de update
            script = f'''
import time, shutil, os, subprocess
time.sleep(2)
shutil.rmtree(r"{os.path.dirname(sys.executable)}", ignore_errors=True)
shutil.copytree(r"{extract_dir}", r"{os.path.dirname(sys.executable)}")
subprocess.Popen([r"{sys.executable}"])
'''
            script_path = os.path.join(temp_dir, "update.py")
            with open(script_path, 'w') as f:
                f.write(script)
            
            subprocess.Popen([sys.executable, script_path])
            sys.exit(0)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na atualização: {e}")