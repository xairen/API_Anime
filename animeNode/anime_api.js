const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');

const app = express();
const port = 3000;

//Database configuration
const pool = mysql.createPool({
    host: 'localhost',
    user: 'your_mysql_username',
    password: 'your_mysql_password',
    database: 'your_database_name',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

app.use(bodyParser.json());

//Fetching all anime
app.get('/anime', (req, res) => {
    const query = "SELECT * FROM Anime";
    pool.query(query, (err, result) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(results);
    });
});

//Fetching anime based on ID
app.get('/anime/:id', (req, res) => {
    const query = "SELECT * FROM Anime WHERE id = ?";
    pool.query(query, [req.params.id], (err, results) => {
        if (err) return res.status(500).json({ error: err.message });
        if (results.length === 0) return res.status(404).json({ error: 'Anime not found' });
        res.json(results[0]);
    });
});

//Searching anime by name and genre
app.get('/anime/search', (req, res) => {
    let query = "SELECT * FROM Anime WHERE 1=1";
    const params = [];

    if (req.query.name) {
        query += " AND name LIKE ?";
        params.push('%' + req.query.name + '%');
    }

    if (req.query.genre) {
        query += " AND genre LIKE ?";
        params.push('%' + req.query.genre + '%');
    }

    pool.query(query, params, (err, results) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(results);
    });
});

app.listen(port, () => {
    console.log('Server started on http://localhost:${port}');
});
