// backend/config/dbConfig.js

const mysql = require('mysql2');

// Konfigurasi koneksi ke database
const dbConfig = {
    host: 'localhost',      
    user: 'root',           
    password: '',   
    database: 'detection_db'  
};

// Membuat koneksi ke database
const connection = mysql.createConnection(dbConfig);

// Menghubungkan ke database
connection.connect(error => {
    if (error) {
        console.error('Error connecting to the database:', error.stack);
        return;
    }
    console.log('Connected to the MySQL database as id', connection.threadId);
});

module.exports = connection;
