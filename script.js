/*
What this program does:
Step 0: Set up IndexedDB & Add 100,000 objects in batches of 10,000
Step 1: Set 1,000 objects to status "Completed"
Step 2: Measure the time to read all objects with status set to "Completed"
Step 3: Same as step 2 but with Read-Only flag
*/

// STEP 0: Setup IndexedDB
function setupIndexedDB(dbName, itemStoreName, onComplete) {
    let request = indexedDB.open(dbName, 1);

    request.onupgradeneeded = function (event) {
        let db = event.target.result;
        // Create an object store if it doesn't exist
        if (!db.objectStoreNames.contains(itemStoreName)) {
            let itemStore = db.createObjectStore(itemStoreName, { keyPath: "id" });
        }
    };
    // If database is opened successfully
    request.onsuccess = function (event) {
        let db = event.target.result;
        console.log("IndexedDB setup successful!");
        onComplete(db);
    };
    // If database fails to open
    request.onerror = function (event) {
        console.error("Error opening IndexedDB:", event.target.error);
    };
}

// STEP 0: Add 100,000 objects in batches of 10,000
function add100kObjects(db, itemStoreName, onComplete) {
    const batchSize = 10000;
    let currentBatch = 0;

    // Recursive function to add objects
    function addBatch() {
        if (currentBatch >= 100000) {
            onComplete();
            return;
        }
        // Create a new transaction in readwrite mode
        let transaction = db.transaction(itemStoreName, "readwrite");
        let itemStore = transaction.objectStore(itemStoreName);
        // If transaction is successful
        transaction.oncomplete = function () {
            console.log(`Batch ${currentBatch / batchSize + 1} added successfully.`);
            currentBatch += batchSize;
            addBatch();
        };
        // If transaction fails
        transaction.onerror = function (event) {
            console.error("Transaction failed:", event.target.error);
        };

        try {
            // Add a batch
            for (let i = currentBatch; i < currentBatch + batchSize && i < 100000; i++) {
                // STEP 1: Set 1000 objects to status "Completed"
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

// STEP 2: Read all COMPLETED tasks and measure time
function readCompletedTasks(db, itemStoreName, callback) {
    let transaction = db.transaction(itemStoreName);
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
            let time = (endTime - startTime).toFixed(2);
            console.log(`Approach 1: Read ${completedTasks} completed tasks in ${time} ms.`);
            callback(time);
        }
    };

    request.onerror = function (event) {
        console.error("Error reading completed tasks:", event.target.error);
    };
}

// STEP 3: Read all COMPLETED tasks and measure time USING READ-ONLY FLAG
function readCompletedTasksReadOnly(db, itemStoreName, callback) {
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
            let time = (endTime - startTime).toFixed(2);
            console.log(`Approach 2 (Read-Only flag): Read ${completedTasks} completed tasks in ${time} ms.`);
            callback(time);
        }
    };

    request.onerror = function (event) {
        console.error("Error reading completed tasks using Read-Only flag:", event.target.error);
    };
}

// Call the functions to set up the DB and read completed tasks
setupIndexedDB("TodoDB", "TodoList", function (db) {
    add100kObjects(db, "TodoList", function () {
        // STEP 2: Read without flag first
         readCompletedTasks(db, "TodoList", function (time) {
            // STEP 3: Read with Read-Only flag
            readCompletedTasksReadOnly(db, "TodoList", function (timeReadonly) {
                console.log(`Time to read using Approach 1: ${time} ms`);
                console.log(`Time to read using Approach 2: ${timeReadonly} ms`);
           });
        })  
    });
});
