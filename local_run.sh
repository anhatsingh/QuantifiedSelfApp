#! /bin/sh

if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No virtual env. Please run setup.sh first"
    exit N
fi

. .env/bin/activate
export FLASK_ENV=development
python3 app.py
deactivate