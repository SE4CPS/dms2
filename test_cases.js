function isStringNotNull(str) {
    return str !== null && str !== undefined;
}

const farmData = {
    temperatureHumidityReading: [[20.5, 45.5]],
    cropPictureBase64Path: "data:image/jpeg;base64,/8BBQZjZJRkBBCPEAAAAAAAD/...",
    farmerNoteString: "Crops are sown, need daily 2l water intake",
    gpsCoordArray: [[-45.94334, -98.123478]],
    dataTimestamp: new Date(),
};

// Test 1: unit test on the sensor reading data of the farmdata
function testTemperatureHumidityReading() {
        console.assert(Array.isArray(farmData.temperatureHumidityReading), "Test failed: temperatureHumidityReading should be an array of array.");
        console.assert(farmData.temperatureHumidityReading[0].length === 2, "Test failed: Each entry in temperatureHumidityReading should have 2 values.");
        farmData.temperatureHumidityReading[0].forEach(value => console.assert(typeof value === "number", "Test failed: All values in temperatureHumidityReading should be numbers."));
        console.log("temperatureHumidityReading tests passed.");
}


function testCropPictureBase64Path() {
        console.assert(isStringNotNull(farmData.cropPictureBase64Path), "Test failed: cropPictureBase64Path should not be null or undefined.");
        console.assert(typeof farmData.cropPictureBase64Path === "string", "Test failed: cropPictureBase64Path should be a string.");
        console.assert(farmData.cropPictureBase64Path.startsWith("data:image/jpeg;base64,"), "Test failed: cropPictureBase64Path should start with 'data:image/jpeg;base64,'.");
        console.log("cropPictureBase64Path tests passed.");
}

function testFarmerNoteString() {
        console.assert(isStringNotNull(farmData.farmerNoteString), "Test failed: farmerNoteString should not be null or undefined.");
        console.assert(typeof farmData.farmerNoteString === "string", "Test failed: farmerNoteString should be a string.");
        console.assert(farmData.farmerNoteString.length > 0, "Test failed: farmerNoteString should not be empty.");
        console.log("farmerNoteString tests passed.");
}

function testGpsCoordArray() {
        console.assert(Array.isArray(farmData.gpsCoordArray), "Test failed: gpsCoordArray should be an array.");
        console.assert(farmData.gpsCoordArray[0].length === 2, "Test failed: Each GPS coordinate entry should have 2 values.");
        farmData.gpsCoordArray[0].forEach(value => console.assert(typeof value === "number", "Test failed: All values in gpsCoordArray should be numbers."));
        console.log("gpsCoordArray tests passed.");
}

function testTimestamp() {
        console.assert(farmData.dataTimestamp instanceof Date, "Test failed: dataTimestamp should be a Date object.");
        console.assert(!isNaN(farmData.dataTimestamp.getTime()), "Test failed: dataTimestamp should be a valid date.");
        console.log("dataTimestamp tests passed.");
}

window.onload = function() {
        testTemperatureHumidityReading();
        testCropPictureBase64Path();
        testFarmerNoteString();
        testGpsCoordArray();
        testTimestamp();
    };