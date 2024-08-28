// backend/routes/detectionRoutes.js

const express = require('express');
const router = express.Router();
const detectionController = require('../controllers/detectionController');

// Route untuk GET /detections
router.get('/detections', detectionController.getDetections);

module.exports = router;
