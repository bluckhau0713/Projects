<?php

    class Database
    {
        
        private PDO $dbh;   //database connection for PDO style

        public function __construct()
        {    
        
            $server = "mysql:dbname=restaurantdb;host=127.0.0.1"; 
            $username = "root";
            $password = "";
            $this->dbh = new PDO($server, $username, $password);
        }

        //**************************************PERSON DB**************************************
        public function addPerson($name)
        {
            session_start();
            $statement = $this->dbh->prepare("INSERT INTO person (person_name, profile_id) VALUES (:person_name, :profile_id)");
            $statement->bindValue('person_name', $name);
            $statement->bindValue('profile_id', $_SESSION['profile_id']);
            $statement->execute();
        }

        public function getPerson($person)
        {
            session_start();
            $statement = $this->dbh->prepare("SELECT person_id FROM person WHERE person_name = :person_name AND profile_id = :profile_id");
            $statement->bindValue('person_name', $person);
            $statement->bindValue('profile_id', $_SESSION['profile_id']);
            $statement->execute();
            return $statement->fetch(PDO::FETCH_ASSOC);
        }

        public function getPeopleGoing()    //gets everyone from the person DB into an array with their ID's and Name's
        {
            //session_start();
            $statement = $this->dbh->prepare('SELECT * FROM person WHERE profile_id = :profile_id');
            $statement->bindValue('profile_id', $_SESSION['profile_id']);
            $statement->execute();
            return $statement->fetchAll(PDO::FETCH_ASSOC);            
        }

        //**************************************PERSON DB**************************************


        //**************************************RESTAURANT DB**************************************
        public function addRating($person, $restaurant, $likes, $rating)
        {
            //need to add if already exists, update maybe do in the addRating.php
            session_start();
            $person_id = $this->getPerson($person);
            $person_id = $person_id['person_id'];
            $statement = $this->dbh->prepare("INSERT INTO restaurants (person_id, person_name, restaurant_name, approve, rating, profile_id) VALUES (:person_id, :person_name, :restaurant_name, :approve, :rating, :profile_id)");
            $statement->bindValue('person_id', $person_id);
            $statement->bindValue('person_name', $person);
            $statement->bindValue('restaurant_name', $restaurant);
            $statement->bindValue('approve', $likes);
            $statement->bindValue('rating', $rating);
            $statement->bindValue('profile_id', $_SESSION['profile_id']);
            $statement->execute();
            syslog(LOG_INFO, "$person_id, $person, logged for $restaurant, with an approval of $likes, and rated $rating");
        }

        public function removeRating($person, $restaurant)  //deletes a rating from the restaurants DB
        {
            session_start();
            $person_id = $this->getPerson($person);
            $person_id = $person_id['person_id'];

            $statement = $this->dbh->prepare('DELETE FROM restaurants WHERE person_id = :person_id AND restaurant_name = :restaurant_name AND profile_id = :profile_id');
            $statement->bindValue('person_id', $person_id);
            $statement->bindValue('restaurant_name', $restaurant);
            $statement->bindValue('profile_id', $_SESSION['profile_id']);
            $statement->execute();
        }

        public function getPersonRatings($id)   //returns all ratings made by one person based off of the ID of the person
        {
            //session_start();
            $statement = $this->dbh->prepare('SELECT * FROM restaurants WHERE person_id = :person_id AND profile_id = :profile_id');
            $statement->bindValue('person_id', $id);
            $statement->bindValue('profile_id', $_SESSION['profile_id']);
            $statement->execute();
            return $statement->fetchAll(PDO::FETCH_ASSOC); 
        }

        public function getAllRestaurantsFromRatings()  //used to create the restaurantNames DB based off of the ratings(restaurants) DB
        {
            $statement = $this->dbh->prepare("SELECT restaurant_name FROM restaurants");
            $statement->execute();
            return $statement->fetchAll(PDO::FETCH_ASSOC);
        }

        public function checkApproval($id, $name)
        {
            session_start();
            $statement = $this->dbh->prepare("SELECT approve FROM resaurants WHERE person_id = :person_id AND restaurant_name = :restaurant_name AND profile_id = :profile_id");
            $statement->bindValue('person_id', $id);
            $statement->bindValue('restaurant_name', $name);
            $statement->bindValue('profile_id', $_SESSION['profile_id']);
            $statement->execute();
            return $statement->fetch(PDO::FETCH_ASSOC);
        }
        //**************************************RESTAURANT DB**************************************

        
        //**************************************RESTAURANT NAMES DB**************************************
        public function getAllRestaurantNames() //gets all restaurant names from the restaurantNames database
        {
            $statement = $this->dbh->prepare('SELECT restaurant_name FROM restaurantNames');
            $statement->execute();
            return $statement->fetchAll(PDO::FETCH_ASSOC); 
        }

        public function getRestaurantIdByName($name)
        {
            $statement = $this->dbh->prepare('SELECT restaurant_id FROM restaurantNames WHERE restaurant_name = :restaurant_name');
            $statement->bindValue('restaurant_name', $name);
            $statement->execute();
            return $statement->fetch(PDO::FETCH_ASSOC); 

        }

        public function deleteRestaurantFromNames($restaurant)
        {
            $statement = $this->dbh->prepare('DELETE FROM restaurantNames WHERE restaurant_name = :restaurant_name');
            $statement->bindValue('restaurant_name', $restaurant);
            $statement->execute();
        }

        public function insertRestaurant($restaurant)
        {

            try 
            {
                $statement = $this->dbh->prepare("INSERT INTO restaurantNames (restaurant_name) VALUES (:restaurant_name)");
                $statement->bindValue('restaurant_name', $restaurant);
                $statement->execute();
            }
            catch(PDOException $e)  //if it it already exists
            {
                if($e->errorInfo[1] == 1062)
                {
                    //do nothing 
                }
            }
        }
        //**************************************RESTAURANT NAMES DB**************************************

        //**************************************PROFILE DB**************************************
        
        public function addProfile($name, $pass)
        {
            //create profile
            $statement = $this->dbh->prepare("INSERT INTO profiles (profile_name, pass) VALUES (:profile_name, :pass)");
            $statement->bindValue('profile_name', $name);
            $statement->bindValue('pass', $pass);
            $statement->execute();


            session_start();    //log user in
            $statement = $this->dbh->prepare("SELECT profile_id FROM profiles WHERE profile_name = :profile_name");
            $statement->bindValue('profile_name', $name);
            $statement->execute();
            $_SESSION['isLoggedIn'] = true;                    
            $id = $statement->fetch(PDO::FETCH_ASSOC); 
            $_SESSION['profile_id'] = $id['profile_id'];
        }

        public function checkLogin($name, $hash)
        {
            session_start();
            $statement = $this->dbh->prepare("SELECT profile_name FROM profiles WHERE EXISTS (SELECT * FROM profiles WHERE profile_name = :profile_name)");
            $statement->bindValue('profile_name', $name);
            $statement->execute();
            $profileName = $statement->fetch(PDO::FETCH_ASSOC);
            if($profileName == $name)   //if profile exists
            {
                
                $statement = $this->dbh->prepare("SELECT * FROM profiles WHERE profile_name = :profile_name");
                $statement->bindValue('profile_name', $name);
                if($statement->execute() == $hash)  //if the password is correct
                {
                    $statement = $this->dbh->prepare("SELECT profile_id FROM profiles WHERE profile_name = :profile_name");
                    $statement->bindValue('profile_name', $name);
                    $statement->execute();
                    $_SESSION['isLoggedIn'] = true;
                    $id = $statement->fetch(PDO::FETCH_ASSOC); 
                    $_SESSION['profile_id'] = $id['profile_id'];
                }

            }
            else    //create a new profile
            {
                $this->addProfile($name, $hash);
            }

        }

        public function logout()
        {
            session_start();
            $_SESSION['isLoggedIn'] = false;
            $_SESSION['profile_id'] = null;

        }

        //**************************************PROFILE DB**************************************
        
        //**************************************JOIN DB**************************************
        public function join($id)
        {
            $statement = $this->dbh->prepare("SELECT * FROM food LEFT OUTER JOIN payments ON food.restaurant_id = payments.restaurant_id
                LEFT OUTER JOIN restaurant_info ON food.restaurant_id = restaurant_info.restaurant_id
                LEFT OUTER JOIN text_review ON food.restaurant_id = text_review.restaurant_id WHERE food.restaurant_id = :id");
            $statement->bindValue('id', $id);
            $statement->execute();
            return $statement->fetchAll(PDO::FETCH_ASSOC); 

        }

        //**************************************JOIN DB**************************************

        //**************************************FOOD DB**************************************

        public function addFood($name, $gf, $vegan, $kosher)
        {

            $statement = $this->dbh->prepare("INSERT INTO food (restaurant_id, glutenfree, vegan, kosher) VALUES (:restaurant_id, :glutenfree, :vegan, :kosher)");
            $id = $this->getRestaurantIdByName($name);
            $statement->bindValue('restaurant_id', $id['restaurant_id']);            $statement->bindValue('glutenfree', $gf);
            $statement->bindValue('vegan', $vegan);
            $statement->bindValue('kosher', $kosher);
            $statement->execute();
 
        }

        public function addPayments($name, $cash, $card, $check)
        {
            $statement = $this->dbh->prepare("INSERT INTO payments (restaurant_id, cash, card, payCheck) VALUES (:restaurant_id, :cash, :card, :payCheck)");
            $id = $this->getRestaurantIdByName($name);
            $statement->bindValue('restaurant_id', $id['restaurant_id']);            $statement->bindValue('cash', $cash);
            $statement->bindValue('card', $card);
            $statement->bindValue('payCheck', $check);
            $statement->execute();

        }

        public function addInfo($name, $address, $type, $pricing)
        {
            $statement = $this->dbh->prepare("INSERT INTO restaurant_info (restaurant_id, address, type, pricing) VALUES (:restaurant_id, :address, :type, :pricing)");
            $id = $this->getRestaurantIdByName($name);
            $statement->bindValue('restaurant_id', $id['restaurant_id']);
            $statement->bindValue('address', $address);
            $statement->bindValue('type', $type);
            $statement->bindValue('pricing', $pricing);
            $statement->execute();

        }

        public function addTextReview($name, $review)
        {
            session_start();
            
            $statement = $this->dbh->prepare("INSERT INTO text_review (restaurant_id, profile_id, review) VALUES (:restaurant_id, :profile_id, :review)");
            //var_dump($name);
            $id = $this->getRestaurantIdByName($name);
            $statement->bindValue('restaurant_id', $id['restaurant_id']);
            //var_dump($this->getRestaurantIdByName($name));
            // var_dump($id['restaurant_id']);
            $statement->bindValue('profile_id', $_SESSION['profile_id']);
            var_dump($_SESSION['profile_id']);
            $statement->bindValue('review', $review);
            $statement->execute();

        }

        public function deleteEntry($restaurant, $table)
        {
            $statement = $this->dbh->prepare("DELETE FROM $table WHERE restaurant_id = :restaurant_id");
            $id = $this->getRestaurantIdByName($restaurant);
            $statement->bindValue('restaurant_id', $id['restaurant_id']);
            $statement->execute();
            
        }
    }

?>