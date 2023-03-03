<?php
    require 'dataBase.php';
    $db = new Database();

    $names = $db->getAllRestaurantsFromRatings();
    //var_dump($names);
    foreach($names as $name)
    {
        //commented out in case of accidentally rerunning this script
        //$db->insertRestaurant($name['restaurant_name']);
    }
?>