## GoodEnergy

Input Data:
{
  "postal_code": 76648,
  "city": "Lenyascheid",
  "street": "Adolf-Reichwein-Str.",
  "house_number": "44-56",
  "yearly_kwh_consumption": 1000
}

Expected Response Data:
{
    "grid_fees": 1.81,
    "kwh_price": 0.5,
    "total_price": 503.69,
    "unit_price": 1.88
}

• The project must have an API.
• The implementation must respect all the rules.
• The project must be protected against errors.
• The project must have tests.
• The project must be uploaded to a Bitbucket/Gitlab/Github account with free access.
• The project must have a README file explaining the setup and all the logic/tech stack decisions behind it.

## Design Pattern
*** 
APIs created using Flask, sqllite, FlaskREST, flask_sqlalchemy
Databse query is acheived using Flask ORM. 

APIs:

Load the CSV data to Location database
1. http://127.0.0.1:8000 > POST
Make sure to pass key as file and .csv 
NOTE: Data load may take time as it has huge amount of data

INPUT : 
file: <file.csv>

2. http://127.0.0.1:8000/userdata > POST

INPUT :  

{
  "postal_code": 76648,
  "city": "Lenyascheid",
  "street": "Adolf-Reichwein-Str.",
  "house_number": "44-56",
  "yearly_kwh_consumption": 1000
}

RESPONSE: 

{
    "grid_fees": 1.81,
    "kwh_price": 0.5,
    "total_price": 503.69,
    "unit_price": 1.88
}

***

###### Setup the app ######

```bash
git clone 
cd <root-folder>
sh setup.sh
sh.start_app.sh
```


###### Unitest ######

```bash
cd test
python test_api.py
```
