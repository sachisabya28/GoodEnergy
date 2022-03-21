## GoodEnergy

Input Data:
```bash
{
  "postal_code": 76648,
  "city": "Lenyascheid",
  "street": "Adolf-Reichwein-Str.",
  "house_number": "44-56",
  "yearly_kwh_consumption": 1000
}
```

Expected Response Data:
```bash
{
    "grid_fees": 1.81,
    "kwh_price": 0.5,
    "total_price": 503.69,
    "unit_price": 1.88
}
```

• The project must have an API. <br />
• The implementation must respect all the rules. <br />
• The project must be protected against errors. <br />
• The project must have tests. <br />
• The project must be uploaded to a Bitbucket/Gitlab/Github account with free access. <br />
• The project must have a README file explaining the setup and all the logic/tech stack decisions behind it. <br />

## Design Pattern
*** 
APIs created using Flask, sqlite, FlaskREST, flask_sqlalchemy
Database query is acheived using Flask ORM. 

APIs:

Load the CSV data to Location database
1. http://0.0.0.0:8000/upload > POST
Make sure to pass key as file and .csv <br />
NOTE: Data load may take time as it has huge amount of data

INPUT : 
file: <file.csv>

2. http://0.0.0.0:8080/userdata?postal_code=postal_code&city=city&street=Torstraße&house_number=house_number&yearly_kwh_consumption=yearly_kwh_consumption > GET

INPUT :  
```bash
{
  "postal_code": 76648,
  "city": "Lenyascheid",
  "street": "Adolf-Reichwein-Str.",
  "house_number": "44-56",
  "yearly_kwh_consumption": 1000
}
```
RESPONSE: 
```bash
{
    "grid_fees": 1.81,
    "kwh_price": 0.5,
    "total_price": 503.69,
    "unit_price": 1.88
}
```
***

###### Start the app ######

```bash
docker-compose up --detach
```


