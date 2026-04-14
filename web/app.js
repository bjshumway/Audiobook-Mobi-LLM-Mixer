/**
 * Audio-Sync Book Reader - Frontend Application Logic
 *
 * This file orchestrates the entire frontend experience,
 * managing UI, audio playback, data synchronization, and
 * communication with the Flask backend.
 *
 * The code is structured into logical modules (objects)
 * for better organization and maintainability.
 */
 
// --- 1. State Management ---
const StateManager = {
    selectedBookId: null,
    isMobile: false, // Will be detected on init
    currentBookData: null,
    currentParagraphIdx: 0,
    currentPage: 0,
    currentAudioTime: 0,
    playbackRate: 1.0,

    init: function() {
        // Detect if running on mobile
        this.isMobile = /Mobi|Android/i.test(navigator.userAgent);
        console.log(`Device detected as mobile: ${this.isMobile}`);

        // Load any persisted state (e.g., last selected book)
        const savedState = JSON.parse(localStorage.getItem('audioSyncReaderState')) || {};
        this.selectedBookId = savedState.selectedBookId || null;
        this.playbackRate = savedState.playbackRate || 1.0;
        // More state can be loaded here as features are added
    },

    saveState: function() {
        const stateToSave = {
            selectedBookId: this.selectedBookId,
            playbackRate: this.playbackRate,
            // Save other essential state here
        };
        localStorage.setItem('audioSyncReaderState', JSON.stringify(stateToSave));
    },

    // Updates progress for the currently loaded book
    updateBookProgress: function() {
        if (this.currentBookData && this.selectedBookId) {
            const progress = {
                last_read_paragraph_idx: this.currentParagraphIdx,
                last_read_time_offset_seconds: this.currentAudioTime
            };
            API_Service.updateProgress(this.selectedBookId, progress)
                .then(() => console.log("Progress saved."))
                .catch(error => console.error("Error saving progress:", error));
        }
    }
};

// --- 2. API Service (stub for now) ---
const API_Service = {
    baseUrl: window.location.origin, // Assumes frontend is served from the same origin as Flask

    fetchBookList: async function() {
        // Placeholder for actual API call
        const response = await fetch(`${this.baseUrl}/api/books`);
        if (!response.ok) throw new Error('Failed to fetch book list');
        return response.json();
    },
    fetchBookData: async function(bookId) {
        // Placeholder for actual API call
        const response = await fetch(`${this.baseUrl}/api/books/${bookId}`);
        if (!response.ok) throw new Error(`Failed to fetch book data for ${bookId}`);
        return response.json();
    },
    updateProgress: async function(bookId, progressData) {
        // Placeholder for actual API call
        const response = await fetch(`${this.baseUrl}/api/books/${bookId}/progress`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(progressData)
        });
        if (!response.ok) throw new Error(`Failed to update progress for ${bookId}`);
        return response.json();
    },
    processBook: async function(bookId) {
        // Placeholder for actual API call
        const response = await fetch(`${this.baseUrl}/api/books/${bookId}/process`, {
            method: 'POST'
        });
        if (!response.ok) throw new Error(`Failed to initiate processing for ${bookId}`);
        return response.json();
    },
    exportLLMText: async function(bookId, selection) {
        // Placeholder for actual API call
        console.log(`Exporting text from ${bookId} for LLM:`, selection);
        return {status: "success", message: "Export placeholder complete"};
    },
    getAudioUrl: function(bookId) {
        return `${this.baseUrl}/books/${bookId}/${bookId}.mp3`;
    }
};

// --- 3. UI Manager (stub) ---
const UIManager = {
    // ... (Functions as defined in README.md)
    init: function() {
        // Placeholder: wire up basic event listeners
        document.getElementById('load-book-btn').addEventListener('click', () => {
            const bookId = document.getElementById('book-select-dropdown').value;
            if (bookId) {
                console.log(`Attempting to load book: ${bookId}`);
                // Call a function to load the book data and transition to reader view
            }
        });
    }
};

// --- 4. Audio Player Manager (stub) ---
const AudioPlayerManager = {
    // ... (Properties and Functions as defined in README.md)
    init: function() {
        // Create the audio element dynamically or reference an existing one
        this.audioElement = new Audio();
        this.audioElement.playbackRate = StateManager.playbackRate;
        // Wire up event listeners for timeupdate, ended, etc.
    }
};

// --- 5. Book Reader Manager (stub) ---
const BookReaderManager = {
    // ... (Properties and Functions as defined in README.md)
};

// --- 6. Sync Engine (stub) ---
const SyncEngine = {
    // ... (Functions as defined in README.md)
};

// --- Initialize Application ---
document.addEventListener('DOMContentLoaded', () => {
    StateManager.init();
    UIManager.init();
    AudioPlayerManager.init();
    // Initial rendering based on state or fetching book list
    console.log("Frontend loaded.");
});