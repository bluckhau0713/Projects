<?php
    require 'dataBase.php';
    require 'restaurantOb.php';
    require 'templates//menu.php';

    $db = new Database();
    $people = $db->getPeopleGoing();
    //var_dump($people);

    $attendingNames = array();  //stores the names of whomever is going
    $attendingIds = array();    //stores whomever is going's ids
    $scores = array();      //used to store final ratings of resaurants
    $approved = array();    //used to see if a restaurant is approved by all

    $currentPersonRatings;  //gets the ratings of the most current person

    $randomPlaceToEat = rand(0,9);  //chooses a random place out of the top 10

    foreach($people as $group)  //adds to $attending array
    {
        if(isset($_POST[$group['person_name']]))
        {
            array_push($attendingNames, $group['person_name']);
            array_push($attendingIds, $group['person_id']);
        }
    }
    $restaurants = $db->getAllRestaurantNames();
    //var_dump($restaurants);

    //get all restaurants in an array and stores them as objects to easily score and rate them
    foreach($restaurants as $score)
    {
        array_push($scores, new Restaurant($score['restaurant_name']));
    }
    
    //var_dump($currentPersonRatings);
    for($j = 0; $j < count($attendingIds); $j++)    //loops over each person
    {
        $currentPersonRatings = $db->getPersonRatings($attendingIds[$j]);
        foreach($currentPersonRatings as $score)    //checks each persons ratings
        {
            $i = 0;
            while($score['restaurant_name'] != $scores[$i]->name)   //finds the name of the restaurant
            {
                $i++;
                //var_dump($i);
                if($i > count($restaurants)) //used to see if there was a misspelling of a restaurant in the rating DB
                {
                    echo '<br><br><br>';
                    echo $score['restaurant_name'] . ' is misspelled, or you need to regenerate the DB for restaurant names';
                    echo '<br><br><br>';
                    break;
                }
            }

            //alters the current restaurant's object's score 
            $current = $scores[$i]; 
            $current->changeApproval($score['approve']);
            $current->addToScore($score['rating']);
            $current->addAttending();
            //var_dump($current);
            //echo '<br>';
        }
    }
    //var_dump($scores);
    // echo '<br><br><br>';

    //sorts the restaurants based on the average score being the highest
    usort($scores, function ($a, $b)
    {
        return $b->calculateAverage() <=> $a->calculateAverage();
    });
    $json = json_encode($scores);   //convert array to javascript
?>

<script>
let javascript_array = <?php echo $json; ?>;
console.log(javascript_array);
function determineRestaurant(places, text)
{   
    rand = Math.floor(Math.random() * 10);  //semi random restaurant from the top 10
    text.textContent = places[rand]['name'] + "!!!";
}
</script>

<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" type="text/css">
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Where in the world are we eating?</title>
</head>

<body>
    <h1>Your answer to where we are going to eat today is:<h1 id="whereToEat"></h1><button id="clickButton" onclick="determineRestaurant(javascript_array, text)">Regenerate Answer</button></h1>
    <script>
        //prints the first place to eat
        let text = document.getElementById("whereToEat");
        determineRestaurant(javascript_array, text);
    </script>

    <div >   <!-- What are rated -->
        <table id="ratedTable">
            <thead>
                <tr><td>Top 10 Places</td>
                    <?php for($i = 0; $i < 10; $i++)
                    {
                        echo "<th> ". $scores[$i]->name . '</th>';
                    } ?>
                </tr>
            </thead>
            <tbody>
                    <tr>
                        <td>Total Score</td>
                        <?php for($i = 0; $i < 10; $i++)
                        {
                            echo "<td> ". $scores[$i]->getScore() . ' ('.(10 * $scores[$i]->getHowManyAttended()) .')</td>';
                        } ?>
                    </tr>
                    <tr>
                        <td>How many have been there</td>
                        <?php for($i = 0; $i < 10; $i++)
                        {
                            echo "<td> ". $scores[$i]->getHowManyAttended() . '</td>';
                        } ?>
                    </tr>
                    <tr>
                        <td>Average </td>
                        <?php for($i = 0; $i < 10; $i++)
                        {
                            echo "<td> ". round($scores[$i]->calculateAverage(), 2). '</td>';
                        } ?>
                    </tr>
            </tbody>
        </table>
        <table id="ratedTable">
            <thead>
                <tr><td>Next 10 Places</td>
                    <?php for($i = 10; $i < 20; $i++)
                    {
                        echo "<th> ". $scores[$i]->name . '</th>';
                    } ?>
                </tr>
            </thead>
            <tbody>
                    <tr>
                        <td>Total Score</td>
                        <?php for($i = 10; $i < 20; $i++)
                        {
                            echo "<td> ". $scores[$i]->getScore() . ' ('.(10 * $scores[$i]->getHowManyAttended()) .')</td>';
                        } ?>
                    </tr>
                    <tr>
                        <td>How many have been there</td>
                        <?php for($i = 10; $i < 20; $i++)
                        {
                            echo "<td> ". $scores[$i]->getHowManyAttended() . '</td>';
                        } ?>
                    </tr>
                    <tr>
                        <td>Average </td>
                        <?php for($i = 10; $i < 20; $i++)
                        {
                            echo "<td> ". round($scores[$i]->calculateAverage(), 2). '</td>';
                        } ?>
                    </tr>
            </tbody>
        </table>
        <table id="ratedTable">
            <thead>
                <tr><td>Next 10 Places</td>
                    <?php for($i = 20; $i <30; $i++)
                    {
                        echo "<th> ". $scores[$i]->name . '</th>';
                    } ?>
                </tr>
            </thead>
            <tbody>
                    <tr>
                        <td>Total Score</td>
                        <?php for($i = 20; $i <30; $i++)
                        {
                            echo "<td> ". $scores[$i]->getScore() . ' ('.(10 * $scores[$i]->getHowManyAttended()) .')</td>';
                        } ?>
                    </tr>
                    <tr>
                        <td>How many have been there</td>
                        <?php for($i = 20; $i <30; $i++)
                        {
                            echo "<td> ". $scores[$i]->getHowManyAttended() . '</td>';
                        } ?>
                    </tr>
                    <tr>
                        <td>Average </td>
                        <?php for($i = 20; $i <30; $i++)
                        {
                            echo "<td> ". round($scores[$i]->calculateAverage(), 2). '</td>';
                        } ?>
                    </tr>
            </tbody>
        </table>
    </div>
    <br>

    <!-- What are approved in the top 10 -->
    <div class = "approved">
    <span id="approvedInTen" class="approved">
        <h3>Approved by everyone in the top 10
            <p class="approvedP">
                <?php
                for($i = 0; $i < 10; $i++)  //print out 
                {
                    if($scores[$i]->getApproval())
                    {
                        echo $scores[$i]->name;
                        echo '<br>';
                    }

                }
                ?>
            </p>
        </h3>
    </span>
    <!-- What are approved -->
    <span id="aprrovedByAll" class="approved">
        <h3>Out of all of the people going, the "approved" restaurants are as follows
            <p class="approvedP">
                <?php
                for($i = 0; $i < count($scores); $i++)  //print out 
                {
                    if($scores[$i]->getApproval())
                    {
                        echo $scores[$i]->name;
                        echo '<br>';
                    }

                }
                ?>
            </p>
        </h3>
    </span>
    </div>
</body>
</html>