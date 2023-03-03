<?php
    require 'templates//menu.php';
    require 'dataBase.php';
    $db = new Database();

//need to open up the accessability of opening new people to the website
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- <link rel="stylesheet" href="style.css" type="text/css"> -->
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Who Is Going</title>
</head>
<body>
    <h1>Check who is going</h1>
    <form action="whereToEat.php" method="post">
        <?php $people = $db->getPeopleGoing();
        //var_dump($people);
        foreach($people as $group)
        {
            echo $group['person_name'].":";
            echo "<input type = 'checkbox' name=".$group['person_name']."><br>";
        
        }?>

        <button><img src="burger.jpg" id="burger"></button>
    </form>

</body>
</html>