// Create basic walker profile
print('Create basic walker profile');
db.walkers.insertOne({ _id: 1, name: "Jane Smith", age: 30, country: "USA" });

// Create personal best time for a 5KM walk
print('Create personal best time for a 5KM walk');
db.walkers.updateOne(
    { _id: 1 },
    { $set: { pb_5km: "45:20" } }
);

// Create initial distance record in kilometers
print('Create initial distance record in kilometers');
db.walkers.updateOne(
    { _id: 1 },
    { $set: { distance_km: 0 } }
);

// Create details for a walking event
print('Create details for a walking event');
db.events.insertOne({
    _id: 1,
    name: "City Walkathon",
    location: "Chicago",
    date: new Date("2024-11-15"),
    distance_km: 10
});

// Register the walker for the event
print('Register the walker for the event');
db.events.updateOne(
    { _id: 1 },
    { $addToSet: { participants: 1 } }
);

// Add walker to a walking group
print('Add walker to a walking group');
db.groups.updateOne(
    { name: "morning_walkers" },
    { $addToSet: { members: 1 } },
    { upsert: true }
);

// Store split times for a walker during an event
print('Store split times for a walker during an event');
db.walkers.updateOne(
    { _id: 1 },
    { $set: { split_times: ["00:10:32", "00:10:28"] } }
);

// Create a weekly walking schedule for the walker
print('Create a weekly walking schedule for the walker');
db.walkers.updateOne(
    { _id: 1 },
    {
        $set: {
            schedule: {
                Monday: "5 km",
                Wednesday: "3 km",
                Friday: "6 km"
            }
        }
    }
);

// Record steps taken by the walker on a specific day
print('Record steps taken by the walker on a specific day');
db.walkers.updateOne(
    { _id: 1 },
    { $set: { "steps.2024-10-31": 8000 } }
);

// Create a monthly walking goal for the walker
print('Create a monthly walking goal for the walker');
db.walkers.updateOne(
    { _id: 1 },
    { $set: { monthly_goal: 50 } }
);

// Retrieve walker profile
print('Retrieve walker profile');
printjson(db.walkers.findOne({ _id: 1 }));

// Retrieve personal best time for a 5KM walk
print('Retrieve personal best time for a 5KM walk');
printjson(db.walkers.findOne({ _id: 1 }, { pb_5km: 1 }));

// Retrieve total distance walked in kilometers
print('Retrieve total distance walked in kilometers');
printjson(db.walkers.findOne({ _id: 1 }, { distance_km: 1 }));

// Retrieve details of a walking event
print('Retrieve details of a walking event');
printjson(db.events.findOne({ _id: 1 }));

// Check if walker is registered for the event
print('Check if walker is registered for the event');
printjson(db.events.findOne({ _id: 1, participants: 1 }));

// Get list of all participants registered for the event
print('Get list of all participants registered for the event');
printjson(db.events.findOne({ _id: 1 }, { participants: 1 }));

// Retrieve all split times for the walker
print('Retrieve all split times for the walker');
printjson(db.walkers.findOne({ _id: 1 }, { split_times: 1 }));

// Retrieve the weekly walking schedule for the walker
print('Retrieve the weekly walking schedule for the walker');
printjson(db.walkers.findOne({ _id: 1 }, { schedule: 1 }));

// Retrieve steps taken by the walker on a specific day
print('Retrieve steps taken by the walker on a specific day');
printjson(db.walkers.findOne({ _id: 1 }, { "steps.2024-10-31": 1 }));

// Check if the walker is part of the morning_walkers group
print('Check if the walker is part of the morning_walkers group');
printjson(db.groups.findOne({ name: "morning_walkers", members: 1 }));

// Retrieve finish time for the walker in an event
print('Retrieve finish time for the walker in an event');
printjson(db.events.findOne({ _id: 1 }, { results: 1 }));

// Retrieve all finish times for participants in a specific event
print('Retrieve all finish times for participants in a specific event');
printjson(db.events.findOne({ _id: 1 }, { results: 1 }));

// Retrieve the walker health condition
print('Retrieve the walker health condition');
printjson(db.walkers.findOne({ _id: 1 }, { health: 1 }));

// Retrieve the walker monthly walking goal
print('Retrieve the walker monthly walking goal');
printjson(db.walkers.findOne({ _id: 1 }, { monthly_goal: 1 }));

// Update walker age
print('Update walker age');
db.walkers.updateOne(
    { _id: 1 },
    { $set: { age: 31 } }
);

// Update total distance walked in kilometers
print('Update total distance walked in kilometers');
db.walkers.updateOne(
    { _id: 1 },
    { $inc: { distance_km: 3.2 } }
);

// Update finish time for walker in the event
print('Update finish time for walker in the event');
db.events.updateOne(
    { _id: 1 },
    { $set: { results: { walker1: '1:35:20' } } }
);

// Update the walker health condition
print('Update the walker health condition');
db.walkers.updateOne(
    { _id: 1 },
    { $set: { health: 'minor foot pain' } }
);

// Simple aggregation to count the number of walkers
print('Count the number of walkers');
const walkerCount = db.walkers.aggregate([
    { $group: { _id: null, count: { $sum: 1 } } }
]).toArray();

// Print the total number of walkers, check if the array has elements
if (walkerCount.length > 0) {
    print('Total number of walkers:', walkerCount[0].count);
} else {
    print('No walkers found.');
}

// Delete walker profile information
print('Delete walker profile information');
db.walkers.deleteOne({ _id: 1 });

// Delete walker personal best time
print('Delete walker personal best time');
db.walkers.updateOne(
    { _id: 1 },
    { $unset: { pb_5km: "" } }
);

// Delete all split times for the walker
print('Delete all split times for the walker');
db.walkers.updateOne(
    { _id: 1 },
    { $unset: { split_times: "" } }
);

// Remove walker from the walking group
print('Remove walker from the walking group');
db.groups.updateOne(
    { name: "morning_walkers" },
    { $pull: { members: 1 } }
);

// Delete walker steps record for a specific day
print('Delete walker steps record for a specific day');
db.walkers.updateOne(
    { _id: 1 },
    { $unset: { "steps.2024-10-31": "" } }
);

// Delete walker monthly walking goal
print('Delete walker monthly walking goal');
db.walkers.updateOne(
    { _id: 1 },
    { $unset: { monthly_goal: "" } }
);
