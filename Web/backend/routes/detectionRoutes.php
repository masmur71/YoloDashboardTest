<?php
include_once '../controllers/detectionController.php';

$controller = new DetectionController();

// Mendapatkan URL permintaan
$request = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

// Routing untuk GET /detections
if ($method == 'GET' && $request == '/backend/public/index.php/api/detections') {
    $controller->getDetections();
} else {
    header('HTTP/1.1 404 Not Found');
    echo json_encode(['error' => 'Route not found']);
}
?>
