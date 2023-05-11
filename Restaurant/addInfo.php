<?php

    require 'dataBase.php';

    $db = new dataBase;
    $db->addInfo(htmlentities($_POST['restaurant_name']), htmlentities($_POST['address']), htmlentities($_POST['type']), htmlentities($_POST['pricing']));

    header('Location: interactions.php');
?>