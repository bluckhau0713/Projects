<?php
    session_start();
    if($_SESSION['isLoggedIn'] == false)
    {
        header('Location: login.php');
    }
    require 'templates//menu.php';
    require 'dataBase.php';
    $db = new dataBase();
    
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactions</title>
</head>
<body>
    <div class="input">
        <span >Add person: 
            <form method='post' action='addPerson.php'>
            <input type='text' name='newPerson' label='newPerson' id='newPerson'>
            <button>Submit new person!</button>
            </form>
        </span>
    </div>
    <hr>
    <div class="input">
        <span>Add rating: 
            <form method='post' action='addRating.php'>
                <span>Person:</span>
                <input type='text' label='person' name='person' id='newPerson'>
                <span>Restaurant:</span>
                <input type='text' label='restaurant' name='restaurant' id='restaurant'>
                <span>Approve? Yes or no:</span>
                <input type='text' label='approve' name='approve' id='approve'>
                <span>Rating:</span>
                <input type='text' label='rating' name='rating' id='rating'>
                <button>Submit new entry!</button>
            </form>
        </span>
    </div>
    <hr>
    <div class="input">
        <span>Delete entry: 
            <form method='post' action='removeEntry.php'>
                <span>Person:</span>
                <input type='text' label='person' name='person' id='personDeleteing'>
                <span>Restaurant:</span>
                <input type='text' label='restaurant' name='restaurant' id='restaurantToDelete'>
                <button>Submit entry to delete!</button>
            </form>
        </span>
    </div>
    <hr>
    <div class="input">
        <span>Delete from names: 
            <form method='post' action='removeName.php'>
                <span>Restaurant:</span>
                <input type='text' label='restaurant' name='restaurant' id='restaurantToDelete'>
                <button>Submit entry to delete!</button>
            </form>
        </span>
    </div>
    <hr>
    <div class="input">
        <span>Add restaurant food information 0/1:
            <form method='post' action='addFood.php'>
                <select name=restaurant_name>
                    <?php
                        $names = $db->getAllRestaurantNames();
                        foreach($names as $name)
                        {  
                            echo '<option value ="' . $name['restaurant_name'] . '">' . $name['restaurant_name'] . '</option>';
                        }
                    ?>
                </select>
                <span>Gluten Free:</span>
                <input type='text' label='glutenfree' name='glutenfree' id='glutenfree'>
                <span>Vegan:</span>
                <input type='text' label='vegan' name='vegan' id='vegan'>
                <span>Kosher:</span>
                <input type='text' label='kosher' name='kosher' id='kosher'>
                <button>Submit food details to add!</button>
            </form>
        </span>
    </div>
    <hr>
    <div class="input">
        <span>Add restaurant payment options 0/1:
            <form method='post' action='addPayment.php'>
                <select name=restaurant_name>
                    <?php
                        $names = $db->getAllRestaurantNames();
                        foreach($names as $name)
                        {  
                            echo '<option value ="' . $name['restaurant_name'] . '">' . $name['restaurant_name'] . '</option>';
                        }
                    ?>
                </select>
                <span>Cash:</span>
                <input type='text' label='cash' name='cash' id='cash'>
                <span>Card:</span>
                <input type='text' label='card' name='card' id='card'>
                <span>Check:</span>
                <input type='text' label='check' name='check' id='check'>
                <button>Submit payment types!</button>
            </form>
        </span>
    </div>
    <hr>
    <div class="input">
        <span>Add restaurant information:
            <form method='post' action='addInfo.php'>
                <select name=restaurant_name>
                    <?php
                        $names = $db->getAllRestaurantNames();
                        foreach($names as $name)
                        {  
                            echo '<option value ="' . $name['restaurant_name'] . '">' . $name['restaurant_name'] . '</option>';
                        }
                    ?>
                </select>
                <span>Address:</span>
                <input type='text' label='address' name='address' id='address'>
                <span>Type of Food:</span>
                <input type='text' label='type' name='type' id='type'>
                <span>Pricing rate:</span>
                <input type='text' label='pricing' name='pricing' id='pricing'>
                <button>Submit restaurant details!</button>
            </form>
        </span>
    </div>
    <hr>
    <div class="input">
        <span>Add text review:
            <form method='post' action='addReview.php'>
                <select name=restaurant_name>
                    <?php
                        $names = $db->getAllRestaurantNames();
                        foreach($names as $name)
                        {  
                            echo '<option value ="' . $name['restaurant_name'] . '">' . $name['restaurant_name'] . '</option>';
                        }
                    ?>
                </select>
                <span>Review:</span>
                <input type='text' label='review' name='review' id='review'>
                <button>Submit a text review!</button>
            </form>
        </span>
    </div>
    <hr>
    <div class="input">
        <span>Delete:
            <form method='post' action='delete.php'>
                <select name=restaurant_name>
                    <?php
                        $names = $db->getAllRestaurantNames();
                        foreach($names as $name)
                        {  
                            echo '<option value ="' . $name['restaurant_name'] . '">' . $name['restaurant_name'] . '</option>';
                        }
                    ?>
                </select>
                <span>From:</span>
                <select name=table>
                        <option value="food">Restaurant Food Info</option>
                        <option value="payments">Payment Options</option>
                        <option value="restaurant_info">Restaurant Info</option>
                        <option value="text_review">Text Review</option>
                </select>
                <button>Delete entry!</button>
            </form>
        </span>
    </div>
</body>
</html>