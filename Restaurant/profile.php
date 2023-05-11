<?php
    require 'dataBase.php';
    $db = new dataBase();

    $name = trim(htmlentities($_POST['profileName']));

    $pass = trim(htmlentities($_POST['profilePassword']));
    $hashPass = password_hash($pass, PASSWORD_DEFAULT);

    $db->checkLogin($name, $hashPass);

    header('Location: whoIsGoing.php');
?>