# TMFL: Tata Motors Finance Ltd.

## Project Setup
### Step 1: Clone the repository
### Step 2: Install all the requirements by using command
> pip install -r requirements.txt
### Step 3: Configure the Database or you can use the default Database
### Step 5:Apply the migrations
>python manage.py migrate
### Step 6: Run the server
> python manage.py runserver 8000


### Run the testcases
> python manage.py test

load default data
python manage.py loaddata seed/admin.json
python manage.py loaddata seed/auth_user.json


test with first api
http://127.0.0.1:8000/api-token-auth/

{
    "username":"admin@gmail.com",
    "password":"Admin@12"
}


postman link 

https://www.getpostman.com/collections/d328662c16fb329a7c1e