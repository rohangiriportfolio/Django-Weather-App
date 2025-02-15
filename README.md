# 🌦️ Weather App ---

## 📝 Overview:

This Weather App offers weather forecasts by past weather data using Django, Prophet, and Open-Meteo, with various icons representing different weather parameters.

## 🌟 Features:

📊 Past Data: Retrieves historical weather from Open-Meteo.

📈 Forecasts: Predicts trends using Prophet.

💻 UI: Intuitive interface with real-time updates.

## 🛠️ Tech Stack:

🐍 Django (Python) for the backend

📉 Prophet for forecasting

🌐 Open-Meteo for weather data

🎨 Custom weather icons

## ⚙️ Setup & Usage:

🐍 Use a virtual environment for dependencies.

🚀 Launch the app to explore forecasts.

## 🧩 API Integration:

🌐 Open-Meteo: Provides past weather data.

📊 Prophet: Produces forecasts from historical trends.

## 💡 Contributions:

💬 Open to pull requests and discussions for improvements.



# COMMANDS ---

    //  1. OPEN AWS.AMAZON.COM -> SIGNIN USING CREDENTIALS -> SEARCH EC2 -> SELECT INSTANCE FROM LEFT BAR -> LAUNCH INSTANCE BY GIVING NAME, KEY-PAIR AND ALLOWING SSH, HTTP, HTTPS TRAFFIC UNDER CREATE SECURITY GROUP.
    //  2. SELECT THE CREATED INSTANCE AND UNDER SECURITY TAB CLICK ON THE SECURITY GROUP -> UNDER INBOUND RULES CLICK EDIT INBOUND RULES -> ADD 2 RULES -> SELECT TYPE AS CUSTOM TCP FOR BOTH AND GIVE PORT RANGE 8000 AND 8080 FOR TWO RULES -> IN SERCH TAB SELECT 0.0.0.0/0 FOR BOTH OF THE RULES -> SAVE RULES.
    //  3. CHANGE "ALLOWED_HOSTS = ['*']" UNDER SETTINGS.PY BY OPENING THE FILE AS "NANO SETTINGS.PY
    //  4. CONNECT THE INSTANCE FOR RUNNING BACK-END SERVER -> RUN THE FOLLOWING COMMANDS.
    
    1  sudo yum update -y  // FOR UPDATING AND UPGRADING PRE-INSTALLED PACKAGES
    2  sudo yum upgrade -y 
    3  mkdir Project  // CREATE A DIRECTORY FOR STORING THE PROJECT
    4  ls  // LIST THE CONTENT OF THE DIRECTORY
    5  cd Project  // MOVE TO THE DIRECTORY
    6  sudo yum install git -y  // INSTALLING GIT FOR CLONING THE PROJECT REPO
    7  git clone https://github.com/rohangiriportfolio/Django-Weather-App  // CLONING FROM GITHUB REPO
    8  ls
    9  cd Django-Weather-App  
    10  ls
    11  sudo yum install python3-pip -y  // INSTALLING PYTHON & PIP
    12  pip install virtualenv  // INSTALLING VIRTUAL ENVIRONMENT FOR RUNNING DJANGO SERVER
    13  python3 -m virtualenv djangoEnv  // CREATING VIRTUAL ENVIRONMENT NAMED DJANGOENV
    14  ls
    15  source djangoEnv/bin/activate  // ACTIVATING THE CREATED ENVIRONMENT
    16  pip install openmeteo-requests  // INSTALLING NECESSARY PACKAGES FOR RUNNING THE WEB APP
    17  pip install requests-cache retry-requests numpy pandas
    18  pip install prophet  // INSTALLING THE DL MODEL NEURAL PROPHET
    19  cd Backend
    20  ls
    21  pip install django  // INSTALLING DJANGO AND CORS
    22  pip install django-cors-headers
    23  python manage.py runserver 0.0.0.0:8000  // RUNNING THE SERVER AT PORT 8000
    24  curl ifconfig.me
    25  ss -tulnp | grep 8000

    //  5. CONNECTING ANOTHER SHELL FOR SAME INSTANCE FOR RUNNING FRONT-END -> MOVING TO SAME DIRECTORY CREATED EARLIER.


    27  cd Project
    28  ls
    29  cd Django-Weather-App
    30  ls
    31  cd Frontend
    32  ls
    33  python3 -m http.server 8080 // RUNNING THE FRONT-END AT PORT 8080
    34  history  // FOR CHECKING COMMAND HISTORY
