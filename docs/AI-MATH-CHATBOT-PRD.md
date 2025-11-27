**AI Math Chatbot - PRD**

**1. High-Level UX Flow**

*   **Initial State:** User lands on the application. The main view is clean, featuring the main text input bar centered horizontally and vertically within the viewport. A welcome message (e.g., "Ask me anything about math!") appears directly above the input bar. A collapsible sidebar on the left shows options for "New Chat" and lists previous chat sessions (initially hidden on mobile, collapsed by default on desktop).
*   **Text Query Flow:**
    1.  User types a math question or problem into the text input field. The input bar dynamically resizes vertically as text is added, up to a defined maximum height (e.g., 200px), after which a scrollbar appears within the input area.
    2.  User clicks the "Send" button (right side of input bar) or presses Enter.
    3.  The Send button transforms into a spinning "Stop" icon. The user's message appears in the chat history (right-aligned, inside a bubble).
    4.  A loading indicator message ("Thinking...") appears temporarily in the AI's response area (left-aligned).
    5.  The AI's response streams token-by-token into the chat history (left-aligned, no bubble), formatted appropriately (including math equations rendered using KaTeX).
    6.  The user can click the spinning "Stop" button or press Enter again to interrupt the AI's generation.
    7.  Once generation is complete (or interrupted), the Stop button reverts to the Send button.
*   **File Upload Query Flow:**
    1.  User clicks the "Upload File" button (paperclip icon, left side of input bar).
    2.  The OS file picker opens. User selects a supported file: **PDF (`.pdf`), Image (`.jpg`, `.png`, `.webp`, `.heic`, `.heif`), Text (`.txt`), or Word (`.docx`)**.
    3.  A visual indicator (e.g., a small chip) showing the filename appears *inside* the input bar. An option to remove the file (e.g., an 'x' on the chip) is available.
    4.  The user types a query *related* to the file in the text input field (e.g., "Solve problem 3 in the PDF," "Describe the graph in the image," "Explain the concept in section 2 of the document").
    5.  User clicks "Send".
    6.  The user's message (referencing the file context implicitly) appears in the chat history.
    7.  Loading indicator ("Thinking..."). Backend processes the file (extracts text from `.docx`/`.txt`, uses Gemini's multimodal capabilities for PDF/Image) and the text query.
    8.  AI's response, considering both text and file content, streams into the chat history.
*   **Voice Query Flow:**
    1.  User clicks the "Voice Input" button (microphone icon, left side of input bar).
    2.  Browser prompts for microphone permission if needed. Handle denial gracefully.
    3.  Visual indicator shows recording is active (e.g., pulsing mic icon).
    4.  User speaks their math query.
    5.  User clicks the "Stop Recording" button (or it stops automatically after a pause).
    6.  The transcribed text **appears directly in the text input field** for user review/editing.
    7.  User clicks "Send".
    8.  The transcribed query appears in the chat history.
    9.  Loading indicator ("Thinking...").
    10. AI's response streams into the chat history.
*   **Chat History Management:**
    1.  User clicks "New Chat" in the sidebar to clear the current conversation view and start fresh. The previous chat is saved and listed in the sidebar.
    2.  User clicks on a previous chat session in the sidebar to load its history into the main view.
    3.  User can **rename** or **delete** chat sessions via options associated with each chat item in the sidebar (e.g., hover menu, right-click). Confirmation needed for deletion.
*   **Clear Current Chat:**
    1.  User clicks the "Litter Bin" icon (top-right).
    2.  A confirmation dialog appears ("Are you sure you want to clear the current chat? This cannot be undone.").
    3.  Upon confirmation, the current chat view is cleared, similar to starting a "New Chat", but the cleared chat is *not* saved to history.
*   **Responsiveness:**
    *   **Mobile:** Sidebar is hidden by default, accessible via a "hamburger" menu icon (likely replacing the sidebar collapse toggle). Input elements remain functional. Font sizes adjust.
    *   **Tablet/Desktop:** Sidebar is visible but collapsible via a toggle button. Full layout otherwise.

**2. UI Layout & Style**

*   **Overall Style:** Minimalist, clean, focused on content. Strictly adheres to the ChatGPT aesthetic (light/dark themes, typography, spacing). **No authentication required.**
*   **Layout Components:**
    *   **Main Container:** Full viewport.
    *   **Sidebar (Left):**
        *   Fixed width on desktop (e.g., 260px), **collapsible** via a toggle button. Off-canvas/hidden on mobile.
        *   Contains: "New Chat" button (top), scrollable list of chat history items, theme toggle (top-left header area), potentially settings if added later.
    *   **Chat Area (Right/Main):**
        *   Takes remaining width/height.
        *   **Header Bar (Top):** Thin bar across the top.
            *   **Right Side:** Theme Toggle (Light/Dark switch), "Litter Bin" icon (Clear Current Chat).
            *   **Left Side:** Chatbot Title "**AI Math Chatbot**".
        *   **Conversation View:** Scrollable area.
            *   User messages: Aligned right, **wrapped in a bubble** with distinct background.
            *   AI responses: Aligned left, **NOT wrapped in a bubble**, text block width slightly wider than the input bar's maximum width.
        *   **Input Area:** Fixed at the bottom center of the Chat Area.
            *   **Left:** Microphone icon, Paperclip icon.
            *   **Center:** Resizable `textarea` for text input, potentially showing file chip(s).
            *   **Right:** Send/Stop button.
*   **Styling Details:**
    *   **Color Palette:**
        *   *Light Mode:* White background. Light gray for user message bubbles and sidebar. Black text. White input bar background.
        *   *Dark Mode:* Heavy dark gray (#202123 or similar) background. Dark gray (#343541 or similar) for user message bubbles, sidebar, and input bar background. White text.
        *   Accent color (e.g., subtle green/teal like ChatGPT) for buttons, icons, links.
    *   **Typography:** Clean sans-serif font (e.g., Inter, system default). Consistent sizes.
    *   **Spacing:** Consistent padding/margins (8px grid). Generous padding within user message bubbles.
    *   **Icons:** Clean, consistent set (Heroicons, Feather Icons).
    *   **Math Rendering:** **KaTeX** library for rendering LaTeX formulas beautifully inline and in display blocks. Ensure seamless integration within message areas.
    *   **Code Blocks:** AI generates code snippets. Render with monospace fonts, syntax highlighting, distinct background, and a "Copy" button within the block.

**3. Tools & Interactions**

*   **Text Input:**
    *   Multi-line `textarea`.
    *   **Animated placeholder text** cycling through math-related prompt suggestions (e.g., "Explain the Pythagorean theorem", "Solve x^2 + 5x + 6 = 0", "What is the integral of sin(x)?").
    *   Send button enabled when text area is not empty OR a file is staged.
    *   Shift+Enter for newline, Enter to send (unless AI is generating, then Enter interrupts).
    *   Displays file chip(s) when files are uploaded.
    *   Displays transcribed voice input for editing.
*   **File Upload Button (Paperclip):**
    *   Triggers file input.
    *   Accepts `.pdf`, `.png`, `.jpg`, `.jpeg`, `.webp`, `.heic`, `.heif`, `.txt`, `.docx`.
    *   Displays file chip in input bar with filename and remove ('x') button.
    *   Implement file size limits (e.g., based on Gemini API limits - 2GB via Files API, ~19MB effective limit for inline). Handle validation client-side first, then server-side.
*   **Voice Input Button (Microphone):**
    *   Uses `react-speech-recognition`.
    *   Handles microphone permissions.
    *   Visual feedback during recording (pulsing icon).
    *   Clear stop mechanism.
    *   **Display transcription in the text area** of the input bar.
*   **Chat Messages:**
    *   **User Messages:**
        *   Rendered in bubbles, right-aligned.
        *   Buttons appear on hover (or persistently on mobile touch): **Copy**, **Edit** (allows modifying the prompt and resubmitting), **Regenerate** (resends the same prompt).
    *   **AI Messages:**
        *   Rendered as plain text blocks, left-aligned.
        *   Buttons appear on hover/nearby: **Copy** (copies the entire AI response), **Regenerate** (requests a new response for the *preceding* user prompt).
    *   Support markdown formatting (bold, italics, lists, links, bullet points).
    *   Render LaTeX with KaTeX.
    *   Render code blocks with syntax highlighting and copy button.
*   **Chat History (Sidebar):**
    *   Highlight active chat.
    *   Show truncated titles (e.g., first user message).
    *   Provide Rename/Delete options on hover/click (with confirmation).
*   **Loading Indicators:** **"Thinking..."** message with pulsing dots appears as a temporary AI message while waiting for a response.
*   **Copy Feedback:** When a copy button is clicked, the icon temporarily changes to a **tick icon**, and a short-lived **toast message ("Copied!")** appears at the bottom-right of the screen.

**4. User Feedback & Error Handling**

*   **Feedback:**
    *   **Sending:** Send button changes to spinning stop icon.
    *   **Loading:** "Thinking..." message.
    *   **AI Responding:** Response streams token-by-token.
    *   **File Upload:** File chip appears in input; clear error message on failure.
    *   **Voice:** Recording indicator; transcription appears in input; error messages for failures.
    *   **Copying:** Icon change (copy -> tick) + Toast notification ("Copied!").
    *   **Interruption:** Generation stops, stop icon reverts to send.
*   **Error Handling:**
    *   **Network Errors:** Clear message ("Network error...") with retry option.
    *   **API/Backend Errors:** User-friendly message ("Sorry, something went wrong...") logged server-side. Specific errors from Gemini (e.g., content filtered, model error) should be relayed appropriately.
    *   **File Errors:** "File size too large (Max X MB/GB).", "Unsupported file type.", "Failed to upload/process file.", "Could not extract text from Word document."
    *   **Voice Errors:** "Microphone access denied.", "Could not transcribe audio.", "Recording failed.", "Microphone is disabled. Please enable the microphone."
    *   **Input Validation:** Handle empty input (disable send if no text and no file). Handle potential issues from Gemini API (e.g., prompt too long after file processing).
    *   **Display Location:** Input-related errors near the input bar. General/API errors as AI messages or prominent toasts.

**5. Accessibility (A11y)**

*   **Semantic HTML:** Use `<nav>`, `<main>`, `<aside>`, `<button>`, `<input>`, `textarea`, headings appropriately.
*   **Keyboard Navigation:** All interactive elements focusable and operable via keyboard. Logical tab order. Enter/Space activate buttons.
*   **Focus Management:** Set initial focus on text input. Manage focus during interactions (e.g., sidebar toggle, modals). Return focus appropriately.
*   **Screen Reader Support:** ARIA attributes (`aria-label`, `aria-live`, `aria-hidden`). Announce messages correctly ("User: [message]", "AI: [message]"). Ensure KaTeX output is accessible. Announce loading/error states.
*   **Color Contrast:** Meet WCAG AA ratios in both light/dark modes.
*   **Resizable Text:** UI reflows gracefully up to 200% zoom without loss of content or functionality.
*   **Forms:** Associate labels with inputs (can be visually hidden if redundant).

**6. Technology Stack**

*   **Frontend:**
    *   **Framework:** **React (with TypeScript)**
    *   **Styling:** **Tailwind CSS**
    *   **State Management:** **Zustand**
    *   **Math Rendering:** **KaTeX** library
    *   **Icons:** Heroicons or Feather Icons
    *   **API Communication:**
        *   **Standard Requests:** **`fetch` API** (native, modern, sufficient). 
        *   **Streaming Responses:** **Server-Sent Events (SSE)** is the recommended approach for unidirectional streaming from the backend. Implement the client-side using the **`fetch` API** with Readable Streams.
    *   **Voice Input:** **`react-speech-recognition`** library.
*   **Backend:**
    *   **Language/Framework:** **Python / FastAPI**
    *   **AI Model Integration:** **`google-genai` Python SDK**
    *   **Core LLM:** **Google Gemini `gemini-2.5-flash-preview-04-17`** (Leverage its text, math reasoning, multimodal PDF/image analysis, long context, and "thinking" capabilities).
        *   Use `client.models.generate_content` or `client.models.generate_content_stream`.
        *   Utilize `system_instruction` within `GenerateContentConfig` to set the math chatbot persona.
        *   Let the model use its default `thinkingBudget`.
    *   **Speech-to-Text:** **OpenAI Whisper API** (Requires separate API key and integration). Hugging face API and URL endpoint.
    *   **File Processing:**
        *   **PDF/Images:** Handled directly by Gemini `gemini-2.5-flash-preview-04-17` model via multimodal input (`types.Part.from_bytes` or Files API).
        *   **Text (`.txt`):** Read file content on the backend, pass text content to Gemini.
        *   **Word (`.docx`):** **Backend pre-processing required.** Use a Python library (e.g., **`python-docx`**) to extract text content from the `.docx` file. Pass the extracted text to Gemini. Handle potential errors during extraction.
    *   **Database:** **SQLite** (Simple, file-based, suitable for standalone/no scalability focus). Store chat sessions and messages.
    *   **File Storage:**
        *   **Small Files (< 20MB approx):** Pass data directly inline to Gemini API using `types.Part.from_bytes(data=..., mime_type=...)`.
        *   **Large Files (> 20MB up to 2GB):** Use the **Gemini Files API** (`client.files.upload`).
            *   Upload the file using `client.files.upload`.
            *   Pass the returned `File` object (or its `uri`) in the `contents` list to `generate_content`.
            *   **Be mindful of the 48-hour TTL.** Files uploaded via the API are automatically deleted after 48 hours. This application will *not* have persistent long-term storage for uploaded files unless this is changed.
    *   **Task Queue:** **No Task Queue.** API calls will be synchronous. Long-running Gemini requests might lead to frontend timeouts if not handled carefully (e.g., increased timeout settings, keeping the connection alive for SSE).
*   **Deployment:**
    *   **Containerization:** **Docker & Docker Compose** for packaging the frontend and backend.
    *   **Platform:** **None specified** (Assumes local running via Docker Compose or user will choose deployment platform later).

**Other Considerations:**

*   **Security:** Sanitize *all* inputs (text, file content, transcribed voice). Protect against prompt injection on the backend. Securely store/manage API keys (Gemini, Whisper) using environment variables or secrets management. Validate file types, sizes, and potentially scan uploads server-side if feasible. Implement basic rate limiting on the FastAPI backend.
*   **Scalability:** **Not a primary focus.** SQLite and synchronous processing are limitations for high concurrency.
*   **Cost:** **Not a primary focus.** API calls to Gemini and Whisper will incur costs. No specific optimizations requested.
*   **Authentication:** **None implemented.** Chat history is tied to the SQLite DB if run locally/persistently. History won't sync across devices.
*   **Testing:** Implement unit, integration, and end-to-end tests, especially for the core chat logic, API interactions, and different input types. Implement unit tests (especially for backend logic like file processing, API interaction), integration tests (frontend-backend communication), and end-to-end tests (simulating user flows like text query, file upload query, voice query).
