# AI Math Chatbot Project Structure

This document outlines the structure of the AI Math Chatbot project—a full-stack, portfolio-quality application designed to showcase advanced AI engineering skills and provide mathematical assistance through a modern chat interface.

## Project Overview

The project is organized into two main components:
1. **Backend**: Python-based API server built with FastAPI, integrating Google Gemini LLM and Whisper STT
2. **Frontend**: React-based web application built with Next.js, featuring a responsive, accessible UI

## Directory Structure

```
AI_MATH_CHATBOT/
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── README.md                 # Project documentation and showcase
├── project-structure.md      # Project structure documentation
├── aichatbot.db              # SQLite database
├── docker-compose.yml        # Docker Compose configuration
├── docs/                     # Project documentation, rules, and references
│   ├── gemini_api_doc.md
│   ├── AI_ Math_Chatbot_Development_Roadmap.md
│   ├── AI-MATH-CHATBOT-PRD.md
│   ├── Global_Rules.md
│   └── Project_Rules.md
├── assets/                   # Project screenshots and demo images
│   ├── demo.png
│   ├── file_upload_demo.png
│   ├── Initial_page_dark_mode.png
│   ├── Initial_page_light_mode.png
│   └── voice_input_demo.png
├── backend/                  # Backend application
│   ├── .gitignore
│   ├── Dockerfile
│   ├── README.md
│   ├── alembic.ini
│   ├── aichatbot.db
│   ├── db_manager.py
│   ├── migrate.py
│   ├── requirements.txt
│   ├── .env.example          # Example environment file (template)
│   ├── app/                  # Main application code
│   │   ├── __init__.py
│   │   ├── cleanup_tasks.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py           # Application entry point
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── seed_db.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   ├── crud/             # Database CRUD operations
│   │   │   ├── __init__.py
│   │   │   ├── chat_crud.py
│   │   │   └── file_crud.py
│   │   ├── middleware/       # Middleware components
│   │   │   ├── __init__.py
│   │   │   ├── error_handler.py
│   │   │   ├── exception_handlers.py
│   │   │   ├── error_utils.py
│   │   │   ├── rate_limiter.py
│   │   │   └── README.md
│   │   ├── routers/          # API route handlers
│   │   │   ├── chat_router.py
│   │   │   ├── file_router.py
│   │   │   ├── message_router.py
│   │   │   ├── speech_router.py
│   │   │   ├── streaming_router.py
│   │   │   └── README_SPEECH.md
│   │   ├── utils/            # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── sanitizer.py
│   │   │   └── README.md
│   │   ├── tests/            # (To be implemented) Test files
│   ├── migrations/           # Database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   ├── README
│   │   └── versions/
│   └── __pycache__/
└── frontend/                 # Frontend application
    ├── .gitignore
    ├── Dockerfile
    ├── README.md
    ├── package.json
    ├── package-lock.json
    ├── pnpm-lock.yaml
    ├── next.config.mjs
    ├── next-env.d.ts
    ├── postcss.config.mjs
    ├── tailwind.config.ts
    ├── tsconfig.json
    ├── .env.local            # Frontend environment variables
    ├── .env.example          # Example environment file
    ├── app/                  # Next.js app directory
    │   ├── globals.css
    │   ├── layout.tsx
    │   └── page.tsx
    ├── components/           # React components
    │   ├── chat-input.tsx
    │   ├── chat-message.tsx
    │   ├── markdown-renderer.tsx
    │   ├── mode-toggle.tsx
    │   ├── recording-modal.tsx
    │   ├── sidebar.tsx
    │   ├── theme-provider.tsx
    │   └── ui/               # UI subcomponents
    ├── hooks/                # Custom React hooks
    │   ├── use-toast.ts
    │   ├── use-media-query.ts
    │   └── use-mobile.tsx
    ├── lib/                  # Utility libraries and API services
    │   ├── api-config.ts
    │   ├── api-service.ts
    │   ├── store.ts
    │   ├── types.ts
    │   └── utils.ts
    ├── public/               # Static assets
    │   ├── placeholder.jpg
    │   ├── placeholder.svg
    │   ├── placeholder-user.jpg
    │   ├── placeholder-logo.svg
    │   └── placeholder-logo.png
    ├── styles/               # CSS styles
        └── globals.css
```

## Key Components

### Backend

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Google Gemini LLM Integration**: Advanced math reasoning, streaming, and multimodal support
- **Whisper STT Integration**: Speech-to-text for voice input
- **SQLite Database**: Lightweight database for chat history
- **Pydantic Models**: Data validation and settings management
- **Middleware**: Request processing and CORS
- **Robust Error Handling**: Centralized exception handling and logging

### Frontend

- **Next.js & React**: Modern, server-rendered React app
- **Tailwind CSS**: Utility-first CSS framework for responsive, accessible UI
- **TypeScript**: Strong typing for maintainability
- **KaTeX**: Fast, high-quality math rendering
- **Zustand**: State management for chat, theme, and more
- **Accessibility (A11y)**: WCAG 2.1 AA compliance, semantic HTML, keyboard navigation
- **Streaming & File Upload**: Real-time LLM responses, multi-part file upload, and voice input

## Development Setup

- **Environment Variables:**
  - Backend: Copy `.env.example` from `backend/` and create `.env` in the same directory
  - Frontend: Use `.env.local` for API base URL and config
- **Docker Compose:** Orchestrates both frontend and backend for local development
- **Testing:**
  - **Note:** Unit, integration, and E2E tests will be implemented in a later stage. The project is structured for easy test integration (pytest, jest, react-testing-library, Playwright/Cypress).

## Future Considerations

- **Advanced Math Capabilities:** Symbolic computation (e.g., SymPy) for algebraic manipulation and equation solving
- **User Authentication:** Optional login for saving personal chat history and preferences
- **Admin Dashboard:** Analytics, usage stats, and moderation tools
- **Multilingual Support:** Expand to support multiple languages
- **Mobile App:** React Native or Flutter client for mobile devices
- **Enhanced A11y:** Further improvements for screen readers and cognitive accessibility
- **Cloud Deployment:** One-click deploy to GCP, AWS, or Azure
- **Automated Testing:** CI/CD integration for automated test runs and deployments
- **Plugin System:** Allow users to extend chatbot capabilities with custom plugins
- **Calculator:** Add a calculator with basic and scientific modes to the chatbot
- **Graphs and Charts:** Add the ability to create graphs and charts from data
- **Canvas drawing:** Add the ability to draw on a canvas mathematical expressions, geometry, graphs, etc.
- **Unit/Integration/E2E Testing:** Add unit, integration, and E2E tests
- **UX/UI:** Some improvements to the UI and UX

---

**This project is designed as a production-grade, portfolio-quality example of modern AI application development.**
