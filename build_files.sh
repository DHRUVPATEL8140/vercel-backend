echo "Building the project..."
python3.13 -m pip install -r requirements.txt
echo "Make Migration..."
python3.13 manage.py makemigrations
python3.13 manage.py migrate
echo "Collect Static..."
python3.13 manage.py collectstatic --noinput