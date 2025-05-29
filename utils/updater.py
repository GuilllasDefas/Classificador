import requests
import os
import zipfile
import subprocess
import sys
import tempfile
import shutil
import threading
from tkinter import messagebox
from packaging import version
import json

class AutoUpdater:
    def __init__(self, modo_teste=False):
        # Configurações do seu repositório GitHub
        self.repo_owner = "GuilllasDefas"
        self.repo_name = "Classificador"
        self.debug = True  # ← Ativar/desativar debug
        self.modo_teste = modo_teste  # Novo parâmetro para teste
        
        # Obtém a versão atual do arquivo version.json
        self.current_version = self._get_current_version()
    
    def _get_current_version(self):
        """Obtém versão atual do arquivo version.json"""
        try:
            # Determina o diretório base (funciona tanto compilado quanto em desenvolvimento)
            if getattr(sys, 'frozen', False):
                # Quando executado como .exe, o PyInstaller cria um diretório temporário
                # Mas os arquivos de dados ficam junto com o executável
                base_dir = os.path.dirname(sys.executable)
                if self.debug:
                    print(f"DEBUG: Executando como .exe, base_dir: {base_dir}")
            else:
                # Quando executado como script Python
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if self.debug:
                    print(f"DEBUG: Executando como script, base_dir: {base_dir}")
            
            version_file = os.path.join(base_dir, "version.json")
            
            if self.debug:
                print(f"DEBUG: Procurando version.json em: {version_file}")
                print(f"DEBUG: Arquivo existe? {os.path.exists(version_file)}")
                if os.path.exists(base_dir):
                    print(f"DEBUG: Arquivos no diretório base: {os.listdir(base_dir)}")
            
            # Se o arquivo não existir, cria com a versão padrão
            if not os.path.exists(version_file):
                if self.debug:
                    print("DEBUG: version.json não encontrado, criando com versão padrão")
                default_version = {"version": "1.0.0"}
                try:
                    with open(version_file, 'w') as f:
                        json.dump(default_version, f, indent=2)
                    return "1.0.0"
                except:
                    if self.debug:
                        print("DEBUG: Não foi possível criar version.json, usando versão padrão")
                    return "1.0.0"
                
            # Lê a versão do arquivo
            with open(version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                versao = data.get("version", "1.0.0")
                if self.debug:
                    print(f"DEBUG: Versão lida do arquivo: {versao}")
                return versao
                
        except Exception as e:
            if self.debug:
                print(f"DEBUG: Erro ao ler versão: {e}")
            # Retorna versão padrão em caso de erro
            return "1.0.0"
        
    def verificar_atualizacao(self):
        """Verifica se tem atualização disponível"""
        # Se estiver em modo de teste, simula uma atualização
        if self.modo_teste:
            if self.debug:
                print("DEBUG: Usando modo de teste - simulando atualização")
            return True, {
                'tag_name': 'v9.9.9',
                'html_url': 'https://github.com/GuilllasDefas/Classificador/releases/latest',
                'download_url': 'https://github.com/GuilllasDefas/Classificador/releases/latest',
                'body': 'Esta é uma versão de teste simulada para verificar a funcionalidade.'
            }
            
        # Código original para verificação real
        try:
            # Pega informações da última release do GitHub
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                release_info = response.json()
                versao_github = release_info['tag_name']
                
                # Remove 'v' se existir e limpa espaços
                versao_nova = versao_github.replace('v', '').strip()
                versao_atual = self.current_version.strip()
                
                if self.debug:
                    print(f"DEBUG: Versão atual: '{versao_atual}'")
                    print(f"DEBUG: Versão no GitHub: '{versao_github}' -> '{versao_nova}'")
                
                # Encontra a URL de download do ZIP
                for asset in release_info.get('assets', []):
                    if asset['name'].endswith('.exe'):
                        download_url = asset['browser_download_url']
                        if self.debug:
                            print(f"DEBUG: Encontrado arquivo .exe: {asset['name']}")
                        break
                
                # Se não encontrou ZIP específico, usa a URL da release
                if 'download_url' not in release_info:
                    release_info['download_url'] = release_info.get('html_url')
                
                # Compara versões usando packaging
                try:
                    if version.parse(versao_nova) > version.parse(versao_atual):
                        if self.debug:
                            print("DEBUG: Atualização disponível!")
                        return True, release_info
                    else:
                        if self.debug:
                            print("DEBUG: Nenhuma atualização disponível - app está na versão mais recente")
                        return False, None
                except:
                    # Se der erro no parse, faz comparação simples
                    if versao_nova != versao_atual:
                        return True, release_info
                    return False, None
                
            else:
                if self.debug:
                    print(f"DEBUG: Erro HTTP {response.status_code} ao verificar atualizações")
                return False, None
                
        except Exception as e:
            if self.debug:
                print(f"DEBUG: Erro ao verificar atualização: {e}")
            return False, None
    
    def perguntar_se_quer_atualizar(self, release_info):
        """Pergunta se o usuário quer ver a nova versão"""
        versao = release_info['tag_name']
        
        resposta = messagebox.askyesno(
            "Atualização Disponível",
            f"Nova versão {versao} disponível!\n\n"
            f"Deseja acessar a página de download?",
            icon='question'
        )
        
        return resposta