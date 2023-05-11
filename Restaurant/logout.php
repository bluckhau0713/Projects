<?php
    require 'dataBase.php';
    session_start();
    $db = new dataBase();

    $db->logout();
    header('Location: login.php');
?>