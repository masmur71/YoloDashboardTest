// backend/controllers/detectionController.js

const Detection = require('../models/Detection');

// Controller untuk menangani permintaan GET /detections
const getDetections = (req, res) => {
    Detection.getAllDetections((err, detections) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to retrieve detections' });
        }
        return res.status(200).json(detections);
    });
};

module.exports = {
    getDetections
};
