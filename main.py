import tkinter as tk
import sys
import os

# Adiciona o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow
from utils.updater import AutoUpdater

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
    
    # Verificação simples de atualização após 2 segundos
    def verificar_update():
        try:
            AutoUpdater().verificar_e_atualizar()
        except:
            pass
    
    root.after(2000, verificar_update)
    root.mainloop()

if __name__ == "__main__":
    main()
