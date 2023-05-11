CREATE TABLE `person` (
  `person_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`person_id`));
	
/////////////////////////////////////////////////////

CREATE TABLE `restaurants` (
  `person_id` INT NOT NULL,
  `person_name` VARCHAR(128) NOT NULL,
  `restaurant_name` VARCHAR(128) NOT NULL,
  `approve` BIT,
  `rating` INT NOT NULL,
  PRIMARY KEY (`person_id`),
  INDEX `fk_person_person_idx` (`person_id` ASC),
  CREATE UNIQUE INDEX unique_restuarant_description ON restaurants(restaurant_name);
  CONSTRAINT `fk_person_id`
    FOREIGN KEY (`person_id`)
    REFERENCES `person` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CREATE UNIQUE INDEX unique_restuarant_description ON restaurants(restaurant_name);
  CONSTRAINT `fk_profile_id`
    FOREIGN KEY (`profile_id`)
    REFERENCES `profiles` (`profile_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    );

/////////////////////////////////////////////////////

CREATE TABLE `restaurantNames` (
  `restaurant_id` INT NOT NULL,
  `restaurant_name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`restaurant_id`),
  CREATE UNIQUE INDEX unique_restuarant_id ON restaurantNames(restaurant_id);
  CREATE UNIQUE INDEX unique_restuarant_description ON restaurantNames(restaurant_name););


/////////////////////////////////////////////////////

CREATE TABLE `food` (
  `restaurant_id` INT NOT NULL,
  `glutenfree` BIT,
  `vegan` BIT,
  `kosher` BIT,
  PRIMARY KEY (`restaurant_id`),
  CONSTRAINT `fk_food_restaurant_id`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `restaurantnames` (`restaurant_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE UNIQUE INDEX `restaurant_id_description` ON `payments` (`restaurant_id`);

/////////////////////////////////////////////////////

CREATE TABLE `payments` (
  `restaurant_id` INT NOT NULL,
  `cash` BIT,
  `card` BIT,
  `payCheck` BIT,
  PRIMARY KEY (`restaurant_id`),
  CONSTRAINT `fk_payments_restaurant_id`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `restaurantnames` (`restaurant_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE UNIQUE INDEX `restaurant_id_description` ON `payments` (`restaurant_id`);


/////////////////////////////////////////////////////
CREATE TABLE `restaurant_info` (
  `restaurant_id` INT NOT NULL,
  `address` varchar(256),
  `type` varchar(128),
  `princing` INT,
  PRIMARY KEY (`restaurant_id`),
  CONSTRAINT `fk_info_restaurant_id`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `restaurantnames` (`restaurant_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE UNIQUE INDEX `restaurant_id_description` ON `restaurant_info` (`restaurant_id`);


/////////////////////////////////////////////////////
CREATE TABLE `text_review` (
  `restaurant_id` INT NOT NULL,
  `profile_id` INT NOT NULL,
  `review` VARCHAR(256),
  PRIMARY KEY (`restaurant_id`, `profile_id`),
  CONSTRAINT `fk_text_review_restaurant_id`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `restaurantnames` (`restaurant_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_text_review_profile_id`
    FOREIGN KEY (`profile_id`)
    REFERENCES `profiles` (`profile_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION    
);


CREATE TABLE `profiles` (
  `profile_id` INT NOT NULL,
  `profile_name` varchar(128),
  `pass` varchar(128),
  PRIMARY KEY (`profile_id_id`),
);

CREATE UNIQUE INDEX `profile_id_unique` ON `profiles` (`profile_id`);