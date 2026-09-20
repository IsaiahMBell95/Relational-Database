# Relational-Database

### What This Project Does

This project uses relational database along with different applications and API to create an e-commerce website. The base of this project is creating different tables (User, Product, Order). From there we create a schema for each, which helps organize, group and manage those tables. Lastly, we create endpoints for the users, products and orders. This allows us to add, delete and update our tables.

### Dependencies Used
  - Flask
  - SQLAlchemy
  - Marshmallow

### Applications Used
  - MYSQL
  - Python

### Breakdown

<img width="1735" height="980" alt="image" src="https://github.com/user-attachments/assets/7b21e17b-a3ca-4e09-9444-86358b4e8741" />

Here we have the imports used and where we essentially actuivate all our dependencies.

<img width="1660" height="1325" alt="image" src="https://github.com/user-attachments/assets/ea3789f1-5157-45fd-bb51-844fddf20b16" />

This is where I create the tables for User, Product and Orders. I assigned each table an ID that uniquely identifies each using the primary key function. From there I created columns with the required information we want to collect for each.

<img width="1592" height="1053" alt="image" src="https://github.com/user-attachments/assets/a8e0cf39-894d-4d9e-acb6-68c1645540a0" />

This section is where we create the schemas. The schemas allow us to choose the fields we want to input that updates the tables in SQL. The model for each will be the the table we are grabbing the info from and we are using include_fk to read the user_id.

<img width="937" height="499" alt="image" src="https://github.com/user-attachments/assets/ca4200f4-f596-457f-821d-912dc220c59a" />

I initialized the schemas. Each schema will be initalized for just one thing and also for many. Example user_schema is to adjust just the user, while users_schema is to adjust multiple users. db.create_all creates all the tables in MySQL.

<img width="1763" height="951" alt="image" src="https://github.com/user-attachments/assets/e404ee9b-1801-4358-85fd-fbb14a79cb17" />

<img width="1466" height="1088" alt="image" src="https://github.com/user-attachments/assets/52a70782-d5be-4d2d-bb82-cc4e0c6c4507" />

<img width="1340" height="1480" alt="image" src="https://github.com/user-attachments/assets/01519f93-687d-407c-8615-5d5223fd5483" />

<img width="1493" height="1353" alt="image" src="https://github.com/user-attachments/assets/76301f24-4b43-4ed6-b64c-3f6c5bbcccbd" />



Here we create different endpoints for the User, Product and Order. Each endpoint we have to route to the schema you are using (User endpoint to Userschema). The "methods" will be dependent based on what you're looking to change. For example, getting users will require you to use the GET method. Both the user and products endpoint will follow the same inputs since you are only retrieving one of the schemas. The order endpoints will require you to combine multiple schemas.





