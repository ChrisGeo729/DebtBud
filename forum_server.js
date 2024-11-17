const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const app = express();

app.use(bodyParser.json());
app.use(cors());

const DATA_FILE = './forum-data.json';

// Helper function to read and write JSON data
const readData = () => {
    if (!fs.existsSync(DATA_FILE)) {
        return { threads: [] };
    }
    const data = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(data);
};

const writeData = (data) => {
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
};

// Route to get all threads
app.get('/api/threads', (req, res) => {
    const data = readData();
    res.json(data.threads);
});

// Route to create a new thread
app.post('/api/threads', (req, res) => {
    const { title, description } = req.body;
    if (!title || !description) {
        return res.status(400).json({ error: 'Title and description are required.' });
    }

    const data = readData();
    const newThread = {
        id: data.threads.length + 1,
        title,
        description,
        replies: [],
    };
    data.threads.push(newThread);
    writeData(data);

    res.status(201).json(newThread);
});

// Route to add a reply to a thread
app.post('/api/threads/:id/replies', (req, res) => {
    const { id } = req.params;
    const { reply } = req.body;

    if (!reply) {
        return res.status(400).json({ error: 'Reply is required.' });
    }

    const data = readData();
    const thread = data.threads.find((t) => t.id === parseInt(id, 10));

    if (!thread) {
        return res.status(404).json({ error: 'Thread not found.' });
    }

    thread.replies.push(reply);
    writeData(data);

    res.status(201).json({ message: 'Reply added successfully.', thread });
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
