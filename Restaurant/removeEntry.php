<?php

    require 'dataBase.php';
    $db = new Database();

    $person = htmlentities($_POST['person']);

    $restaurant = htmlentities($_POST['restaurant']);

    $db->removeRating($person, $restaurant);

    header('Location: interactions.php');

?>