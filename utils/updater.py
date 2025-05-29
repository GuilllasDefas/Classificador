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
from config.app_config import APP_VERSION, REPO_OWNER, REPO_NAME

class AutoUpdater:
    def __init__(self, modo_teste=False):
        # Configurações do seu repositório GitHub
        self.repo_owner = REPO_OWNER
        self.repo_name = REPO_NAME
        self.debug = True  # ← Ativar/desativar debug
        self.modo_teste = modo_teste  # Novo parâmetro para teste
        
        # Obtém a versão atual da configuração centralizada
        self.current_version = APP_VERSION
        if self.debug:
            print(f"DEBUG: Versão atual carregada: {self.current_version}")
    
    def verificar_atualizacao(self):
        """Verifica se tem atualização disponível"""
        # Se estiver em modo de teste, simula uma atualização
        if self.modo_teste:
            if self.debug:
                print("DEBUG: Usando modo de teste - simulando atualização")
            return True, {
                'tag_name': 'v9.9.9',
                'html_url': f'https://github.com/{self.repo_owner}/{self.repo_name}/releases/latest',
                'download_url': f'https://github.com/{self.repo_owner}/{self.repo_name}/releases/latest',
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
                
                # Encontra a URL de download - prioriza .exe, depois .zip
                download_url = None
                
                # Primeiro procura por arquivo .exe
                for asset in release_info.get('assets', []):
                    if asset['name'].endswith('.exe'):
                        download_url = asset['browser_download_url']
                        if self.debug:
                            print(f"DEBUG: Encontrado arquivo .exe: {asset['name']}")
                        break
                
                # Se não encontrou .exe, procura por .zip
                if not download_url:
                    for asset in release_info.get('assets', []):
                        if asset['name'].endswith('.zip'):
                            download_url = asset['browser_download_url']
                            if self.debug:
                                print(f"DEBUG: Encontrado arquivo .zip: {asset['name']}")
                            break
                
                # Define a URL de download ou usa a URL da release como fallback
                if download_url:
                    release_info['download_url'] = download_url
                else:
                    release_info['download_url'] = release_info.get('html_url')
                    if self.debug:
                        print("DEBUG: Nenhum arquivo .exe ou .zip encontrado, usando URL da release")
                
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