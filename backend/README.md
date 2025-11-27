# AI Math Chatbot - Backend

This is the **backend** for the AI Math Chatbot application, built with FastAPI, SQLAlchemy, and the Google Gemini API. It provides robust, secure, and scalable API endpoints for chat, file upload, speech-to-text, and chat history management.

## 🌟 Key Features

- **RESTful API** for chat, file upload, and speech-to-text
- **Streaming LLM responses** (Google Gemini 2.5 Flash)
- **Multimodal input support:** text, images, PDFs, DOCX
- **Speech-to-text** via Whisper (Hugging Face)
- **Persistent chat history** with SQLite + SQLAlchemy
- **File management** (inline and Gemini Files API, **up to 5 files per request**)
- **Robust error handling** and logging
- **Rate limiting** and input sanitization for security
- **Automatic background maintenance** (expired file cleanup, message pruning)

## 🧑‍💻 Engineering & Best Practices

- **FastAPI** for high-performance, async API development
- **SQLAlchemy ORM** for safe, efficient database access
- **Alembic** for database migrations
- **Centralized error handling** with custom middleware and exception handlers
- **Structured logging** for debugging and monitoring
- **Environment-based config** (see `.env.example`)
- **Security:**
  - API key management via environment variables
  - Input sanitization (text, filenames, MIME types)
  - Rate limiting per endpoint
  - No sensitive data in logs or responses
- **Modular codebase:** routers, services, CRUD, middleware, utils

## 🏗️ Project Structure

See [project-structure.md](../project-structure.md) for a detailed breakdown of the backend and overall project layout.

## ⚙️ Database Management

- **SQLite** for local development (configurable via `DATABASE_URL`)
- **Schema:** Chats, Messages, GeminiFiles (see `app/models.py`)
- **Management script:** `db_manager.py` for init, seed, reset, backup, clean, check
- **Migrations:** Alembic for schema evolution

## 🛡️ Security & Error Handling

- **Centralized error handling:**
  - `ErrorHandlerMiddleware` for global exception capture
  - Custom exception handlers for validation, HTTP, and Gemini API errors
- **Rate limiting:**
  - `RateLimiter` middleware with configurable per-endpoint limits
- **Input sanitization:**
  - Text, filenames, and MIME types validated and sanitized
- **API key management:**
  - All secrets loaded from environment variables, never hardcoded

## 🔗 API Endpoints

- `POST /chats`: Create a new chat
- `GET /chats`: Get all chats
- `GET /chats/{chat_id}`: Get a specific chat
- `PUT /chats/{chat_id}`: Update a chat
- `DELETE /chats/{chat_id}`: Delete a chat
- `POST /chats/{chat_id}/messages/`: Send a message to a chat
- `GET /chats/{chat_id}/messages/`: Get all messages in a chat
- `POST /chats/{chat_id}/stream`: Send a message and receive a streaming response
- `POST /upload-file`: Upload up to 5 files (PDF, image, DOCX, text) at once
- `POST /stt`: Transcribe audio to text

## 🏃 Running the Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize the database
python db_manager.py init

# Run the server
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## 🧪 Testing

**Note:** Backend tests will be implemented in a later stage. The project is structured for easy test integration using:

- `pytest` for unit/integration tests
- `httpx` or FastAPI's `TestClient` for API testing
- Mocking for external APIs (Gemini, Whisper)

## 🗂️ More Information

- See [main README](../README.md) for global setup, features, and deployment
- See [project-structure.md](../project-structure.md) for a full directory breakdown

## 🔮 Future Considerations

- **Advanced Admin Tools:** Analytics dashboard, usage stats, moderation
- **Plugin System:** Allow custom backend plugins for new features
- **More Analytics:** Track API usage, errors, and performance metrics
- **Advanced Rate Limiting:** User-based, adaptive, or token bucket algorithms
- **Multi-DB Support:** Add support for PostgreSQL or MySQL
- **Automated Testing:** CI/CD integration for automated test runs and deployments
- **Multilingual Support:** Backend i18n for error messages and logs
- **Enhanced File Scanning:** Malware scanning for uploads
- **User Authentication:** Optional login for chat history and personalization

---

**Showcase your backend engineering skills:** This project is designed to be a portfolio-quality, production-grade example of modern AI API development. Contributions and feedback are welcome!