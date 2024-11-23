// Fetch the data from the server
fetch('http://localhost:5000/get_flower_data')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // Parse JSON data
    })
    .then(data => {
        console.log('Fetched Data:', data);

        // Empty array for the data lake
        let lake = [];

        // Getting data from their respective sources
        for (let source in data) {
            // MongoDB data
            if (source === "MongoDB") {
                const transformed = data[source]["flowers"].map(flower => ({
                    db: "MongoDB",
                    flower
                }));
                lake = lake.concat(transformed);
            }

            // Neo4J data
            if (source === "Neo4J") {
                const transformed = data[source]["relationships"].map(rel => ({
                    db: "Neo4J",
                    flower: {
                        name: rel.flower,
                        related_to: rel.related_to,
                        zip_code: rel.zip_code
                    }
                }));
                lake = lake.concat(transformed);
            }

            // Redis data
            if (source === "Redis") {
                const transformed = Object.entries(data[source]["inventory"]).map(([name, details]) => ({
                    db: "Redis",
                    flower: {
                        name,
                        ...details
                    }
                }));
                lake = lake.concat(transformed);
            }

            // SQL data
            if (source === "SQL") {
                const transformed = data[source]["flower_sales"].map(flower => ({
                    db: "SQL",
                    flower
                }));
                lake = lake.concat(transformed);
            }
        }

        console.log('Data Lake:', lake);


        // create warehouse
        // with zipcodes and flower count per zipcode

        // array of unique zip codes
        const uniqueZips = lake
            .map(entry => entry.flower.zip_code)
            .filter((zip_code, index, self) =>
            self.indexOf(zip_code) === index);
    
        console.log(uniqueZips);

        // fill warehouse
        const warehouse = { };

        key = 0;
        for (let zip in uniqueZips) {
            let currentCount = lake
                .filter(entry => entry.flower.zip_code === uniqueZips[key])
                .reduce((count, _) => count + 1, 0);

            warehouse[key] = {zip_code: uniqueZips[key], count: currentCount} // add entry

            key ++;
        }

        console.log('Warehouse:', warehouse);

    })
    .catch(error => console.error('Error fetching data:', error));