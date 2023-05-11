<?php

    require 'dataBase.php';

    $db = new dataBase;
    $db->addPayments(htmlentities($_POST['restaurant_name']), htmlentities($_POST['cash']), htmlentities($_POST['card']), htmlentities($_POST['check']));

    header('Location: interactions.php');
?>