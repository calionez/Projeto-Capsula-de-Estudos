# Guia — organizar e publicar no GitHub

Este guia explica como subir o projeto Cápsula de Estudos para um repositório no GitHub.

## 1. Criar uma conta no GitHub (se ainda não tiver)

1. Acesse [github.com](https://github.com)
2. Clique em **Sign up** e siga os passos

## 2. Instalar o Git (se ainda não tiver)

1. Baixe em [git-scm.com](https://git-scm.com/downloads)
2. Instale com as opções padrão
3. No terminal do VS Code, confirme que funcionou:
   ```powershell
   git --version
   ```

## 3. Criar o repositório vazio no GitHub

1. No canto superior direito do GitHub, clique no ícone **+** → **New repository**
2. Preencha:
   - **Repository name**: `capsula-estudos`
   - **Description** (opcional): "Sistema web para organizar matérias e tópicos de estudo"
   - **Visibility**: escolha **Public** (para mostrar no portfólio) ou **Private**
   - **Não marque** nenhuma das opções de inicializar com README, .gitignore ou licença — o projeto já tem esses arquivos
3. Clique em **Create repository**

Você vai cair numa página com instruções e uma URL parecida com:

```
https://github.com/calionez/capsula-estudos.git
```

Copie essa URL — você vai usar no próximo passo.

## 4. Subir o projeto local para o GitHub

No terminal do VS Code, dentro da pasta do projeto (a mesma onde está o `app.py`):

```powershell
git init
git add .
git commit -m "Primeira versão da Cápsula de Estudos"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/capsula-estudos.git
git push -u origin main
```

Troque `SEU-USUARIO` pelo seu nome de usuário real do GitHub (ou cole a URL exata que você copiou no passo anterior).

Na primeira vez, o Git pode abrir uma janela do navegador pedindo para você autorizar o acesso à sua conta — basta confirmar.

## 5. Confirmar que subiu certo

1. Acesse `https://github.com/SEU-USUARIO/capsula-estudos`
2. Você deve ver todos os arquivos do projeto (`app.py`, `templates/`, `static/`, `README.md`, etc.)
3. Confirme que o arquivo `database.db` **não aparece** na lista — ele deve ter sido ignorado pelo `.gitignore`, como esperado

## Enviando atualizações depois

Sempre que você fizer mudanças no código e quiser atualizar o GitHub (e, consequentemente, disparar um novo deploy automático no Render, se já estiver configurado):

```powershell
git add .
git commit -m "Descreva o que você mudou aqui"
git push
```

## Erros comuns

**`git: command not found` ou `git não é reconhecido`**
O Git não foi instalado corretamente, ou o terminal precisa ser reaberto depois da instalação.

**`fatal: remote origin already exists`**
Você já rodou `git remote add origin` antes. Use `git remote set-url origin URL` em vez disso.

**Pede usuário e senha e a senha normal não funciona**
O GitHub não aceita mais senha comum para `git push` via HTTPS. Ele deve abrir uma janela de login no navegador automaticamente (autenticação via navegador) — se isso não acontecer, será necessário criar um [token de acesso pessoal](https://github.com/settings/tokens) e usá-lo no lugar da senha.
