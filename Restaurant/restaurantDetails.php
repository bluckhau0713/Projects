<?php
    require 'templates//menu.php';  
    require 'dataBase.php';
    $db = new dataBase();

    $restaurant = $_POST['restaurant_name'];
    
    $id = $db->getRestaurantIdByName($restaurant);
    //var_dump($restaurant['restaurant_id']);
    $id = $id['restaurant_id'];
    $similar = $db->join($id);
    //var_dump($similar);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css" type="text/css">
    <link rel="script" href="scripts.js">
    <title>Details</title>
</head>
<body>
    <h1><?php echo $restaurant?></h1>
    <h4>Food options:</h4>
    <p>Gluten Free: <?php echo $similar[0]['glutenfree']?></p>
    <p>Vegan: <?php echo $similar[0]['vegan']?></p>
    <p>Kosher: <?php echo $similar[0]['kosher']?></p>
    <h4>Accepted Payment Types:</h4>
    <p>Cash: <?php echo $similar[0]['cash']?></p>
    <p>Card: <?php echo $similar[0]['card']?></p>
    <p>Check: <?php echo $similar[0]['payCheck']?></p>
    <h4>Misc Details:</h4>
    <p>Address: <?php echo $similar[0]['address']?></p>
    <p>Type of food: <?php echo $similar[0]['type']?></p>
    <p>Pricing: <?php echo $similar[0]['pricing']?></p>
    <h4>User Review</h4>
    <?php echo "<p>" . $similar[0]['review'] . "</p>"?>
</body>
</html>