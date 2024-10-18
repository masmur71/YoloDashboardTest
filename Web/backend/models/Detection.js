// backend/models/Detection.js

const db = require('../config/dbConfig');

// Fungsi untuk mengambil semua data deteksi dari database
const getAllDetections = (callback) => {
    const query = 'SELECT * FROM peoplecount';
    db.query(query, (err, results) => {
        if (err) {
            return callback(err, null);
        }
        return callback(null, results);
    });
};

module.exports = {
    getAllDetections
};
