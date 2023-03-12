/*
In this project, I am exploring, cleaning, and analyzing data on electric vehicles to answer the following questions in Microsoft SQL Server.

    1) Which car has the fastest 0-100 acceleration?
    2) Which has the highest efficiency?
    3) Does a difference in power train effect the range, top speed, efficiency?
    4) Which manufacturer has the most number of models?
    5) How does price relate to rapid charging?
	6) Which car is the most expensive?
	7) Which car is the least expensive?
	8) Which is the best deal for an electric vehicle meeting certain specifications, including the price to charge 200km of driving?

*/



/*                                                     Data Exploration and Cleaning                                                     */
-- Retrieve the field names from the table.
SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'ElectricCarData'

-- How many records are in the table?
SELECT COUNT(*) AS Records FROM ElectricCarData

-- How many unique models are in the table?
SELECT COUNT(DISTINCT Model) AS Models FROM ElectricCarData
-- There is one extra record than unique models.

-- Are there any duplicate models in the table?
SELECT Model, COUNT(*) as Count
FROM ElectricCarData
GROUP BY Model
HAVING COUNT(*) > 1;
-- There are 2 records of the e-Soul 64 kWh.

-- Let's look at those records.
SELECT *
FROM ElectricCarData
WHERE Model = 'e-Soul 64 kWh'
-- The records are identical with the exception of the FastCharge_kmH field
-- I went to https://ev-database.org/car/1154/Kia-e-Soul-64-kWh and found that the fast charge speed was 350 km/hr for that model

-- Delete one of the duplicate records.
DELETE FROM ElectricCarData
WHERE Model = 'e-Soul 64 kWh' AND FastCharge_KmH = 320

-- Update FastCharge_KmH.
UPDATE ElectricCarData
SET FastCharge_KmH = 350
WHERE Model = 'e-Soul 64 kWh'

-- Verify deletion of the duplicate.
SELECT *
FROM ElectricCarData
WHERE Model = 'e-Soul 64 kWh'

-- How many different brands are there in the data.
SELECT COUNT(DISTINCT Brand) AS 'Brand Count' 
FROM ElectricCarData



/*                                                     Data Analysis                                                                  */
-- 1) Which car has the fastest 0-100 acceleration?
SELECT TOP 5 Brand, Model, AccelSec
FROM ElectricCarData
ORDER BY AccelSec ASC
-- Tesla tops the list with it's Roadster reaching 100km/h in 2.1 seconds and it's Model S Performance reaching it in 2.5 seconds.

-- 2) Which has the highest efficiency?
SELECT TOP 5 Brand, Model, Efficiency_WhKm
FROM ElectricCarData
ORDER BY Efficiency_WhKm ASC
-- The Lightyear One is by far the most efficient with 104 watt hours per kilometer. 

-- 3) Does a difference in power train effect the range, top speed, efficiency?
SELECT DISTINCT PowerTrain, ROUND(AVG(TopSpeed_KmH), 2) AS avg_top_speed, ROUND(AVG(Efficiency_WhKm), 2) AS avg_efficiency
FROM ElectricCarData
GROUP BY PowerTrain
-- On average, all wheel drive vehicles have a higher top speed but are less efficient, front wheel drives have the lowest top speed 
-- but are the most efficient, rear wheel drives are situated in the middle.

-- 4) Which manufacturer has the most number of models?
SELECT TOP 5 Brand, COUNT(*) AS Models
FROM ElectricCarData
GROUP BY Brand
ORDER BY Models DESC
-- Tesla leads the list with 13 models followed by Audi with 9 models.

-- 5) How does price relate to rapid charging?
SELECT RapidCharge, ROUND(AVG(PriceEuro), 0) AS Price
FROM ElectricCarData
GROUP BY RapidCharge
-- Cars with the rapid charge feature are more than twice as expensive on average.

-- 6) Which car is the most expensive?
SELECT TOP 5 Brand, Model, PriceEuro
FROM ElectricCarData
ORDER BY PriceEuro DESC
-- The Tesla Roadster is the most expensive vehicle, costing EUR 215,000.

-- 7) Which car is the least expensive?
SELECT TOP 5 Brand, Model, PriceEuro
FROM ElectricCarData
ORDER BY PriceEuro ASC
-- The SEAT Mii Electric is the least expensive vehicle, costing EUR 20,129.

-- 8) Which is the best deal for an electric vehicle meeting certain specifications, including the price to charge 200km of driving?
--    Specifications: The vehicle must have rapid charging and a range of at least 300km.
-- According to https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Electricity_price_statistics,
-- The average price of electricity in the EU was EUR .2525 per KwH in the first half of 2022.
-- I will assume this price in my query and exlude costs for insurance, repairs, and other miscellaneous costs.
SELECT TOP 5 Brand, Model, Range_Km, TopSpeed_KmH, PriceEuro, ROUND((((Efficiency_WhKm * 200000) / 1000) * .2525) + PriceEuro, 0) AS  total_cost
FROM ElectricCarData
WHERE RapidCharge = 'Yes' AND Range_Km >= 300
ORDER BY total_cost ASC
-- The Renault Zoe ZE50 R110 tops the list as the best deal according to the specifications with a buying price of EUR 31184 and a total cost of 39517.
-- If you want a car with a longer range and a higher top speed, then I would recommend the second cheapest car on the list, the Volkswagen ID.3 Pro.




