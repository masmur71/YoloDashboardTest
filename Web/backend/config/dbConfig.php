<?php
$host = 'localhost';
$db = 'yolodetect';
$user = 'root';
$pass = '';

// Membuat koneksi ke database
$mysqli = new mysqli($host, $user, $pass, $db);

// Mengecek koneksi
if ($mysqli->connect_error) {
    die("Connection failed: " . $mysqli->connect_error);
}
?>
