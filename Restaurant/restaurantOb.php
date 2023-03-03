<?php
    class Restaurant
    {
        public $name;
        private $score;
        private $howManyAttended;
        private $isApproved;
        
        public function __construct($nameOfPlace)
        {
            $this->name = $nameOfPlace;
            $this->score = 0;
            $this->howManyAttended = 0;
            $this->isApproved = true;
            
        }

        public function addToScore($rating)
        {
            $this->score += $rating;
        }

        public function getScore()
        {
            return $this->score;
        }

        public function addAttending()
        {
            $this->howManyAttended++;
        }

        public function getHowManyAttended()
        {
            return $this->howManyAttended;
        }
  
        public function calculateAverage()
        {
            if($this->howManyAttended == 0)
            {
                return 0;
            }
            return $this->score/$this->howManyAttended;
        }

        public function changeApproval($approval)
        {
            if($this->isApproved)
            {
                $this->isApproved = $approval;
                return;
            } 
        }

        public function getApproval()
        {
            return $this->isApproved;
        }
    }


?>