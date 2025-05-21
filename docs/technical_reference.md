# Referência Técnica

Esta documentação técnica descreve as principais classes, métodos e estruturas do Classificador de Imagens.

## Arquitetura

O aplicativo segue uma arquitetura modular com separação clara de responsabilidades:

- **Model**: Gerencia os dados e regras de negócio
- **View**: Implementa a interface gráfica
- **Utils**: Fornece funcionalidades auxiliares

## Módulos Principais

### 1. ImageManager (`models/image_manager.py`)

Responsável pelo gerenciamento de arquivos e operações com imagens.

#### Métodos

| Método | Descrição |
|--------|-----------|
| `selecionar_pasta(pasta)` | Define a pasta de origem e cria subpastas |
| `carregar_imagens()` | Carrega a lista de imagens na pasta selecionada |
| `atualizar_imagem_atual()` | Atualiza o caminho da imagem atual |
| `mover_imagem(destino)` | Move a imagem para a pasta de destino (certo/errado) |
| `pular_imagem(qtd=1)` | Avança para a próxima imagem ou para qtd imagens à frente |
| `voltar_imagem()` | Volta para a imagem anterior |
| `obter_estatisticas()` | Retorna dados estatísticos sobre a classificação |
| `obter_nome_imagem_atual()` | Retorna o nome da imagem atual |
| `obter_indice_atual()` | Retorna o índice atual e o total de imagens |
| `abrir_pasta_no_explorador()` | Abre a pasta atual no explorador de arquivos |

### 2. MainWindow (`views/main_window.py`)

Implementa a interface gráfica principal do aplicativo.

#### Métodos

| Método | Descrição |
|--------|-----------|
| `configurar_interface()` | Configura os elementos da interface |
| `configurar_botoes()` | Configura os botões e suas ações |
| `configurar_atalhos()` | Configura os atalhos de teclado |
| `selecionar_pasta()` | Inicia o diálogo de seleção de pasta |
| `exibir_imagem_atual(redimensionar=False)` | Exibe a imagem atual na interface |
| `atualizar_status()` | Atualiza a barra de status com informações |
| `mover_imagem(destino)` | Classifica a imagem e a move para o destino |
| `pular_imagem()` | Avança para a próxima imagem |
| `pular_10_imagens()` | Avança 10 imagens |
| `voltar_imagem()` | Volta para a imagem anterior |
| `abrir_pasta()` | Abre a pasta atual no explorador de arquivos |

### 3. ImageProcessor (`utils/image_utils.py`)

Fornece funções para processamento de imagens.

#### Métodos

| Método | Descrição |
|--------|-----------|
| `carregar_e_redimensionar(caminho_imagem, max_width, max_height)` | Carrega e redimensiona uma imagem |
| `redimensionar_imagem(img, max_width, max_height)` | Redimensiona uma imagem preservando a proporção |

## Diagrama de Classes

```
+----------------+     +----------------+     +----------------+
| MainWindow     |---->| ImageManager   |     | ImageProcessor |
+----------------+     +----------------+     +----------------+
| - root         |     | - pasta_origem |     | + carregar_e_  |
| - image_manager|<----|               |---->|   redimensionar|
+----------------+     +----------------+     +----------------+
| + configurar_  |     | + selecionar_  |     | + redimensionar|
|   interface()  |     |   pasta()      |     |   _imagem()    |
| + mover_imagem |     | + mover_imagem |     +----------------+
| + pular_imagem |     | + pular_imagem |
+----------------+     +----------------+
```

## Fluxo de Execução

1. O arquivo `main.py` inicia a aplicação
2. Uma instância de `MainWindow` é criada, que por sua vez cria uma instância de `ImageManager`
3. O usuário seleciona uma pasta através da interface
4. O `ImageManager` carrega as imagens da pasta
5. A interface exibe as imagens e permite a classificação
6. As ações do usuário são processadas e refletidas na interface e no sistema de arquivos

## Personalização e Extensão

Para adicionar novos recursos ou modificar existentes:

- **Adicionar novos tipos de classificação**: Modificar `ImageManager.mover_imagem()` e adicionar novos botões na interface
- **Suportar novos formatos de imagem**: Alterar o filtro em `ImageManager.carregar_imagens()`
- **Adicionar atalhos de teclado**: Adicionar novos bindings em `MainWindow.configurar_atalhos()`
