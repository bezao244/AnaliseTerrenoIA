# AnaliseTerrenoIA

Sistema de análise de terrenos utilizando Inteligência Artificial (Google Gemini) com backend em FastAPI e frontend em React + TypeScript.

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Obtendo a Chave da API Gemini](#obtendo-a-chave-da-api-gemini)
- [Instalação e Execução](#instalação-e-execução)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (React)](#frontend-react)
- [Executando os Testes](#executando-os-testes)
  - [Testes do Backend](#testes-do-backend)
  - [Testes do Frontend](#testes-do-frontend)
- [Referência da API](#referência-da-api)
- [Solução de Problemas](#solução-de-problemas)

---

## Visão Geral

O **AnaliseTerrenoIA** permite enviar imagens de terrenos e receber uma análise detalhada gerada por IA, incluindo:

- Classificação do tipo de solo/terreno
- Composição percentual dos componentes do terreno
- Identificação de áreas férteis
- Pontuação de fertilidade (0–10)
- Mapa de calor (heatmap) sobre a imagem original
- Exportação do relatório em PDF
- Histórico de análises salvo em banco de dados local (SQLite)

---

## Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Análise por IA | Google Gemini 1.5 Flash analisa a imagem do terreno |
| Heatmap | Sobreposição visual colorida indicando composição do solo |
| Exportação PDF | Relatório completo gerado com ReportLab |
| Histórico | Todas as análises são persistidas em SQLite |
| Interface Web | React + TypeScript + Tailwind CSS com animações Framer Motion |

---

## Pré-requisitos

Certifique-se de ter instalados:

| Ferramenta | Versão mínima | Verificação |
|---|---|---|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Git | qualquer | `git --version` |

---

## Obtendo a Chave da API Gemini

O backend utiliza o **Google Gemini** para análise de imagens. É necessário criar uma chave de API gratuita:

1. Acesse [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Faça login com uma conta Google
3. Clique em **"Create API key"** e copie a chave gerada
4. Guarde a chave — ela será usada na configuração do backend abaixo

---

## Instalação e Execução

### Clonando o repositório

```bash
git clone https://github.com/bezao244/AnaliseTerrenoIA.git
cd AnaliseTerrenoIA
```

---

### Backend (FastAPI)

> Execute estes comandos em um terminal dedicado.

#### 1. Entrar na pasta do backend

```bash
cd backend
```

#### 2. Criar e ativar o ambiente virtual Python

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

#### 4. Configurar a variável de ambiente

Copie o arquivo de exemplo e adicione sua chave Gemini:

**Linux / macOS:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

Abra o arquivo `.env` e substitua o valor da variável:

```
GEMINI_API_KEY=sua_chave_aqui
```

> **Dica:** Você pode editar com qualquer editor de texto: `notepad .env` (Windows) ou `nano .env` (Linux/macOS).

#### 5. Iniciar o servidor backend

```bash
uvicorn main:app --reload
```

O servidor estará disponível em: **http://localhost:8000**

Para confirmar que está funcionando, acesse no navegador:
- Documentação interativa (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

---

### Frontend (React)

> Execute estes comandos em **outro terminal**, mantendo o backend rodando.

#### 1. Entrar na pasta do frontend

A partir da raiz do projeto:

```bash
cd frontend
```

#### 2. Instalar as dependências

```bash
npm install
```

#### 3. Iniciar o servidor de desenvolvimento

```bash
npm run dev
```

O frontend estará disponível em: **http://localhost:5173**

> O Vite configura automaticamente um proxy: requisições para `/api` são encaminhadas para `http://localhost:8000`.

---

### Usando a aplicação

Com ambos os serviços rodando:

1. Acesse [http://localhost:5173](http://localhost:5173) no navegador
2. Na aba **"Nova Análise"**, clique em **"Selecionar Imagem"** e escolha uma foto de terreno
3. Clique em **"Analisar Terreno"** e aguarde o resultado
4. Visualize o heatmap e faça o download do relatório PDF
5. Na aba **"Histórico"**, veja todas as análises realizadas anteriormente

---

## Executando os Testes

### Testes do Backend

Com o ambiente virtual ativado e dentro da pasta `backend/`:

```bash
cd backend
source .venv/bin/activate   # Linux/macOS — pule se já estiver ativo
pytest
```

Para ver a saída detalhada:

```bash
pytest -v
```

Para executar um arquivo de testes específico:

```bash
pytest tests/test_main.py -v
pytest tests/test_analyzer.py -v
pytest tests/test_heatmap.py -v
```

> Os testes usam `pytest-asyncio` em modo automático (configurado em `pytest.ini`). Não é necessária a chave Gemini para rodar os testes — eles utilizam mocks.

---

### Testes do Frontend

Dentro da pasta `frontend/`:

```bash
cd frontend
npm test
```

Para executar com saída detalhada e watch mode (reexecuta ao salvar arquivos):

```bash
npm run test -- --reporter=verbose
```

---

## Referência da API

Base URL: `http://localhost:8000`

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/health` | Verifica se a API está funcionando |
| `POST` | `/api/analyses` | Envia uma imagem para análise |
| `GET` | `/api/analyses` | Lista todas as análises salvas |
| `GET` | `/api/analyses/{id}` | Retorna uma análise específica |
| `GET` | `/api/analyses/{id}/heatmap` | Retorna o heatmap (PNG) |
| `GET` | `/api/analyses/{id}/report` | Baixa o relatório em PDF |

### Exemplo: enviar imagem para análise

```bash
curl -X POST http://localhost:8000/api/analyses \
  -F "file=@/caminho/para/imagem.jpg"
```

### Exemplo: listar análises

```bash
curl http://localhost:8000/api/analyses
```

A documentação interativa completa da API está disponível em [http://localhost:8000/docs](http://localhost:8000/docs) enquanto o backend estiver em execução.

---

## Solução de Problemas

### `ModuleNotFoundError` ao iniciar o backend

Certifique-se de que o ambiente virtual está ativado e as dependências foram instaladas:

```bash
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

### `GEMINI_API_KEY` não configurada

Verifique se o arquivo `.env` existe na pasta `backend/` e contém a chave correta:

```bash
cat backend/.env
# Deve exibir: GEMINI_API_KEY=sua_chave_aqui
```

### Erro `400 Bad Request` ao enviar imagem

- Confirme que o arquivo enviado é uma imagem válida (JPG, PNG, WEBP)
- Verifique se o arquivo não está corrompido ou vazio

### Erro `422 Unprocessable Entity` ao analisar imagem

A IA identificou que a imagem não representa um terreno válido. Tente com uma foto de solo, campo, área rural ou urbana vista de cima.

### Frontend não consegue se comunicar com o backend

- Confirme que o backend está rodando em `http://localhost:8000`
- Confirme que o frontend está sendo executado com `npm run dev` (porta 5173)
- Verifique se nenhum firewall ou antivírus está bloqueando as portas 8000 ou 5173

### Porta 8000 ou 5173 já em uso

Para usar uma porta diferente no backend:

```bash
uvicorn main:app --reload --port 8001
```

Para usar uma porta diferente no frontend:

```bash
npm run dev -- --port 3000
```

---

## Estrutura do Projeto

```
AnaliseTerrenoIA/
├── backend/
│   ├── main.py           # Entrypoint FastAPI, definição das rotas
│   ├── analyzer.py       # Integração com Google Gemini AI
│   ├── database.py       # Configuração SQLAlchemy + SQLite
│   ├── models.py         # Modelos ORM (tabela analyses)
│   ├── schemas.py        # Schemas Pydantic para validação
│   ├── heatmap.py        # Geração do mapa de calor
│   ├── pdf_export.py     # Geração de relatório PDF
│   ├── requirements.txt  # Dependências Python
│   ├── .env.example      # Exemplo de variáveis de ambiente
│   └── tests/            # Testes automatizados (pytest)
└── frontend/
    ├── src/
    │   ├── App.tsx        # Componente principal
    │   ├── api/           # Cliente HTTP (Axios)
    │   ├── components/    # Componentes React
    │   └── types/         # Interfaces TypeScript
    ├── package.json       # Dependências e scripts npm
    └── vite.config.ts     # Configuração Vite + proxy
```