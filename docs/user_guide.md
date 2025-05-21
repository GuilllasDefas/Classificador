# Guia do Usuário

## Introdução

O Classificador de Imagens permite organizar e classificar imagens manualmente de forma rápida e eficiente. Este guia apresenta as principais funcionalidades e como utilizá-las.

## Iniciando

1. Execute o aplicativo através do arquivo `main.py`
2. Clique no botão "Selecionar Pasta" para escolher o diretório que contém as imagens a serem classificadas
3. Após selecionar a pasta, a primeira imagem será exibida automaticamente

## Interface Principal

![Interface do usuário](screenshots/interface_labeled.png)

A interface é composta por:

1. **Nome da imagem atual**: Exibido na parte superior
2. **Visualizador de imagem**: Área central que exibe a imagem atual
3. **Botões de ação**: 
   - **Voltar**: Retorna à imagem anterior
   - **Selecionar Pasta**: Abre o diálogo para selecionar a pasta de imagens
   - **Abrir Pasta**: Abre a pasta selecionada no explorador de arquivos do sistema
   - **Certo**: Classifica a imagem como "certa" e a move para a subpasta correspondente
   - **Errado**: Classifica a imagem como "errada" e a move para a subpasta correspondente
   - **Pular**: Avança para a próxima imagem sem classificar
   - **Pular 10**: Avança 10 imagens sem classificar
4. **Barra de status**: Exibe informações sobre o progresso da classificação

## Atalhos de Teclado

Para agilizar o processo de classificação, utilize os seguintes atalhos:

| Ação | Atalho |
|------|--------|
| Classificar como "certo" | `Enter` ou `→` (seta direita) |
| Classificar como "errado" | `Esc` ou `←` (seta esquerda) |
| Voltar para imagem anterior | `Backspace` |
| Pular imagem | `Espaço` |
| Pular 10 imagens | `Shift + Espaço` |

## Fluxo de Trabalho Recomendado

1. Selecione a pasta contendo as imagens que deseja classificar
2. Observe a imagem atual no centro da tela
3. Decida se a imagem está "certa" ou "errada" e classifique usando os botões ou atalhos de teclado
4. Continue o processo até classificar todas as imagens
5. Ao finalizar, as imagens estarão organizadas nas subpastas "certo" e "errado"

## Estrutura de Pastas

Ao selecionar uma pasta para classificação, o aplicativo cria automaticamente:

- Uma subpasta `certo` para armazenar as imagens classificadas como corretas
- Uma subpasta `errado` para armazenar as imagens classificadas como incorretas

## Dicas e Truques

- Use atalhos de teclado para classificação mais rápida
- Para verificar as imagens já classificadas, use o botão "Abrir Pasta" e navegue pelas subpastas
- Para classificar grandes quantidades de imagens, faça pausas regulares para evitar fadiga visual
