import tkinter as tk
import sys
import os
import threading
import tkinter.messagebox
import webbrowser  # Adicionar esta importação

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
    """Processa a atualização na thread principal mostrando apenas um link clicável"""
    if updater.perguntar_se_quer_atualizar(release_info):
        url = release_info.get('download_url', release_info.get('html_url', 'https://github.com/GuilllasDefas/Classificador/releases'))
        
        # Criar janela de diálogo simplificada com link clicável
        dialog = tk.Toplevel()
        dialog.title("Nova versão disponível")
        dialog.geometry("500x120")
        dialog.configure(bg="#23272e")
        dialog.resizable(False, False)
        
        # Adicionar mensagem
        tk.Label(dialog, text="Uma nova versão está disponível!", 
                 bg="#23272e", fg="white", font=("Arial", 12, "bold")).pack(pady=(15, 5))
        
        # Função para abrir o link
        def abrir_link(event=None):
            webbrowser.open_new(url)
            dialog.destroy()
        
        # Adicionar instrução
        tk.Label(dialog, text="Clique no link abaixo para baixar:", 
                 bg="#23272e", fg="white").pack(pady=(0, 5))
        
        # Adicionar link clicável (estilizado como link)
        link_label = tk.Label(dialog, text=url, fg="#3498db", cursor="hand2",
                            bg="#23272e", font=("Arial", 10, "underline"))
        link_label.pack(pady=5)
        link_label.bind("<Button-1>", abrir_link)
        
        # Adicionar botão de fechar (X) no título
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
        
        # Centralizar diálogo
        dialog.transient()
        dialog.focus_set()
        dialog.grab_set()

def testar_atualizacao(root):
    """Função para testar o diálogo de atualização"""
    updater = AutoUpdater(modo_teste=True)
    tem_atualizacao, release_info = updater.verificar_atualizacao()
    
    if tem_atualizacao:
        processar_atualizacao(updater, release_info)

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
    
    # Para testes: Descomente a linha abaixo e comente a verificação normal
    #root.after(1000, lambda: testar_atualizacao(root))
    
    # Verificação normal (deixe comentado ao testar)
    root.after(3000, lambda: verificar_atualizacoes_em_background(root))
    
    root.mainloop()

if __name__ == "__main__":
    main()
