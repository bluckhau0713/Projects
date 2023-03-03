<?php
    require 'dataBase.php';
    $db = new Database();

    $res = trim(htmlentities($_POST['restaurant']));

    $db->deleteRestaurantFromNames($res);
    
    header('Location: interactions.php');
?>