// app.js

const dbName = "MyDatabase";
const storeName = "MyObjectStore";
let db;
let isGenerating = false; // Flag to prevent multiple generations

// Open (or create) the database with version 2
const request = indexedDB.open(dbName, 2);

request.onerror = (event) => {
    console.error("Database error: ", event.target.errorCode);
};

request.onupgradeneeded = (event) => {
    db = event.target.result;
    const objectStore = db.createObjectStore(storeName, { keyPath: "uuid" });
    objectStore.createIndex("source", "source", { unique: false });
    objectStore.createIndex("createdAt", "createdAt", { unique: false });
    objectStore.createIndex("updatedAt", "updatedAt", { unique: false });
    objectStore.createIndex("attribute1", "attribute1", { unique: false });
    objectStore.createIndex("attribute2", "attribute2", { unique: false });
    objectStore.createIndex("attribute3", "attribute3", { unique: false });
};

request.onsuccess = (event) => {
    db = event.target.result;
    console.log("Database initialized");
    document.getElementById("generate").addEventListener("click", () => {
        // Prevent multiple generations
        if (isGenerating) return;
        isGenerating = true; // Set flag to true
        generateAndStoreObjects(1000);
    });
};

function generateAndStoreObjects(count) {
    // Disable the button to prevent multiple clicks
    document.getElementById("generate").disabled = true;

    // Clear existing entries before generating new ones
    const transaction = db.transaction([storeName], "readwrite");
    const objectStore = transaction.objectStore(storeName);

    // Clear the object store if you want to start fresh
    const clearRequest = objectStore.clear();
    clearRequest.onsuccess = () => {
        console.log("Existing entries cleared.");
        let entriesAdded = 0; // Counter for entries added

        // Generate and add new entries
        for (let i = 0; i < count; i++) {
            const object = {
                uuid: generateUUID(),
                source: "IndexedDB",
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                attribute1: `Attribute 1 Value ${i}`,
                attribute2: `Attribute 2 Value ${i}`,
                attribute3: `Attribute 3 Value ${i}`
            };

            const addRequest = objectStore.add(object);
            addRequest.onsuccess = () => {
                entriesAdded++;
                // Check if we've added all entries
                if (entriesAdded === count) {
                    document.getElementById("result").innerText = "1000 objects generated and stored in IndexedDB.";
                    console.log("All objects have been added to the database.");
                    // Re-enable the button and reset flag
                    document.getElementById("generate").disabled = false;
                    isGenerating = false; // Reset flag after completion
                }
            };
            addRequest.onerror = (event) => {
                console.error("Error adding object: ", event.target.error);
                // Still re-enable button in case of errors
                document.getElementById("generate").disabled = false;
                isGenerating = false; // Reset flag on error
            };
        }
    };

    transaction.onerror = (event) => {
        console.error("Transaction error: ", event.target.error);
        // Re-enable the button if there is an error
        document.getElementById("generate").disabled = false;
        isGenerating = false; // Reset flag on error
    };
}

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}