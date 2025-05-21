from PIL import Image, ImageTk

class ImageProcessor:
    """Classe utilitária para processamento de imagens"""
    
    @staticmethod
    def carregar_e_redimensionar(caminho_imagem, max_width, max_height):
        """Carrega e redimensiona uma imagem para os limites especificados"""
        try:
            img = Image.open(caminho_imagem)
            img = ImageProcessor.redimensionar_imagem(img, max_width, max_height)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            raise Exception(f"Erro ao processar a imagem: {str(e)}")
    
    @staticmethod
    def redimensionar_imagem(img, max_width, max_height):
        """Redimensiona uma imagem preservando a proporção"""
        width, height = img.size
        
        if max_width <= 0:
            max_width = 700
        if max_height <= 0:
            max_height = 500
            
        aspect_ratio = width / height
        
        if width > max_width:
            width = max_width
            height = int(width / aspect_ratio)
            
        if height > max_height:
            height = max_height
            width = int(height * aspect_ratio)
            
        try:
            return img.resize((width, height), Image.LANCZOS)
        except AttributeError:
            try:
                return img.resize((width, height), Image.ANTIALIAS)
            except AttributeError:
                return img.resize((width, height))
