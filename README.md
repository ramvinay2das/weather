# Weather Forecast
This is a Django based weather forecasting application which is using openweathermap api and sqlite database is used in this which is a file based db.

## How to run this application?
### Prerequiste
* Python
* pip 

#### Step 1
Download/git clone this repository in your system

#### Step 2(optional)
Create a Virtual Environment for this application and activate that virtual env
if you are creating using Conda
```
conda create --name weather python=3.7
activate weather
```

#### Step 3
Open cmd in current working directory of weather which is created after git clone/download and write command
```
pip install -r requirements.txt
```

#### step 4
After pip install in cmd write
```
python manage.py runserver
```
above command will launch your application in localhost at port 8000, http://127.0.0.1:8000/
