<?php
    require 'dataBase.php';
    require 'templates//menu.php';

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css" type="text/css">
    <link rel="script" href="scripts.js">
    <title>Login</title>
</head>
<body>
    <h1>Login, if you do not have a login, you will have an account registered</h1>
    <form method="POST" action="profile.php">
            <span>Name:</span>
            <input type='text' label='profileName' name='profileName' id='profileName'>
            <span>Password? </span>
            <input type='password' label='profilePassword' name='profilePassword' id='profilePassword'>
            <button>Submit profile!</button>
    </form>

</body>
</html>