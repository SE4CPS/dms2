// Setup IndexedDB 
function setupIndexedDB(dbName, itemStoreName, onComplete) {
    let request = indexedDB.open(dbName, 1);

    request.onupgradeneeded = function (event) {
        let db = event.target.result;

        if (!db.objectStoreNames.contains(itemStoreName)) {
            let itemStore = db.createObjectStore(itemStoreName, { keyPath: "id" });
        }
    };

    request.onsuccess = function (event) {
        let db = event.target.result;
        console.log("Database setup successful");
        onComplete(db);
    };

    request.onerror = function (event) {
        console.error("Error opening IndexedDB:", event.target.error);
    };
}

// Add objects in batches
function add100kObjects(db, itemStoreName, onComplete) {
    const batchSize = 10000;
    let currentBatch = 0;

    function addBatch() {
        if (currentBatch >= 100000) {
            onComplete();
            return;
        }

        let transaction = db.transaction(itemStoreName, "readwrite");
        let itemStore = transaction.objectStore(itemStoreName);

        transaction.oncomplete = function () {
            console.log(`Batch ${currentBatch / batchSize + 1} added successfully.`);
            currentBatch += batchSize;
            addBatch();
        };

        transaction.onerror = function (event) {
            console.error("Transaction failed:", event.target.error);
        };

        try {
            for (let i = currentBatch; i < currentBatch + batchSize && i < 100000; i++) {
                let status = i < 1000 ? "completed" : "in progress";
                let object = { 
                    id: i,
                    task: `Task_${i}`, 
                    status: status, 
                    dueDate: `2024-09-${(i % 30) + 1}` 
                };
                let addRequest = itemStore.add(object);

                addRequest.onerror = function (event) {
                    console.error(`Error adding object with id ${i}:`, event.target.error); 
                };
            }
        } catch (err) {
            console.error("Unexpected error during object insertion:", err);
        }
    }

    addBatch();
}

// Read all COMPLETED tasks and measure time
function readCompletedTasks(db, itemStoreName) {
    let transaction = db.transaction(itemStoreName, "readonly");
    let itemStore = transaction.objectStore(itemStoreName);
    let request = itemStore.openCursor();
    let startTime = performance.now();
    let completedTasks = 0;

    request.onsuccess = function (event) {
        let cursor = event.target.result;
        if (cursor) {
            if (cursor.value.status === "completed") {
                completedTasks++;
            }
            cursor.continue();
        } else {
            let endTime = performance.now();
            console.log(`Read ${completedTasks} completed tasks in ${(endTime - startTime).toFixed(2)} ms.`);
        }
    };

    request.onerror = function (event) {
        console.error("Error reading completed tasks:", event.target.error);
    };
}

// Call the functions to set up the DB and read completed tasks
setupIndexedDB("TodoDB", "TodoList", function (db) {
    add100kObjects(db, "TodoList", function () {
        readCompletedTasks(db, "TodoList");
    });
});
