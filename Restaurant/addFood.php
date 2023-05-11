<?php

    require 'dataBase.php';

    $db = new dataBase;
    $db->addFood(htmlentities($_POST['restaurant_name']), htmlentities($_POST['glutenfree']), htmlentities($_POST['vegan']), htmlentities($_POST['kosher']));

    header('Location: interactions.php');
?>