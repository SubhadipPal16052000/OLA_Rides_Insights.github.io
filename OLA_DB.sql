SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

select * from "cleaned_OLAride_data";

--1. Retrieve all successful bookings.

create view successful_bookings as
SELECT *
FROM "cleaned_OLAride_data"
WHERE "Booking_Status" = 'Success';

select * from successful_bookings;

--2. Find the average ride distance for each vehicle type.
create view average_ride_distance_each_vehicle as
SELECT "Vehicle_Type", AVG("Ride_Distance") AS average_distance
FROM "cleaned_OLAride_data"
GROUP BY "Vehicle_Type";

select * from average_ride_distance_each_vehicle;

--3. Get the total number of cancelled rides by customers.

create view cancelled_rides_by_customers as
SELECT SUM("Is_Canceled_by_Customer") AS total_customer_cancellations
FROM "cleaned_OLAride_data";

select * from cancelled_rides_by_customers;

--4. List the top 5 customers who booked the highest number of rides.

create view booked_the_highest_rides as
SELECT "Customer_ID", COUNT(*) AS number_of_rides
FROM "cleaned_OLAride_data"
GROUP BY "Customer_ID"
ORDER BY number_of_rides DESC
LIMIT 5;

select * from booked_the_highest_rides;

--5. Get the number of rides cancelled by drivers due to personal and car-related issues.

create view cancelled_by_drivers_due_to_p_c_issues as
SELECT COUNT(*) AS drivers_cancellation_count
FROM "cleaned_OLAride_data"
WHERE "Driver_Cancellation_Reason" = 'Personal & Car related issue';

select * from cancelled_by_drivers_due_to_p_c_issues;

--6. Find the maximum and minimum driver ratings for Prime Sedan bookings.

create view prime_sedan_min_max_rating as
SELECT
    MAX("Driver_Ratings") AS max_rating,
    MIN("Driver_Ratings") AS min_rating
FROM "cleaned_OLAride_data"
WHERE "Vehicle_Type" = 'Prime Sedan';

select * from prime_sedan_min_max_rating;

--7. Retrieve all rides where payment was made using UPI.

create view upi_payment as
SELECT *
FROM "cleaned_OLAride_data"
WHERE "Payment_Method" = 'UPI';

select * from upi_payment;

--8. Find the average customer rating per vehicle type.

create view per_vehicle_avg_customer_rating as
SELECT "Vehicle_Type", AVG("Customer_Rating") AS average_customer_rating
FROM "cleaned_OLAride_data"
GROUP BY "Vehicle_Type";

select * from per_vehicle_avg_customer_rating;

--9. Calculate the total booking value of rides completed successfully.

create view total_booking_successfully_complete as
SELECT SUM("Booking_Value") AS total_completed_value
FROM "cleaned_OLAride_data"
WHERE "Booking_Status" = 'Success';

select * from total_booking_successfully_complete;

--10. List all incomplete rides along with the reason.

create view incomplete_rides_with_reason as
SELECT "Booking_ID", "Incomplete_Rides_Reason"
FROM "cleaned_OLAride_data"
WHERE "IsIncomplete" = 1;

select * from incomplete_rides_with_reason;


--=================================================================
--=================================================================
create view number_of_rides_booking_per_hour_in_day as
SELECT
    TO_CHAR("Booking_Timestamp", 'Day') AS day_of_week,
    EXTRACT(HOUR FROM "Booking_Timestamp") AS booking_hour,
    COUNT(*) AS number_of_rides
FROM
    "cleaned_OLAride_data"
GROUP BY
    day_of_week,
    booking_hour
ORDER BY
    number_of_rides DESC;

select * from number_of_rides_booking_per_hour_in_day;


