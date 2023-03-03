<?php
    require 'templates//menu.php';
    require 'dataBase.php';

    $db = new dataBase();

    $person = trim(htmlentities($_POST['person']));

    $restaurant = trim(htmlentities($_POST['restaurant']));

    $approval = trim(htmlentities($_POST['approve']));
    
     //verifies that approval can be put into a true/false state in the DB
    $approval = strtoupper($approval);
    if($approval === 'YES' || $approval === 'Y')
    {
        $approval = 1;
    }
    elseif($approval === 'NO' || $approval === 'N')
    {
        $approval = 0;
    }

    $rate = trim(htmlentities($_POST['rating']));
    $rate = (float) $rate;
    
    $db->addRating($person, $restaurant, $approval, $rate);

    header('Location: interactions.php');

?>