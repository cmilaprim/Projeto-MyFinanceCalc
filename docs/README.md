# MyFinanceCalc

Este projeto é uma aplicação financeira que permite calcular o rendimento de investimentos com base na taxa Selic e no percentual do CDI. A aplicação gera um PDF com os resultados e mantém um histórico das aplicações realizadas.

## Funcionalidades

- **Cálculo de Rendimentos**: Calcula o rendimento de uma aplicação financeira com base na taxa Selic e no percentual do CDI.
- **Geração de PDF**: Gera um PDF com os resultados do cálculo.
- **Histórico de Aplicações**: Mantém um histórico das aplicações realizadas, permitindo editar, excluir e visualizar os resultados.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Tkinter**: Biblioteca para criação da interface gráfica.
- **FPDF**: Biblioteca para geração de PDFs.
- **Pickle**: Biblioteca usada para salvar o histórico).

## Estrutura do Projeto

/Projeto-MyFinanceCalc
│
├── /src                      # Código-fonte
│   ├── __init__.py           # Indica que é um pacote
│   ├── calcula_aplicacao.py
│   ├── gera_documento.py
│   ├── historico.py
│   ├── tela_inicial.py
│   ├── main.py
│
├── /data                     # Dados armazenados
│   ├── historico.pkl
│
├── /assets                   # Imagens e ícones
│   ├── icon-investimento.ico
│   ├── logo-empresa.png
│
├── /docs                     # Documentação
│   ├── README.md
│
├── requirements.txt          # Dependências do projeto
│
└── /test                     # Testes 