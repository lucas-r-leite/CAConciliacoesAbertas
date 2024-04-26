# Dashboard Conciliações Abertas - Conta Azul

## Descrição

Um script python que cria um dashboard web com todas as conciliações abertas de uma lista de clientes da plataforma Conta Azul

## Instalação

Recomendo a criação de um ambiente virtual em python para rodar o projeto:
``` python -m venv /path/to/new/virtual/environment```

Após a criação do ambiente virtual, ative-o e instale as bibliotecas python necessárias para o projeto:
```
. venv/bin/activate
pip install -r requirements.txt
```

Feita a instalação das dependências, o script *plotlyConciliacao.py* pode ser executado:
```python3 plotlyConciliacao.py```

## Usabilidade

Adicione o(s) XAuthorization do(s) cliente(s) no arquivo *authorizationTemplate.xlsx*  e o renomei para *authorization.xlsx*.
