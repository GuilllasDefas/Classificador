import os
import random
import shutil
from pathlib import Path

class ImageSampler:
    """Classe para gerenciar a amostragem de imagens"""
    
    # Extensões de imagens suportadas
    SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    def __init__(self, source_folder):
        """Inicializa o gerenciador de amostragem
        
        Args:
            source_folder (str): Caminho da pasta contendo as imagens
        """
        self.source_folder = source_folder
        self.image_files = []
    
    def _get_image_files(self):
        """Obtém a lista de arquivos de imagem na pasta de origem
        
        Returns:
            list: Lista de caminhos completos para os arquivos de imagem
        """
        if not self.image_files:
            self.image_files = [
                os.path.join(self.source_folder, f) 
                for f in os.listdir(self.source_folder)
                if os.path.isfile(os.path.join(self.source_folder, f)) and 
                   self._is_image_file(f)
            ]
        return self.image_files
    
    def _is_image_file(self, filename):
        """Verifica se um arquivo é uma imagem baseado na extensão
        
        Args:
            filename (str): Nome do arquivo a ser verificado
            
        Returns:
            bool: True se for um arquivo de imagem, False caso contrário
        """
        return filename.lower().endswith(self.SUPPORTED_EXTENSIONS)
    
    def count_images(self):
        """Conta o número de imagens na pasta
        
        Returns:
            int: Número de imagens encontradas
        """
        return len(self._get_image_files())
    
    def _calculate_sample_size(self, param, mode):
        """Calcula o tamanho da amostra baseado no parâmetro e modo
        
        Args:
            param (float|int): Porcentagem ou quantidade fixa
            mode (str): 'percentage' ou 'quantity'
            
        Returns:
            int: Número de imagens a serem amostradas
        """
        total_images = len(self._get_image_files())
        
        if mode == 'percentage':
            return max(1, int(total_images * param / 100))
        else:  # quantity
            return min(param, total_images)
    
    def generate_sample(self, destination_folder, param, mode='percentage', random_sample=True):
        """Gera uma amostra de imagens e copia para a pasta de destino
        
        Args:
            destination_folder (str): Pasta onde as imagens serão copiadas
            param (float|int): Porcentagem ou quantidade fixa de imagens
            mode (str): 'percentage' ou 'quantity'
            random_sample (bool): Se True, seleciona aleatoriamente, senão pega as primeiras
            
        Returns:
            dict: Dicionário com informações sobre o resultado da operação
        """
        try:
            # Verifica se as pastas existem
            if not os.path.exists(self.source_folder):
                return {'success': False, 'message': 'Pasta de origem não existe'}
                
            # Cria a pasta de destino se não existir
            os.makedirs(destination_folder, exist_ok=True)
            
            # Obtém a lista de arquivos
            image_files = self._get_image_files()
            
            if not image_files:
                return {'success': False, 'message': 'Nenhuma imagem encontrada na pasta de origem'}
            
            # Calcula o tamanho da amostra
            sample_size = self._calculate_sample_size(param, mode)
            
            # Seleciona as imagens
            if random_sample:
                selected_files = random.sample(image_files, sample_size)
            else:
                selected_files = image_files[:sample_size]
            
            # Copia as imagens para o destino
            copied_count = 0
            for file_path in selected_files:
                file_name = os.path.basename(file_path)
                dest_path = os.path.join(destination_folder, file_name)
                shutil.copy2(file_path, dest_path)
                copied_count += 1
            
            return {
                'success': True, 
                'copied': copied_count,
                'total': len(image_files),
                'message': f'{copied_count} imagens copiadas com sucesso'
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
