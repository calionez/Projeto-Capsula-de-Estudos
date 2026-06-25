# Cápsula de Estudos

Sistema web para organizar matérias e tópicos de estudo, com controle de progresso e revisões.

## Sobre o projeto

A Cápsula de Estudos permite que cada usuário crie sua própria conta, cadastre as matérias que está estudando e divida o conteúdo de cada uma em tópicos. Cada tópico pode ter um resumo, um nível de dificuldade e uma data de revisão, além de poder ser marcado como pendente ou feito.

## Funcionalidades

- Cadastro e login de usuários, com senha protegida por hash
- Criação, edição e exclusão de matérias
- Criação, edição e exclusão de tópicos dentro de cada matéria
- Marcação de tópicos como feito ou pendente
- Dashboard com total de matérias, total de tópicos, tópicos pendentes e a próxima revisão agendada
- Tema claro e escuro, com a preferência salva no navegador
- Isolamento de dados entre usuários: cada pessoa só vê e edita o que é seu

## Tecnologias usadas

- [Python](https://www.python.org/) com [Flask](https://flask.palletsprojects.com/)
- SQLite como banco de dados
- HTML, CSS e JavaScript puros, com templates Jinja2
- [Gunicorn](https://gunicorn.org/) como servidor de produção

## Estrutura do projeto

```
capsula-estudos/
├─ app.py              # rotas e lógica principal da aplicação
├─ database.py         # conexão e criação das tabelas do banco
├─ requirements.txt    # dependências do projeto
├─ render.yaml         # configuração de deploy no Render
├─ templates/           # páginas HTML (Jinja2)
└─ static/
   ├─ css/style.css     # estilos
   └─ js/script.js      # alternância de tema e pequenas interações
```

## Como rodar localmente

### Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado

### Passo a passo

Clone o repositório e entre na pasta:

```bash
git clone https://github.com/SEU-USUARIO/capsula-estudos.git
cd capsula-estudos
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Rode o projeto:

```bash
python app.py
```

Acesse no navegador:

```
http://127.0.0.1:5000
```

O banco de dados (`database.db`) é criado automaticamente na primeira execução.

## Deploy

Este projeto está configurado para deploy gratuito no [Render](https://render.com) através do arquivo `render.yaml`.

- Para organizar e publicar o projeto no GitHub, veja [`GITHUB.md`](GITHUB.md)
- Para o passo a passo completo de deploy no Render, veja [`DEPLOY.md`](DEPLOY.md)

## Licença

Projeto pessoal de estudo, livre para uso e modificação.
