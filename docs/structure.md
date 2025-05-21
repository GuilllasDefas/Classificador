# Estrutura do Projeto

## Visão Geral

O Classificador de Imagens é organizado em uma estrutura modular que separa claramente as responsabilidades do código, seguindo princípios de design de software como Separação de Responsabilidades e Modelo-Visão-Controlador (de forma adaptada).

## Árvore de Diretórios

```
e:\Py_Projetos\Classificador\
├── main.py                 # Arquivo principal do aplicativo
├── models\                 # Gerenciamento de dados e lógica de negócios
│   ├── __init__.py
│   └── image_manager.py    # Gerenciamento de imagens e arquivos
├── views\                  # Interface de usuário
│   ├── __init__.py
│   └── main_window.py      # Janela principal e componentes de UI
├── utils\                  # Utilitários e funções auxiliares
│   ├── __init__.py
│   └── image_utils.py      # Processamento de imagens
└── docs\                   # Documentação do projeto
    ├── index.md            # Página inicial da documentação
    ├── user_guide.md       # Guia do usuário
    ├── technical_reference.md  # Documentação técnica
    ├── installation.md     # Guia de instalação
    └── structure.md        # Este documento
```

## Descrição dos Componentes

### Componentes Principais

#### `main.py`

O ponto de entrada do aplicativo. Inicializa a GUI e gerencia a execução principal.

#### Diretório `models/`

Contém a lógica de negócios e o gerenciamento de dados.

- `image_manager.py`: Implementa a classe `ImageManager` que gerencia as operações de arquivo, incluindo:
  - Carregar imagens da pasta selecionada
  - Mover imagens para as pastas de classificação
  - Calcular estatísticas
  - Navegar pela coleção de imagens

#### Diretório `views/`

Contém os componentes da interface gráfica.

- `main_window.py`: Implementa a classe `MainWindow` que cria e gerencia a interface de usuário, incluindo:
  - Configuração da janela principal
  - Criação de componentes de UI (botões, labels, etc.)
  - Tratamento de eventos de UI
  - Exibição de imagens e atualização de status

#### Diretório `utils/`

Contém funções utilitárias e auxiliares.

- `image_utils.py`: Implementa a classe `ImageProcessor` com métodos para:
  - Carregar imagens
  - Redimensionar imagens mantendo a proporção
  - Processar imagens para exibição

## Fluxo de Dados

1. O usuário seleciona uma pasta através da interface (`MainWindow`)
2. A pasta é passada para o `ImageManager` para carregar as imagens
3. O `ImageManager` lista todas as imagens na pasta e atualiza seu estado interno
4. A `MainWindow` solicita a imagem atual do `ImageManager`
5. O `ImageProcessor` é usado para carregar e redimensionar a imagem para exibição
6. Quando o usuário classifica uma imagem, a `MainWindow` instrui o `ImageManager` a mover o arquivo
7. A interface é atualizada para mostrar a próxima imagem ou o status final

## Benefícios da Estrutura

1. **Modularidade**: Cada componente tem uma responsabilidade clara
2. **Manutenção Facilitada**: Alterações em um módulo não afetam diretamente outros
3. **Testabilidade**: Componentes podem ser testados isoladamente
4. **Extensibilidade**: Novos recursos podem ser adicionados com modificações mínimas
5. **Reutilização**: Componentes podem ser reutilizados em outros projetos

## Diretrizes para Contribuição

Ao contribuir com código para este projeto:

1. Respeite a estrutura de diretórios existente
2. Adicione novos recursos em módulos apropriados
3. Mantenha a separação de responsabilidades
4. Atualize a documentação conforme necessário
5. Siga o estilo de codificação existente
