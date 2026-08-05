## 📌 Project Overview
**OpenWA** is an open-source, multi-session WhatsApp REST API gateway and automation engine. Built on **NestJS**, **TypeScript**, and modular engine adapters (such as `whatsapp-web-js` and `baileys`), OpenWA transforms WhatsApp accounts into controllable REST endpoints, event-driven webhooks, and automation pipelines.

It features multi-session isolation, QR code authentication, webhooks with HMAC signatures, plugin extension hooks, a React dashboard, and SQLite storage for persistent session keys and state tracking.

---

## 📂 Project Directory Structure

```
OpenWA/
├── .github/                      # CI/CD workflows, issue templates & automation
├── dashboard/                    # React/Vite web-based management dashboard
├── data/                         # Persistent database (SQLite), sessions & runtime assets
├── docker/                       # Docker containerization scripts, entrypoints & environments
├── docs/                         # OpenAPI specs, API docs & architectural guides
├── OpenWA_Backend/               # Python Auto-Reply & Twenty CRM Integration Backend
│   ├── assets/                   # Static branding images & PDF pitch decks
│   ├── app.py                    # Flask server, webhook signature verification & router
│   ├── chatbot.py                # State-machine chatbot navigation engine
│   ├── config.py                 # System constants, env variables & menu definitions
│   ├── crm.py                    # Twenty CRM API integration & phone parser
│   ├── state.py                  # Stateful session tracker with JSON disk persistence
│   ├── users.json                # User state store (chatId -> stage, last_seen)
│   └── requirements.txt          # Python dependencies
├── plugins/                      # Custom plugin loaders and core OpenWA plugins
├── scripts/                      # Build, dev, database maintenance & setup scripts
├── sdk/                          # Client SDK libraries (TypeScript/JS) for REST API
├── src/                          # Main NestJS Application Source Code
│   ├── common/                   # Shared guards, decorators, filters, interceptors & utils
│   ├── config/                   # Configuration services & env schema validation
│   ├── core/                     # Core event bus, schedulers, session manager & tasks
│   ├── database/                 # TypeORM database config, entities & repositories
│   ├── engine/                   # Adapter abstraction layer (whatsapp-web-js / baileys)
│   ├── modules/                  # REST Controllers & Services (Sessions, Messages, Webhooks)
│   ├── plugins/                  # Plugin execution runtime & sandbox handlers
│   ├── app.module.ts             # Primary NestJS application entry module
│   └── main.ts                   # Bootstrap entry point (Pipes, Swagger, CORS, Listeners)
├── test/                         # End-to-end (E2E) and unit test suite
├── .env.example                  # Environment configuration template
├── Dockerfile                    # Multi-stage Docker build recipe
├── docker-compose.yml            # Production orchestration stack
├── docker-compose.dev.yml        # Local development environment stack
├── nest-cli.json                 # NestJS framework build configuration
├── openapi.json                  # Swagger OpenAPI 3.0 API spec definition
├── package.json                  # Node.js project manifest & scripts
└── tsconfig.json                 # TypeScript compiler configuration
```

### Major Directory Responsibilities
- **`src/`**: Core NestJS application hosting REST APIs, WebSocket gateways, database entities, session life-cycle handling, and adapter abstraction wrappers.
- **`dashboard/`**: Front-end React control panel to monitor session status, scan QR codes, inspect live logs, and manage API keys visually.
- **`OpenWA_Backend/`**: Python microservice running alongside OpenWA. Processes incoming webhooks, drives interactive menu state machines, dispatches media/documents, and syncs leads to Twenty CRM.
- **`plugins/`**: Isolated hooks that intercept messages, transform data, or trigger automated custom logic prior to API or webhook dispatch.
- **`sdk/`**: Client SDK bindings allowing external Node/TS projects to control OpenWA programmatically.
- **`docker/` & `Dockerfile`**: Multi-stage container builds wrapping Chromium, Node.js, dependencies, and environment setup for headless WhatsApp session execution.
- **`data/`**: Runtime persistent storage containing `sqlite.db`, session tokens, and cached media.

---

## 🏗️ Architecture & Component Flow

### Overall System Architecture Diagram

```mermaid
graph TD
    subgraph Client & Frontend Layer
        UserPhone[WhatsApp User Device]
        Dash[React Dashboard]
        APIClient[External REST Clients]
    end

    subgraph OpenWA Core Gateway (NestJS)
        API[NestJS REST API / Swagger]
        SessMgr[Session Manager]
        Engine[Adapter: whatsapp-web-js / Baileys]
        DB[(SQLite / Data Store)]
        WebHookDispatcher[Webhook Dispatcher]
    end

    subgraph Custom Backend & CRM
        Flask[Python Flask Server :5000]
        Chatbot[State Engine & Rule Processor]
        TwentyCRM[Twenty CRM API]
    end

    UserPhone <-->|WhatsApp Web Protocol| Engine
    Dash <-->|HTTP / REST| API
    APIClient <-->|HTTP / API Key| API
    API <--> SessMgr <--> Engine
    SessMgr <--> DB

    Engine -->|Inbound Event| WebHookDispatcher
    WebHookDispatcher -->|HTTP POST + HMAC SHA256| Flask
    Flask --> Chatbot
    Flask -->|Sync Lead| TwentyCRM
    Flask -->|HTTP POST Send Message| API
```

---

## 🔄 Core Engine Mechanics

### Request / Response Flow
1. **API Request**: External client submits HTTP POST to `/api/sessions/{sessionId}/messages/send-text` with header `X-API-Key`.
2. **Authentication & Guard**: NestJS `ApiKeyGuard` verifies header against system configuration.
3. **Session Routing**: `SessionManager` retrieves active session instance.
4. **Adapter Dispatch**: Call standard adapter interface method (e.g. `sendMessage`).
5. **WhatsApp Transport**: Engine translates request to WebSocket frames or web protocol calls to WhatsApp servers.
6. **Response**: HTTP 200/201 JSON confirmation returned to client.

### OpenWA Server Lifecycle
1. **Bootstrap (`main.ts`)**: Loads environment, initializes NestJS app, sets up Global Validation Pipes, CORS, and Swagger UI at `/docs`.
2. **Database Connect**: Establishes TypeORM SQLite connection (`data/sqlite.db`).
3. **Session Restoration**: Checks active session records in SQLite and reinstantiates headless browser or socket instances.
4. **Adapter Initialization**: Boots Puppeteer/Chromium instances for browser-based sessions or establishes direct socket connections.
5. **Webhook Listening**: System enters event loop, listening for incoming messages, battery updates, and connection status events.

### Session Management & Authentication
- **Session ID**: Every WhatsApp account connected is assigned a unique `sessionId` string.
- **Authentication**: Requests must include the header `X-API-Key: <configured_key>`.
- **QR Code Authentication**: When a new session is spawned via POST `/api/sessions`, OpenWA emits a QR code via WebSocket/Dashboard or REST endpoint (`/api/sessions/{id}/qr`) to pair with WhatsApp.

---

## 🐳 Docker Architecture & Storage
- **Docker Compose**: Orchestrates `openwa-core` (Node.js/NestJS) and optional microservices (like `openwa-python-backend`).
- **Headless Chromium**: Docker image bundles standard Google Chromium dependencies to support headless web scraping protocols required by `whatsapp-web-js`.
- **Database & Storage**:
  - `data/sqlite.db`: Stores session metadata, webhooks, API tokens, and persistent system configuration.
  - `data/sessions/`: Retains Puppeteer/Browser profile caches and local storage to keep accounts logged in across container restarts.

---

## 🚀 Build, Run & Deployment

### Local Development Setup
```bash
# 1. Install dependencies
npm install

# 2. Configure Environment
cp .env.example .env

# 3. Start Development Server
npm run start:dev
```

### Docker Deployment
```bash
# Build and start via Docker Compose
docker-compose up -d --build
```
