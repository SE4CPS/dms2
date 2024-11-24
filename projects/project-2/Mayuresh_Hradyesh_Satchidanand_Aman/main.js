fetch('http://127.0.0.1:5000/data')
    .then(response => response.json())
    .then(data => {
        console.log('Fetched Data:', data);

        // Initialize data lake
        const lake = [];

        // Process MongoDB data
        data.MongoDB.forEach(flower => {
            lake.push({ db: "MongoDB", flower });
        });

        // Process Neo4J data
        data.Neo4J.forEach(rel => {
            lake.push({
                db: "Neo4J",
                flower: {
                    name: rel.flower,
                    zip_code: rel.zip_code,
                    related_to: rel.related_to
                }
            });
        });

        // Process Redis data
        for (const [name, details] of Object.entries(data.Redis)) {
            lake.push({
                db: "Redis",
                flower: {
                    name,
                    ...details
                }
            });
        }

        // Process SQL data
        data.SQL.forEach(sale => {
            lake.push({ db: "SQL", flower: sale });
        });

        console.log('Data Lake:', lake);

        // Create warehouse: aggregate counts by zip code
        const warehouse = lake.reduce((acc, entry) => {
            const zip = entry.flower.zip_code;
            acc[zip] = (acc[zip] || 0) + 1;
            return acc;
        }, {});

        console.log('Warehouse:', warehouse);

        // Prepare data for Chart.js
        const labels = Object.keys(warehouse);
        const counts = Object.values(warehouse);

        const ctx = document.getElementById('zipChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Flower Count by Zip Code',
                    data: counts,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        enabled: true
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Zip Codes'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Flower Count'
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching data:', error));
