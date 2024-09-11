<?php
include_once '../models/Detection.php';

class DetectionController {
    // Controller untuk menangani permintaan GET /detections
    public function getDetections() {
        $detectionModel = new Detection();
        $detections = $detectionModel->getAllDetections();
        
        if ($detections === false) {
            header('HTTP/1.1 500 Internal Server Error');
            echo json_encode(['error' => 'Failed to retrieve detections']);
        } else {
            header('Content-Type: application/json');
            echo json_encode($detections);
        }
    }
}
?>
