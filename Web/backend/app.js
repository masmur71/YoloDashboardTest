// backend/app.js

const express = require('express');
const app = express();
const detectionRoutes = require('../backend/routes/detectionRoutes');

// Middleware untuk memparsing request body dalam format JSON (jika diperlukan)
app.use(express.json());

// Menggunakan routes
app.use('/', detectionRoutes);

// Menangani permintaan ke endpoint lain yang tidak ditemukan
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// Memulai server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
