<?php

    require 'dataBase.php';

    $db = new dataBase;
    $db->addTextReview(htmlentities($_POST['restaurant_name']), htmlentities($_POST['review']));

    header('Location: interactions.php');
?>