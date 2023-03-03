<?php
    require 'templates//menu.php';
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
</body>
</html>