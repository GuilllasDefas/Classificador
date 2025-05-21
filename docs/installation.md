# Guia de Instalação

## Requisitos do Sistema

- Python 3.6 ou superior
- Sistema operacional: Windows, macOS ou Linux

## Dependências

O aplicativo depende dos seguintes pacotes Python:

- Pillow (PIL)

## Instalação

### 1. Clone ou baixe o repositório

```bash
git clone [https://github.com/GuilllasDefas/Classificador]
cd Classificador
```

Ou baixe e extraia o arquivo ZIP do projeto.

### 2. Instale as dependências

```bash
pip install Pillow
```

### 3. Verifique se o Tkinter está instalado

Para verificar se o Tkinter está instalado corretamente, execute no terminal:

```python
python -c "import tkinter; print(tkinter.TkVersion)"
```

Se você receber um número de versão, o Tkinter está instalado corretamente.

## Instalação em Sistemas Específicos

### Windows

Normalmente, o Python para Windows já vem com Tkinter. Para verificar, abra o Prompt de Comando e execute:

```bash
python -c "import tkinter"
```

Se não houver erros, o Tkinter está instalado. Caso contrário, considere reinstalar o Python.

### macOS

Se você instalou o Python via Homebrew:

```bash
brew install python-tk
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install python3-pil.imagetk
```

### Linux (Fedora)

```bash
sudo dnf install python3-pillow
```

## Executando o Aplicativo

Após a instalação, você pode executar o aplicativo navegando até a pasta do projeto e executando:

```bash
python main.py
```

## Resolução de Problemas

### Erro "No module named 'PIL'"

Este erro indica que o pacote Pillow não está instalado. Instale-o usando:

```bash
pip install Pillow
```

### Erro "No module named '_tkinter'"

Este erro indica que o Tkinter não está instalado corretamente. Consulte as instruções específicas do seu sistema operacional acima.

### Erro "Não foi possível abrir a imagem"

Certifique-se de que os formatos de imagem que você está tentando classificar são suportados (PNG, JPG, JPEG, BMP, GIF).

### Outros Erros

Se encontrar outros erros, verifique:
- Se você está usando uma versão compatível do Python
- Se todas as dependências estão instaladas corretamente
- Se o caminho do arquivo contém caracteres especiais ou não-ASCII

Se os problemas persistirem, consulte a documentação do Python e das bibliotecas específicas ou abra uma issue no repositório do projeto.
