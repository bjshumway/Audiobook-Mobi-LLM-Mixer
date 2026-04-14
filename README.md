# Audio-Sync Book Reader

This project aims to create a personalized tool that synchronizes an audiobook (MP3) with its corresponding e-book (MOBI), allowing for a seamless reading and listening experience. It will extract text from MOBI files, process audio using Speech-to-Text (STT) to generate word-level timestamps, align the book text with these timestamps, and provide a local web interface for synchronized playback. Additionally, it will feature an export function to grab text snippets for use with LLMs.

This tool is designed for personal use and local-first development.

## Features

- **MOBI to Text Conversion**: Extracts plain text from e-book files.
- **Speech-to-Text with Timestamps**: Transcribes audio files, generating word-level start and end times.
- **Fuzzy Text Alignment**: Synchronizes the extracted book text with the transcribed audio, even with minor discrepancies.


C:\Users\Asher\Audiobook-Mobi-LLM-Mixer
├── books/
│   ├── book_a/
│   │   ├── book_a.mobi          # Original MOBI file
│   │   ├── book_a.mp3           # Original MP3 audiobook
│   │   ├── book_a.json          # Processed data (text, timestamps, metadata)
│   │   └── book_a_export.txt    # Exported text snippets
│   ├── book_b/
│   │   ├── book_b.mobi
│   │   ├── book_b.mp3
│   │   └── book_b.json
│   └── ...
├── scripts/
│   ├── process_book.py          # Main script to process MOBI, MP3, STT, alignment
│   ├── mobi_parser.py           # Helper for MOBI to text conversion
│   ├── stt_processor.py         # Helper for Speech-to-Text
│   └── text_aligner.py          # Helper for text alignment
├── web/
│   ├── index.html               # Frontend HTML
│   ├── style.css                # Frontend CSS
│   ├── app.js                   # Frontend JavaScript (player, synching, export)
│   └── server.py                # Simple local Flask/FastAPI server to serve files and data
├── config.py                    # Configuration for API keys (if needed) and paths
├── requirements.txt             # Python dependencies
└── README.md

- **MOBI to Text Conversion**: Extracts plain text from e-book files.
- **Speech-to-Text with Timestamps**: Transcribes audio files, generating word-level start and end times.
- **Fuzzy Text Alignment**: Synchronizes the extracted book text with the transcribed audio, even with minor discrepancies.

## Updates to File System over Time:
* config.py: A new file is introduced to store global configurations, specifically paths to various directories. This makes the project more organized and easier to configure.
Imports: Necessary Flask components, os for path manipulation, json for reading/writing data, and subprocess for running the processing script are imported. CORS is also imported and initialized to allow the frontend to communicate with the backend.
Helper Functions: get_book_path, get_book_json_path, etc., are defined to simplify path construction, making the routes cleaner.
Static File Serving (/, /<path:filename>):
The root route / serves index.html.
The generic /<path:filename> route serves other static assets like style.css and app.js from the web directory.
API Endpoints (/api/books/*):
/api/books (GET): Scans the books/ directory, checks for processed JSON files, and constructs a list of book metadata. It attempts to read title/







## Kickoff Discussion
Here are some specific questions to guide our discussion:

Book Selection and Management:

How should a user initially load or select a book from their books/ directory into the web interface? Will there be a simple dropdown, a list of available books, or some other mechanism?
Should there be any visual cues about which books have been processed (i.e., have an associated .json file)?
Text Display and Reading Experience:

How should the book's text be displayed? As a continuous scrolling page, or should it be paginated like a traditional e-reader?
What level of text granularity should be highlighted during audio playback (e.g., the current word, sentence, or paragraph)?
What visual style should the highlighting take (e.g., background color, underline, bolder text, change of text color)?
Should users be able to adjust font size, line height, or switch between light/dark mode?
Audio Playback Controls:

What standard audio controls do you need? (e.g., play/pause button, a seek bar/progress slider, volume control, playback speed options like 0.75x, 1x, 1.25x, 1.5x, 2x).
Should there be quick skip buttons (e.g., skip forward/backward 10-15 seconds)?
Synchronization Interaction:

When the audio is playing, how should the text automatically follow? Should it scroll smoothly, or jump to the relevant section?
If a user taps/clicks on a specific sentence or paragraph in the displayed text, should the audio automatically jump to that corresponding point?
Conversely, if the user manually seeks the audio (e.g., drags the seek bar), should the text automatically update to highlight the new position?
Navigation within the Book:

How should users navigate between different sections or chapters of the book? A table of contents, previous/next buttons?
Should there be a way to quickly jump to a specific time in the audio or a specific page/percentage of the text?
Export Context Feature (for LLMs):

How will a user select the specific "amount/section" of text they want to export? Will it be by selecting sentences/paragraphs with a mouse/finger, by defining a start and end point, or simply exporting the currently highlighted segment?
What kind of UI element should trigger the export action (e.g., a button, a context menu)?
Mobile (iPhone) Specifics:

Are there any particular design patterns or mobile-first considerations that are important for the iPhone experience (e.g., touch-friendly controls, full-screen reading mode, gestures)?
How should the audio controls be integrated into the mobile layout, especially considering screen real estate?
Overall Aesthetic / Look and Feel:

Do you have any general preferences for the design language? For example, clean and minimalist, modern, academic, a specific color scheme, etc.?
Your answers to these questions will be invaluable in crafting a robust technical design that truly reflects your vision for this personal tool!

Context Sources (5)

Ben Shumway
The index.html (perhaps by talking to the server) will detect whether this is running on the PC or in the cloud (over phone). If running on PC it will know to provide additional options... namely options for file management like doing those conversions with the python script. But at any rate... regardless of whether you are on phone dealing with cloud or on computer... it will allow you to pick a book simply by looking at the directory and providing a dropdown menu. After picking the book... you will have access to button to open either the Mobi or the mp3. If you open the mobi it continues where you left off. If you open the mp3 it also continues where you left off. So it always remembers the last page you read (or listened up to). Yes there would be a visual cue if a book hasn't been processed yet (ie have an associated .json file) and a button called "Process Book". There would also be a button called "Copy to TXT for LLM".

Paginated like a traditional e-reader. In dark-mode so its easier on the eyes.

During playback, highlight simply the paragraph. This is the easiest because the words can differ from the playbook vs the book... and the goal isn't to align them word-for-word... or even sentence-to-sentence... but rather to align them paragraph to paragraph... with an understanding that occasionally the mp3 will add its own paragraphs like "You're listening to blah blah blah read by blah blah blah" (or any number of variations kind of like that)... which the python script has to learn is basically its own mp3-specific paragraph and consider it lumped inbetween two real paragraphs in the book.

Highligh just with background color. Nothing else

User should be able to adjust font size, line height. User shouldn't have to switch to light or dark mode. it should always be dark mode.

Yes all of those controls Yes there should be quick skip buttons... but it should be based on paragraphs not seconds. So skipping forward skips forward one paragraph. Backwards skips backward one paragraph. Massive-skip would go 10 forward, massive skip back 10 backward.

Jump to the relevant section Yes - if the audio is playing and the user taps or clicks on a specific paragraph the audio should jump to that corresponding point. Yes - the converse is also true

A table of contents... if provided in the book... should allow users to jump around like a normal mobi. If not provided in ignore it. Previous/next page buttons also provided.

The export action would be tucked under an "extra actions" button that contains other things like "close book" or "jumpt to chapter" so these less commonly used actions are all tucked away together

Since this project is built entirely for me as a hobby project... there is no need to think about it working for an android phone... so any design patterns that iphones appreciate are also appreciated in this project. 95% of the time the reading/listening will be on the iphone so optimize for that (on the computer the UI just hsa to work doesn't have to look great)... while the computer will handle more the processing side of things (adding books; processing them)

clean and minimalist; gray slate (a version of dark mode).

OK...Take a moment to absorb this. if you have followup questions let me know. Otherwise wait for my prompt and then we will do that writeup I mentioned earlier.


Gemini
Understood! I've absorbed all those details regarding the UI and user experience for your Audio-Sync Book Reader project. It sounds like a well-thought-out plan, with a clear focus on a seamless, personalized reading and listening experience, especially optimized for iPhone usage in dark mode.

The key points I've noted include:

Adaptive UI: The index.html distinguishing between PC and phone for displaying file management options.
Intuitive Book Selection: A dropdown based on the books/ directory, clear visual cues for processed/unprocessed books, and dedicated "Process Book" and "Copy to TXT for LLM" buttons.
Persistent Progress: Always remembering the last reading/listening position.
E-reader Like Text Display: Paginated layout, always dark mode (gray slate, clean, minimalist), and adjustable font size/line height.
Paragraph-Level Synchronization: Highlighting only the current paragraph with a background color, with the critical capability for the Python script to handle audio-specific filler content.
Comprehensive Audio Controls: Standard play/pause, seek, volume, speed, along with paragraph-based skip (single and "massive" 10-paragraph jumps).
Bidirectional Sync: Tapping text jumps audio, seeking audio jumps text (both to paragraph start).
Table of Contents: Utilization of MOBI's internal TOC if available, plus page navigation.
Tucked-Away Actions: "Extra Actions" button for less frequent actions like "Copy to TXT for LLM", "Close Book", "Jump to Chapter".
iPhone-First Design: Prioritizing touch-friendly, full-screen, and generally iPhone-appreciated patterns for the web UI.
This comprehensive set of requirements provides an excellent foundation for designing the architecture and individual components.

## Technical Design

This section details the architectural and component-level design of the Audio-Sync Book Reader. The goal is to provide a comprehensive guide for implementation, ensuring that each piece of the system works together to deliver the desired synchronized reading and listening experience.

### 1. High-Level Architecture

The project follows a client-server architecture, primarily designed for local execution but with a web-based frontend for accessibility across devices (especially iPhone).

*   **Backend (Python - `web/server.py`)**: A lightweight Python Flask server acts as the central hub. It's responsible for:
    *   Serving the static frontend files (`index.html`, `app.js`, `style.css`).
    *   Providing API endpoints for managing books (listing, processing, retrieving processed data).
    *   Triggering the core book processing pipeline (`scripts/process_book.py`).
    *   Managing book metadata and user progress (last read position).
*   **Processing Core (Python - `scripts/`)**: A set of Python scripts that handle the heavy lifting of book and audio processing:
    *   `mobi_parser.py`: Extracts text from MOBI files.
    *   `stt_processor.py`: Interfaces with Google Cloud Speech-to-Text to get transcriptions with word-level timestamps.
    *   `text_aligner.py`: Aligns the MOBI text (paragraph-by-paragraph) with the STT output.
    *   `process_book.py`: Orchestrates the calls to these individual scripts and saves the final processed data.
*   **Data Storage (`books/<book_id>/book_id.json`)**: Processed book data (aligned text, timestamps, metadata, progress) is stored locally as JSON files within the `books/` directory. This JSON file is the single source of truth for the synchronized experience.
*   **Frontend (HTML, CSS, JavaScript - `web/`)**: A Single-Page Application (SPA) built with vanilla JavaScript. It runs in the user's web browser (desktop or mobile) and communicates with the local Flask server via AJAX requests. It handles:
    *   Displaying the book selection interface.
    *   Rendering the paginated book text in dark mode.
    *   Implementing the audio player with custom controls.
    *   Managing the synchronization logic (highlighting paragraphs, scrolling).
    *   Handling user interactions (tapping text, skipping paragraphs, exporting text).

```mermaid
graph TD
    A[User's Browser (iPhone/Desktop)] -- HTTP/HTTPS --> B(Flask Server: web/server.py)
    B -- Serves Static Files --> A
    B -- API Calls --> C[Processing Scripts (scripts/)]
    C -- Reads MOBI/MP3 --> D[books/<book_id>/*.mobi/*.mp3]
    C -- Writes Processed JSON --> E[books/<book_id>/<book_id>.json]
    B -- Reads/Writes JSON --> E
    A -- Displays Data & Controls --> E
```

### 2. Data Model (`books/<book_id>/<book_id>.json`)

The core of the synchronized experience relies on a well-structured JSON file for each processed book. This file will store all the necessary information to drive the frontend.

**File Path**: `books/<book_id>/<book_id>.json`

**Example Structure**:

```json
{
  "metadata": {
    "id": "unique_book_identifier_from_filename",
    "title": "The Hitchhiker's Guide to the Galaxy",
    "author": "Douglas Adams",
    "mobi_file": "book_id.mobi",
    "mp3_file": "book_id.mp3",
    "processing_date": "YYYY-MM-DDTHH:MM:SSZ",
    "page_count": 42,
    "total_audio_duration_seconds": 12345.67
  },
  "progress": {
    "last_read_paragraph_idx": 25,
    "last_read_time_offset_seconds": 123.45
  },
  "table_of_contents": [
    {
      "title": "Chapter 1",
      "paragraph_idx": 0,
      "audio_start_time_seconds": 0.0
    },
    {
      "title": "Chapter 2",
      "paragraph_idx": 50,
      "audio_start_time_seconds": 1200.5
    }
  ],
  "pages": [
    {
      "page_number": 1,
      "paragraph_start_idx": 0,
      "paragraph_end_idx": 4,
      "approx_audio_start_time_seconds": 0.0,
      "approx_audio_end_time_seconds": 60.0
    },
    // ...
  ],
  "paragraphs": [
    {
      "id": "p0",
      "mobi_text": "This is the first paragraph of the book.",
      "stt_text_raw": "This is the first paragraph of the book.", // Raw STT for reference/debugging
      "start_time_seconds": 0.0,
      "end_time_seconds": 5.2,
      "words": [ // Optional: Store word-level timestamps for finer-grained future features if needed.
        {"word": "This", "start": 0.0, "end": 0.3},
        {"word": "is", "start": 0.3, "end": 0.4},
        // ...
      ],
      "is_filler": false // True if this is an audio-only, non-book content (e.g., "You're listening to...")
    },
    {
      "id": "p1",
      "mobi_text": "And this is the second paragraph, continuing the story.",
      "stt_text_raw": "And this is the second paragraph, continuing the story.",
      "start_time_seconds": 5.5,
      "end_time_seconds": 12.8,
      "words": [],
      "is_filler": false
    },
    {
      "id": "p2",
      "mobi_text": null, // Indicates this paragraph was not found in the MOBI text
      "stt_text_raw": "You're listening to the Audio-Sync Reader.",
      "start_time_seconds": 13.0,
      "end_time_seconds": 16.0,
      "words": [],
      "is_filler": true // Explicitly mark audio-only content
    },
    // ...
  ]
}
```

**Key fields in `paragraphs` array**:
*   `id`: A unique identifier for the paragraph (e.g., `p0`, `p1`). This will be used by the frontend for targeting and highlighting.
*   `mobi_text`: The clean, original paragraph text extracted from the MOBI file. This is the text displayed to the user. `null` if the paragraph is audio-only filler.
*   `stt_text_raw`: The raw transcription from Google STT for this paragraph's duration. Useful for debugging and potential re-alignment.
*   `start_time_seconds`, `end_time_seconds`: The aligned start and end timestamps in the audio for this paragraph.
*   `words`: (Optional, but recommended for futureproofing) An array of word objects with `word`, `start`, and `end` times. This allows for finer-grained highlighting if the design evolves beyond paragraph-level, or for more precise selection for LLM export.
*   `is_filler`: A boolean flag indicating if this paragraph is audio-only content (e.g., narrator intros, chapter announcements that are not part of the actual book text). This is crucial for filtering during display and alignment.

**Key fields in `pages` array**:
*   `page_number`: The sequential page number.
*   `paragraph_start_idx`, `paragraph_end_idx`: The start and end indices (inclusive) of the `paragraphs` array that belong to this page. This enables pagination.
*   `approx_audio_start_time_seconds`, `approx_audio_end_time_seconds`: Approximate audio range for the entire page, useful for initial jumps.

**Handling "Audio-Specific Filler"**:
The `is_filler: true` flag in the `paragraphs` array is our solution for handling content like "You're listening to..." The `text_aligner.py` script will be responsible for identifying these segments. This can be done by:
1.  Checking if an STT-transcribed segment has *no* strong fuzzy match with any MOBI paragraph (i.e., `mobi_text` would be `null`).
2.  Potentially using a predefined list of common audiobook filler phrases to explicitly tag STT segments as `is_filler`.
The frontend will then skip displaying these `is_filler` paragraphs in the main reading view but can still use their audio timestamps for smooth playback.

---

This covers the fundamental architecture and the detailed structure of our processed data. The data model is designed to support all the UI requirements we discussed, from pagination and progress tracking to paragraph-level synchronization and the identification of filler content.

### 3. Backend (`web/server.py`)

The Flask server (`web/server.py`) serves as the API layer and static file server for the application. It orchestrates interactions between the frontend and the backend processing scripts, and manages persistent user progress.

**Key Responsibilities:**

*   **Static File Serving**: Delivers `index.html`, `style.css`, `app.js`, and any other static assets (like audio files from `books/` directories) to the client's browser.
*   **Book Management**: Handles listing available books, fetching their processed data, and saving user progress.
*   **Processing Orchestration**: Triggers the Python processing scripts (`scripts/*.py`) for new books or reprocessing requests.
*   **File Operations**: Manages reading and writing of `.json` files (processed data) and `.txt` files (LLM export) within the `books/` directory.
*   **Cross-Origin Resource Sharing (CORS)**: Configured to allow requests from the local frontend, especially important if running on different ports during development or if accessing from a mobile device on the local network.

**API Endpoints:**

All API endpoints will return JSON responses.

1.  **`/` (GET)**
    *   **Purpose**: Serves the main `index.html` page, which is the entry point for the frontend SPA.
    *   **Response**: `index.html` content.

2.  **`/<path:filename>` (GET)**
    *   **Purpose**: Serves static files such as CSS, JavaScript, and potentially audio files from within the `web/` directory. Audio files from `books/` will be handled by a dedicated endpoint.
    *   **Parameters**: `filename` (path to the static asset).
    *   **Response**: The requested static file.

3.  **`/api/books` (GET)**
    *   **Purpose**: Lists all available book directories within the `books/` folder. For each book, it indicates if a processed `.json` file exists (meaning it's ready to be read).
    *   **Response**: `application/json`
        ```json
        [
          { "id": "book_a", "title": "Book A Title", "processed": true, "author": "Author A" },
          { "id": "book_b", "title": "Book B Title (Unprocessed)", "processed": false, "author": "Unknown" }
        ]
        ```
        *The `title` and `author` for unprocessed books will be inferred from the MOBI file if possible, otherwise marked as "Unknown".*

4.  **`/api/books/<book_id>` (GET)**
    *   **Purpose**: Retrieves the full processed JSON data for a specific book, including metadata, progress, TOC, pages, and paragraphs.
    *   **Parameters**: `book_id` (e.g., "the_hitchhikers_guide").
    *   **Response**: `application/json` (the full `book_id.json` structure as described in Section 2).
    *   **Error Handling**: Returns 404 if `book_id.json` does not exist.

5.  **`/api/books/<book_id>/progress` (POST)**
    *   **Purpose**: Updates the user's reading/listening progress for a given book.
    *   **Parameters**: `book_id`.
    *   **Request Body**: `application/json`
        ```json
        {
          "last_read_paragraph_idx": 25,
          "last_read_time_offset_seconds": 123.45
        }
        ```
    *   **Response**: `application/json` `{ "status": "success" }` or appropriate error.

6.  **`/api/books/<book_id>/process` (POST)**
    *   **Purpose**: Triggers the backend processing pipeline (`scripts/process_book.py`) for the specified book. This endpoint might take some time to respond.
    *   **Parameters**: `book_id`.
    *   **Response**: `application/json` `{ "status": "processing_started", "message": "Book processing initiated." }` or error.
    *   **Consideration**: For long-running tasks, a more advanced setup might involve background tasks (e.g., Celery) and a separate endpoint to poll for status, but for a local-first personal tool, a direct blocking call might be acceptable with appropriate frontend loading indicators.

7.  **`/api/books/<book_id>/export-llm` (POST)**
    *   **Purpose**: Exports a selected range of text from the book into a plain text file (`book_id_export.txt`) for LLM consumption.
    *   **Parameters**: `book_id`.
    *   **Request Body**: `application/json`
        ```json
        {
          "start_paragraph_id": "p10",
          "end_paragraph_id": "p20"
        }
        ```
        *The frontend will provide the `start_paragraph_id` and `end_paragraph_id` based on user selection.*
    *   **Response**: `application/json` `{ "status": "success", "file_path": "/books/book_a/book_a_export.txt" }` or error.

8.  **`/books/<book_id>/<filename>` (GET)**
    *   **Purpose**: Serves the actual `.mobi` and `.mp3` files (and potentially the processed `.json` file directly) from their respective book directories. This allows the frontend's `<audio>` tag to directly access the MP3.
    *   **Parameters**: `book_id`, `filename` (e.g., "book_a.mp3").
*   **Response**: The requested file. Flask's `send_from_directory` will be used here, ensuring correct MIME types.

---

### 4. Frontend (HTML, CSS, JavaScript - `web/`)

The frontend is a Single-Page Application (SPA) designed to provide a clean, minimalist, and highly functional interface, primarily optimized for iPhone use in dark mode. It communicates with the local Flask backend via asynchronous JavaScript (AJAX) calls to fetch data and save user progress.

**4.1. Structure and Core Components**

The frontend will consist of:

*   **`web/index.html`**: The main entry point, providing the basic page structure, linking to CSS and JavaScript files, and containing the root elements for the dynamic content.
*   **`web/style.css`**: Defines the visual aesthetics, layout, and responsiveness of the application. It will implement the requested dark mode (gray slate) theme and ensure a touch-friendly design.
*   **`web/app.js`**: The core JavaScript file containing all the application logic for UI rendering, event handling, audio playback, synchronization, and communication with the backend. It will be structured into several logical modules for maintainability.

**4.2. Key JavaScript Modules/Concerns (`web/app.js`)**

`app.js` will logically be divided to handle distinct aspects of the application:

1.  **`UI_Manager`**:
    *   **Responsibility**: Handles all DOM manipulations, rendering content, and managing the visibility of different UI sections (e.g., book selection screen vs. reader screen).
    *   **Functions**:
        *   `renderBookList(books)`: Displays the dropdown/list of available books.
        *   `renderReaderView(bookData)`: Renders the book text, controls, and sets up pagination.
        *   `updateParagraphHighlight(paragraphId)`: Applies/removes highlighting for the current active paragraph.
        *   `scrollToParagraph(paragraphId)`: Smoothly scrolls the view to the specified paragraph.
        *   `displayToast(message)`: Shows temporary feedback messages to the user.
        *   `showProcessingIndicator()`: Displays a loading spinner or message during book processing.
        *   `updateProgressBar(currentTime, totalDuration)`: Updates the audio seek bar.
        *   `updateControlsState(isPlaying)`: Enables/disables play/pause buttons, etc.
        *   `adjustFontSize(size)` / `adjustLineHeight(height)`: Updates CSS variables or classes.

2.  **`API_Service`**:
    *   **Responsibility**: Encapsulates all communication with the Flask backend.
    *   **Functions**:
        *   `fetchBookList()`: Calls `/api/books`.
        *   `fetchBookData(bookId)`: Calls `/api/books/<book_id>`.
        *   `updateProgress(bookId, progressData)`: Calls `/api/books/<book_id>/progress`.
        *   `processBook(bookId)`: Calls `/api/books/<book_id>/process`.
        *   `exportLLMText(bookId, selection)`: Calls `/api/books/<book_id>/export-llm`.
        *   `getAudioUrl(bookId)`: Constructs the direct URL for the MP3 file (`/books/<book_id>/<book_id>.mp3`).

3.  **`Audio_Player_Manager`**:
    *   **Responsibility**: Manages the `<audio>` HTML element, its playback state, and interactions with audio controls.
    *   **Properties**: `audioElement`, `currentBookId`, `isPlaying`, `playbackRate`.
    *   **Functions**:
        *   `loadAudio(bookId, startTime)`: Sets the `src` of the audio element and seeks to `startTime`.
        *   `play()` / `pause()`: Controls playback.
        *   `seek(timeInSeconds)`: Jumps to a specific point in the audio.
        *   `setPlaybackRate(rate)`: Changes playback speed.
        *   `skipParagraph(direction)`: Uses current paragraph's `start_time_seconds` and next/previous paragraph's `start_time_seconds` to seek.
        *   `skipMassive(direction)`: Jumps by 10 paragraphs.
        *   **Event Listeners**: For `timeupdate` (to drive text sync), `ended`, `play`, `pause`, `error`.

4.  **`Book_Reader_Manager`**:
    *   **Responsibility**: Manages the display of book text, pagination, and interaction with the displayed text.
    *   **Properties**: `currentBookData`, `currentPage`, `currentParagraphIdx`.
    *   **Functions**:
        *   `loadBook(bookData)`: Initializes the reader with processed book data, renders the first page, and seeks to last saved progress.
        *   `renderPage(pageNumber)`: Displays the paragraphs for the given page, hiding `is_filler` paragraphs.
        *   `goToNextPage()` / `goToPreviousPage()`: Navigates through pages.
        *   `getParagraphByTime(time)`: Finds the paragraph corresponding to a given audio time.
        *   `getParagraphById(id)`: Retrieves a paragraph object by its unique ID.
        *   **Event Listeners**: For clicks/taps on paragraphs (to trigger audio seek).

5.  **`Sync_Engine`**:
    *   **Responsibility**: The core logic for keeping audio and text synchronized.
    *   **Functions**:
        *   `startSyncLoop()`: Periodically checks `Audio_Player_Manager.currentTime` and calls `Book_Reader_Manager.getParagraphByTime()` to identify the current paragraph.
        *   `onAudioTimeUpdate(currentTime)`: Callback from `Audio_Player_Manager` that drives `UI_Manager.updateParagraphHighlight()` and `Book_Reader_Manager.scrollToParagraph()`.
        *   `onParagraphClick(paragraphId)`: Callback from `Book_Reader_Manager` that calls `Audio_Player_Manager.seek()` to the paragraph's start time.

6.  **`State_Manager`**:
    *   **Responsibility**: Manages the application's overall state (e.g., `selectedBookId`, `isMobile`, `currentFontSize`). Persists user preferences and progress locally (e.g., using `localStorage`).
    *   **Functions**: `loadState()`, `saveState()`, `updateProgress()`.

**4.3. UI Requirements Handling**

*   **Adaptive UI (PC vs. Phone)**:
    *   `index.html` will be minimal. `app.js` will detect `isMobile` (via user agent or screen width) and conditionally render UI elements or adjust layout.
    *   PC-specific file management options will be handled by the Flask server, which will only expose them if accessed from a non-mobile browser or identified as local access (though this distinction might be primarily backend-driven based on request headers/IP). The frontend will simply not display "Process Book" button if `isMobile` is true and a flag from the backend indicates remote access.
*   **Book Selection**:
    *   `UI_Manager` will render a `<select>` dropdown (or a styled list for mobile) populated by `API_Service.fetchBookList()`.
    *   Visual cues for processed books will be based on the `processed` flag in the API response.
    *   "Process Book" and "Copy to TXT for LLM" buttons will be available, conditionally visible based on `isMobile` and processing status.
*   **Persistent Progress**: `State_Manager` will load `last_read_paragraph_idx` and `last_read_time_offset_seconds` from the fetched `bookData.progress` and also save it back via `API_Service.updateProgress()` at regular intervals (e.g., every 5-10 seconds of playback or on pause/close).
*   **E-reader Like Text Display**:
    *   `UI_Manager` and `Book_Reader_Manager` will render paragraphs into pages based on the `bookData.pages` array, creating a paginated look.
    *   `style.css` will define a dark mode theme (gray slate) for the entire application.
    *   `UI_Manager` will provide controls for font size and line height adjustments, modifying CSS variables.
*   **Paragraph-Level Synchronization**:
    *   `Sync_Engine` will drive the highlighting. When `onAudioTimeUpdate` fires, it determines the current paragraph.
    *   `UI_Manager.updateParagraphHighlight()` will apply a background color to the active paragraph, removing it from the previous one.
    *   `Book_Reader_Manager.scrollToParagraph()` will ensure the current paragraph is visible, possibly scrolling the page automatically.
*   **Comprehensive Audio Controls**:
    *   `index.html` will contain buttons for play/pause, speed (e.g., 0.75x, 1x, 1.25x), volume, a progress slider, and paragraph skip buttons.
    *   `Audio_Player_Manager` will handle events from these controls and manage the underlying `<audio>` element.
    *   Paragraph skip buttons will use `Book_Reader_Manager` to find the target paragraph's start time and instruct `Audio_Player_Manager` to seek.
*   **Bidirectional Sync**:
    *   Tapping a paragraph (`Book_Reader_Manager` event listener) will call `Audio_Player_Manager.seek()` to that paragraph's start time.
    *   Seeking the audio (`Audio_Player_Manager` `timeupdate` event) will automatically trigger `Sync_Engine` to update the highlighted text and scroll the view.
*   **Navigation within the Book**:
    *   Table of Contents: `UI_Manager` will render a TOC (if present in `bookData.table_of_contents`) as a clickable list, using `Book_Reader_Manager.loadPage()` and `Audio_Player_Manager.seek()` to jump to the selected chapter.
    *   Previous/Next Page buttons: `UI_Manager` will expose these, calling `Book_Reader_Manager.goToNextPage()` / `goToPreviousPage()`.
*   **Export Context Feature**:
    *   An "Extra Actions" button (dropdown/modal) in `UI_Manager` will contain "Copy to TXT for LLM."
    *   Upon clicking, the frontend will need a mechanism to select a range of paragraphs. This could be a click-and-drag selection, or (simpler for V1) defaulting to the currently visible page's text, or explicitly defining start/end paragraph IDs via a modal.
    *   The selected text (or paragraph IDs) will be sent to `API_Service.exportLLMText()`.
*   **Mobile (iPhone) Specifics**:
    *   `style.css` will use media queries and flexible box/grid layouts to ensure responsiveness and touch-friendly sizing of elements.
    *   Audio controls will be prominent but designed to not obstruct reading too much, potentially collapsing into a smaller bar or appearing on demand.
    *   Full-screen mode considerations will be built into the `UI_Manager` (e.g., hiding header/footer).
    *   Gestures for page turning (swipe) could be a future enhancement, but initial pagination buttons will suffice.

**4.4. Frontend (PC) Specifics**:
*   The main difference for the PC frontend will be the presence of additional UI elements for file management (uploading new MOBI/MP3 pairs) and the "Process Book" button, which will trigger `API_Service.processBook()`. The backend will provide an indicator if the request is from a desktop browser via the API.
*   The UI will adapt to larger screen real estate, potentially displaying more controls or a different layout, but maintaining the dark mode aesthetic.

---
```

### Explanation of the Additions:

This extensive addition to the `README.md` details the Frontend (`web/`) component, addressing all your specified UI requirements:

*   **Structure and Core Components**: Clearly defines the role of `index.html`, `style.css`, and `app.js`.
*   **Key JavaScript Modules/Concerns (`web/app.js`)**: Breaks down the `app.js` file into logical, conceptual modules (`UI_Manager`, `API_Service`, `Audio_Player_Manager`, `Book_Reader_Manager`, `Sync_Engine`, `State_Manager`). This promotes modularity, testability, and clarity, making it easier for future prompts to focus on specific parts. Each module's responsibilities and key functions are outlined.
*   **UI Requirements Handling**: This section directly maps your desired features (book selection, dark mode, paragraph highlighting, audio controls, bidirectional sync, navigation, LLM export, mobile specifics, etc.) to how they will be implemented within the frontend structure and the aforementioned JavaScript modules.
*   **Handling "Audio-Specific Filler"**: Reaffirms that filler paragraphs (`is_filler: true`) will be hidden from the main reading view but their timestamps will still contribute to smooth audio playback.
*   **PC vs. Mobile Differences**: Explicitly outlines how the UI will adapt based on the detected device, primarily impacting the visibility of file management options.

This provides a very solid foundation for building out the frontend. The next logical steps would be to start implementing these backend and frontend components.

---

