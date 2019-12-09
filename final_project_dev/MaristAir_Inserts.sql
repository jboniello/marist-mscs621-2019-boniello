
-- This a file containing inital data population of some of the static tables in the MaristAir db 
-- The other tables are dynamically populated by the application (examples in ApplicationSQL_dynamic.txt)


-- AIRLINE INSERST --
INSERT INTO `MaristAir`.`Airline` (`airline_id`, `airline_name`, `airline_addr`, `airline_phone`, `airline_email`) VALUES ('1', 'United', 'PO Box 06649 Chicago IL, 60606-0649', '18008648331', 'eservice@united.com');
INSERT INTO `MaristAir`.`Airline` (`airline_id`, `airline_name`, `airline_addr`, `airline_phone`, `airline_email`) VALUES ('2', 'JetBlue', 'PO Box 17435 Salt Lake City Utah, 84117', '18005382583', 'DearJetBlue@jetblue.com');
INSERT INTO `MaristAir`.`Airline` (`airline_id`, `airline_name`, `airline_addr`, `airline_phone`, `airline_email`) VALUES ('3', 'American', 'PO Box 619616 DFW Airport TX, 75261', '18004337300', 'Customer.Relations@aa.com');

-- CITY INSERTS --
INSERT INTO `MaristAir`.`City` (`city_id`, `city_name`, `city_state`, `city_lat`, `city_long`) VALUES ('1', 'New York City', 'New York', '40.6413', '73.7781');
INSERT INTO `MaristAir`.`City` (`city_id`, `city_name`, `city_state`, `city_lat`, `city_long`) VALUES ('2', 'Los Angeles', 'California', '33.9416', '118.4085');
INSERT INTO `MaristAir`.`City` (`city_id`, `city_name`, `city_state`, `city_lat`, `city_long`) VALUES ('3', 'Orlando', 'Florida', '28.4312', '81.3081');
INSERT INTO `MaristAir`.`City` (`city_id`, `city_name`, `city_state`, `city_lat`, `city_long`) VALUES ('4', 'Denver', 'Colorado', '39.8561', '104.6737');
INSERT INTO `MaristAir`.`City` (`city_id`, `city_name`, `city_state`, `city_lat`, `city_long`) VALUES ('5', 'Austin', 'Texas', '30.1941', '97.6711');
INSERT INTO `MaristAir`.`City` (`city_id`, `city_name`, `city_state`, `city_lat`, `city_long`) VALUES ('6', 'Chicago', 'Illinois', '41.9742', '87.9073');
INSERT INTO `MaristAir`.`City` (`city_id`, `city_name`, `city_state`, `city_lat`, `city_long`) VALUES ('7', 'St. Louis', 'Missouri', '38.7503', '90.3755');
INSERT INTO `MaristAir`.`City` (`city_id`, `city_name`, `city_state`, `city_lat`, `city_long`) VALUES ('8', 'Salt Lake City', 'Utah', '40.7899', '111.9791');


-- OPTIONS INSERTS --
INSERT INTO `MaristAir`.`Options` (`option_id`, `option_name`, `option_price`) VALUES ('1', 'Meal Purchase', '20');
INSERT INTO `MaristAir`.`Options` (`option_id`, `option_name`, `option_price`) VALUES ('2', 'Commodity Purchase', '10');
INSERT INTO `MaristAir`.`Options` (`option_id`, `option_name`, `option_price`) VALUES ('3', 'Pet Carry-On', '100');
INSERT INTO `MaristAir`.`Options` (`option_id`, `option_name`, `option_price`) VALUES ('4', 'Early Boarding', '30');
INSERT INTO `MaristAir`.`Options` (`option_id`, `option_name`, `option_price`) VALUES ('5', 'Checked Luggage', '40');
INSERT INTO `MaristAir`.`Options` (`option_id`, `option_name`, `option_price`) VALUES ('6', 'Extra Checked Luggage', '20');


-- PLANE INSERTS --
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('1', '1', 'B747', '416');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('2', '1', '7B47', '416');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('3', '2', 'A320', '162');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('4', '2', 'A320', '162');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('5', '2', 'E190', '100');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('6', '2', 'A321', '200');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('7', '2', 'A321', '200');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('8', '2', 'A321', '200');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('9', '3', 'A321', '200');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('10', '3', 'A321', '200');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('11', '3', 'A321', '200');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('12', '3', 'B737', '451');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('13', '3', 'B737', '451');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('14', '1', 'B737', '451');
INSERT INTO `MaristAir`.`Plane` (`plane_id`, `airline_id`, `plane_model`, `plane_seats`) VALUES ('15', '1', 'B737', '451');

