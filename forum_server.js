const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const app = express();

app.use(bodyParser.json());
app.use(cors());

const DATA_FILE = './forum-data.json';

// Route to get all threads
app.get('/api/threads', (req, res) => {
    fs.readFile(DATA_FILE, 'utf8', (err, fileData) => {
        if (err) {
            console.error('Error reading data file:', err);
            return res.status(500).json({ error: 'Failed to read data.' });
        }
        const threads = fileData ? JSON.parse(fileData) : [];
        res.json(threads);
    });
});

// Route to create a new thread
app.post('/api/threads', (req, res) => {
    const { title, description } = req.body;

    if (!title || !description) {
        return res.status(400).json({ error: 'Title and description are required.' });
    }

    // Read existing data
    fs.readFile(DATA_FILE, 'utf8', (err, fileData) => {
        if (err) {
            console.error('Error reading data file:', err);
            return res.status(500).json({ error: 'Failed to read data.' });
        }

        const threads = fileData ? JSON.parse(fileData) : [];
        const newThread = {
            id: threads.length + 1,
            title,
            description,
            replies: [],
            createdAt: new Date().toISOString(),
        };

        threads.push(newThread);

        // Write updated data back to file
        fs.writeFile(DATA_FILE, JSON.stringify(threads, null, 2), (writeErr) => {
            if (writeErr) {
                console.error('Error writing data file:', writeErr);
                return res.status(500).json({ error: 'Failed to save data.' });
            }
            res.status(201).json(newThread);
        });
    });
});

// Route to add a reply to a thread
app.post('/api/threads/:id/replies', (req, res) => {
    const { id } = req.params;
    const { reply } = req.body;

    if (!reply) {
        return res.status(400).json({ error: 'Reply is required.' });
    }

    // Read existing data
    fs.readFile(DATA_FILE, 'utf8', (err, fileData) => {
        if (err) {
            console.error('Error reading data file:', err);
            return res.status(500).json({ error: 'Failed to read data.' });
        }

        const threads = fileData ? JSON.parse(fileData) : [];
        const thread = threads.find((t) => t.id === parseInt(id, 10));

        if (!thread) {
            return res.status(404).json({ error: 'Thread not found.' });
        }

        thread.replies.push({ reply, createdAt: new Date().toISOString() });

        // Write updated data back to file
        fs.writeFile(DATA_FILE, JSON.stringify(threads, null, 2), (writeErr) => {
            if (writeErr) {
                console.error('Error writing data file:', writeErr);
                return res.status(500).json({ error: 'Failed to save data.' });
            }
            res.status(201).json({ message: 'Reply added successfully.', thread });
        });
    });
});

const PORT = 5003;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
