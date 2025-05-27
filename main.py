import tkinter as tk
import sys
import os
import threading

# Adiciona o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow
from utils.updater import AutoUpdater

def verificar_atualizacoes_em_background(root):
    """Verifica atualizações sem travar a interface"""
    def verificar():
        updater = AutoUpdater()
        tem_atualizacao, release_info = updater.verificar_atualizacao()
        
        if tem_atualizacao:
            # Executa na thread principal (UI)
            root.after(0, lambda: processar_atualizacao(updater, release_info))
    
    # Roda em thread separada para não travar
    thread = threading.Thread(target=verificar)
    thread.daemon = True
    thread.start()

def processar_atualizacao(updater, release_info):
    """Processa a atualização na thread principal"""
    if updater.perguntar_se_quer_atualizar(release_info):
        updater.baixar_e_instalar(release_info)

def main():
    """Função principal para iniciar o aplicativo"""
    # Criar diretório de documentação se não existir
    docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print(f"Diretório de documentação criado em: {docs_dir}")
    
    # Iniciar a aplicação
    root = tk.Tk()
    root.configure(bg="#23272e")
    app = MainWindow(root)
    
    # Verifica atualizações 3 segundos após abrir (para não atrasar a abertura)
    root.after(3000, lambda: verificar_atualizacoes_em_background(root))
    
    root.mainloop()

if __name__ == "__main__":
    main()
