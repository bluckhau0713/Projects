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
            $statement = $this->dbh->prepare("INSERT INTO person (person_name) VALUES (:person_name)");
            $statement->bindValue('person_name', $name);
            $statement->execute();
        }

        public function getPerson($person)
        {
            $statement = $this->dbh->prepare("SELECT person_id FROM person WHERE person_name = :person_name");
            $statement->bindValue('person_name', $person);
            $statement->execute();
            return $statement->fetch(PDO::FETCH_ASSOC);
        }

        public function getPeopleGoing()    //gets everyone from the person DB into an array with their ID's and Name's
        {
            $statement = $this->dbh->prepare('SELECT * FROM person');
            $statement->execute();
            return $statement->fetchAll(PDO::FETCH_ASSOC);            
        }

        //**************************************PERSON DB**************************************


        //**************************************RESTAURANT DB**************************************
        public function addRating($person, $restaurant, $likes, $rating)
        {
            //need to add if already exists, update maybe do in the addRating.php
            $person_id = $this->getPerson($person);
            $person_id = $person_id['person_id'];
            $statement = $this->dbh->prepare("INSERT INTO restaurants (person_id, person_name, restaurant_name, approve, rating) VALUES (:person_id, :person_name, :restaurant_name, :approve, :rating)");
            $statement->bindValue('person_id', $person_id);
            $statement->bindValue('person_name', $person);
            $statement->bindValue('restaurant_name', $restaurant);
            $statement->bindValue('approve', $likes);
            $statement->bindValue('rating', $rating);
            $statement->execute();
            syslog(LOG_INFO, "$person_id, $person, logged for $restaurant, with an approval of $likes, and rated $rating");
        }

        public function removeRating($person, $restaurant)  //deletes a rating from the restaurants DB
        {
            $person_id = $this->getPerson($person);
            $person_id = $person_id['person_id'];

            $statement = $this->dbh->prepare('DELETE FROM restaurants WHERE person_id = :person_id AND restaurant_name = :restaurant_name');
            $statement->bindValue('person_id', $person_id);
            $statement->bindValue('restaurant_name', $restaurant);
            $statement->execute();
        }

        public function getPersonRatings($id)   //returns all ratings made by one person based off of the ID of the person
        {
            $statement = $this->dbh->prepare('SELECT * FROM restaurants WHERE person_id = :person_id');
            $statement->bindValue('person_id', $id);
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
            $statement = $this->dbh->prepare("SELECT approve FROM resaurants WHERE person_id = :person_id AND restaurant_name = :restaurant_name");
            $statement->bindValue('person_id', $id);
            $statement->bindValue('restaurant_name', $name);
            $statement->execute();
            return $statement->fetch(PDO::FETCH_ASSOC);
        }
        //**************************************RESTAURANT DB**************************************

        
        //**************************************RESTAURANT NAMES DB**************************************
        public function getAllRestaurantNames() //gets all restaurant names from the restaurantNames database
        {
            $statement = $this->dbh->prepare('SELECT restaurant_name FROM restaurantNames ');
            $statement->execute();
            return $statement->fetchAll(PDO::FETCH_ASSOC); 
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


        //WIP WIP WIP WIP WIP WIP WIP WIP WIP
        public function alterRating($person, $restaurant, $column)  
        {
            $person_id = $this->getPerson($person);
            $person_id = $person_id['person_id'];
            
            $statement = $this->dbh->prepare('');
            $statement->bindValue('person_id', $person_id);
            $statement->bindValue('restaurant_name', $restaurant);
            $statement->execute();
        }
        //WIP WIP WIP WIP WIP WIP WIP WIP WIP
    }

?>