<?php
include_once '../config/dbConfig.php';

class Detection {
    // Mengambil semua data dari tabel detections
    public function getAllDetections() {
        global $mysqli;
        $query = "SELECT * FROM detections";
        $result = $mysqli->query($query);

        if (!$result) {
            return false;
        }

        return $result->fetch_all(MYSQLI_ASSOC);
    }
}
?>
