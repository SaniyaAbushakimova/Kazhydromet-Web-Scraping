# Kazhydromet-Web-Scraping

Kazhydromet serves as the national hydrometeorological agency of the Republic of Kazakhstan, offering comprehensive hydrological data sourced from 227 stations distributed across the country. 

The **Kazhydromet-Web-Scraping** automates the retrieval of data from Kazhydromet's Meteorological Database spanning from 01/01/2000 to 30/04/2023. Manually handling this would be extremely time-consuming because the database contains 3.5 GB of **tabular** data, which is a very large number of tables. This process was automated using `Python` and `Selenium` framework.

Here is an overview of the website that was scraped in this project:

* The website URL is: https://www.kazhydromet.kz/ru/. By default, the language is set to Russian, but it can be switched to English.
* Following the guide below, we can access the target database for scraping:

![Guide 1](https://github.com/SaniyaAbushakimova/Kazhydromet-Web-Scraping/assets/81459892/14376122-b314-4628-a7c8-53559cbbdc97)

About the database:

The database contains information about meteorological indices such as Temperature, Partial Pressure, Relative humidity, and another 8 indices. The data is divided by regions (there are 17 regions in Kazakhstan), and by corresponding stations in each region (there are 227 of them). And we need to scrape data from 01/01/2000 to 30/04/2023. The approximate number of entries per table was 8,521 which weights aproximately 800 KB each. Below is a database screenshot with comments.

![Guide 2](https://github.com/SaniyaAbushakimova/Kazhydromet-Web-Scraping/assets/81459892/75b869a0-c5a1-4041-96cd-eaf28f23e29f)

