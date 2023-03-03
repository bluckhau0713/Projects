<?php

    require 'dataBase.php';

    $name = htmlentities($_POST['newPerson']);
    //var_dump($name);
    $conn = new dataBase();
    $conn->addPerson($name);

    header('Location: interactions.php');
?>