const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const app = express();

app.use(bodyParser.json());
app.use(cors());

// POST route to handle newsletter signup
app.post('/api/newsletter', (req, res) => {
  const { email } = req.body;

  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'A valid email address is required.' });
  }

  const filePath = './newsletter_subscriptions.json';

  // Read and update the file
  fs.readFile(filePath, 'utf8', (err, fileData) => {
    const subscriptions = fileData ? JSON.parse(fileData) : [];

    // Check for duplicate email
    if (subscriptions.some(sub => sub.email === email)) {
      return res.status(400).json({ error: 'This email is already subscribed.' });
    }

    subscriptions.push({ email, timestamp: new Date().toISOString() });

    fs.writeFile(filePath, JSON.stringify(subscriptions, null, 2), (writeErr) => {
      if (writeErr) {
        return res.status(500).json({ error: 'Failed to save data.' });
      }

      res.status(200).json({ message: 'Successfully subscribed!' });
    });
  });
});

// Start the server
const PORT = 5005;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
