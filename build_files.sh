
set -e 

echo "Building the project..."
python3 -m pip install -r requirements.txt

echo "Make Migration..."
python3 manage.py makemigrations

echo "Apply Migration..."
python3 manage.py migrate

echo "Collect Static..."
python3 manage.py collectstatic --noinput
