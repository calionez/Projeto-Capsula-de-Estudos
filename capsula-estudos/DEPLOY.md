# Guia de deploy — Render

Este guia explica como colocar a Cápsula de Estudos no ar, gratuitamente, usando o [Render](https://render.com).

> O projeto já tem um arquivo `render.yaml` na raiz, que diz ao Render exatamente como construir e rodar a aplicação. Isso significa que o deploy é só conectar o repositório — nenhuma configuração manual é necessária.

## Antes de começar

Você precisa ter:

- Uma conta no [GitHub](https://github.com) com este projeto já enviado (veja o guia de organização do repositório, se ainda não fez isso)
- Uma conta no [Render](https://render.com) — pode criar com login do GitHub, sem precisar de cartão de crédito

## Passo 1 — Criar uma conta no Render

1. Acesse [render.com](https://render.com)
2. Clique em **Get Started** ou **Sign Up**
3. Escolha **Sign up with GitHub** — isso já conecta sua conta do GitHub automaticamente

## Passo 2 — Criar um novo Blueprint a partir do repositório

1. No painel do Render, clique em **New** (canto superior direito)
2. Selecione **Blueprint**
3. Selecione o repositório `capsula-estudos` na lista (se não aparecer, clique em **Configure GitHub App** e autorize o acesso ao repositório)
4. O Render vai detectar automaticamente o arquivo `render.yaml` e mostrar o serviço que será criado: um Web Service chamado `capsula-estudos`, plano **Free**
5. Clique em **Apply** (ou **Create New Resources**, dependendo da versão da interface)

O Render vai gerar automaticamente uma `SECRET_KEY` segura para o seu app — você não precisa configurar nada manualmente.

## Passo 3 — Acompanhar o primeiro deploy

1. Você será levado para a página do serviço, com uma aba de **Logs**/**Events**
2. Acompanhe o build: o Render vai instalar as dependências do `requirements.txt` e depois iniciar o servidor com Gunicorn
3. Quando o status mudar para **Live**, o deploy terminou

## Passo 4 — Acessar o site

No topo da página do serviço, o Render mostra a URL pública, algo como:

```
https://capsula-estudos.onrender.com
```

Clique nela para abrir o site no ar.

## O que esperar do plano gratuito

- O serviço **"dorme" depois de 15 minutos sem receber nenhuma visita**. A próxima pessoa que acessar vai esperar cerca de 1 minuto enquanto o servidor "acorda" — depois disso, fica rápido normalmente
- O banco de dados (SQLite) é um arquivo dentro do próprio serviço. Ele **não sobrevive** a um novo deploy — ou seja, toda vez que você atualizar o código e o Render reconstruir o serviço, os usuários, matérias e tópicos cadastrados são apagados
  - Isso é aceitável para portfólio e testes. Se no futuro você quiser que os dados sejam permanentes mesmo com atualizações de código, será necessário migrar para um banco PostgreSQL (o Render também oferece um plano gratuito para isso)

## Deploys futuros

Depois desse primeiro deploy, qualquer novo `git push` para a branch principal do seu repositório no GitHub vai disparar um novo deploy automaticamente no Render. Não é necessário repetir nenhum passo manual.

## Alternativa: criar o serviço manualmente (sem o render.yaml)

Caso prefira não usar o Blueprint, ou se o Render não detectar o arquivo `render.yaml` automaticamente, é possível configurar tudo manualmente:

1. No painel do Render, clique em **New** → **Web Service**
2. Conecte e selecione o repositório `capsula-estudos`
3. Configure os campos:
   - **Name**: `capsula-estudos` (ou o nome que preferir)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --workers 1 --threads 4`
   - **Instance Type**: `Free`
4. Em **Advanced** → **Environment Variables**, adicione:
   - `SECRET_KEY` → clique em **Generate** para um valor aleatório seguro
   - `FLASK_DEBUG` → `false`
5. Clique em **Create Web Service**

## Solução de problemas

**O deploy falhou na etapa de build**
Veja os logs na aba **Events** ou **Logs** do serviço — geralmente é uma dependência faltando no `requirements.txt`.

**O site abre, mas dá erro 500**
Verifique se a variável `SECRET_KEY` foi configurada. Veja os logs do serviço para a mensagem de erro completa.

**Quero resetar o banco de dados**
Como o SQLite não é persistente nesse plano, basta fazer um novo deploy manual (botão **Manual Deploy** → **Deploy latest commit**) que o banco será recriado vazio.
