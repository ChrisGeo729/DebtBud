const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const app = express();

app.use(bodyParser.json());
app.use(cors());

// POST route to handle contact form submission
app.post('/api/contact', (req, res) => {
    const { name, email, message } = req.body;

    if (!name || !email || !message) {
        return res.status(400).json({ error: 'All fields are required.' });
    }

    // Save the data to a JSON file (simulating a database)
    const data = { name, email, message, timestamp: new Date().toISOString() };
    const filePath = './contact-submissions.json';

    // Read existing data, append new entry, and save
    fs.readFile(filePath, 'utf8', (err, fileData) => {
        const submissions = fileData ? JSON.parse(fileData) : [];
        submissions.push(data);

        fs.writeFile(filePath, JSON.stringify(submissions, null, 2), (writeErr) => {
            if (writeErr) {
                return res.status(500).json({ error: 'Failed to save data.' });
            }

            res.status(200).json({ message: 'Your message has been received!' });
        });
    });
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
