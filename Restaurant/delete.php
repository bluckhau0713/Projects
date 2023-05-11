<?php

    require 'dataBase.php';

    $db = new dataBase;
    //$db->addTextReview(htmlentities($_POST['restaurant_name']), htmlentities($_POST['review']));

    $db->deleteEntry(htmlentities($_POST['restaurant_name']), htmlentities($_POST['table']));
    header('Location: interactions.php');
?>