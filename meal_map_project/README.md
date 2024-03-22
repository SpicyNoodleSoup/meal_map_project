

Name of web application: Meal Map


The objective of our application is to create a
centralised platform where food lovers and
restaurant owners can exchange their views,
share experiences and explore the culinary
scene.

Users will be able to view different restaurants,
leave reviews with a rating (1-5) and share their
thoughts, restaurant owners will be able to use
this platform to showcase their restaurant by
adding photos, social links and the location of
their restaurant while being able to understand
what their customers think through the reviews.
The application will serve as a
vibrant community hub from Three Michelin
Star restaurant to your local Takeaway.


Lab Group 10, Team A
Abdisalam Abukar 2618966A
Luke Latta 2787729L
Xiaoshi Chen 2742059C
Olivia Long 2774536L
Aidan Yip 2789553Y

GitHub URL for the app: https://github.com/WADteam10a/meal_map_project
PythonAnywhere URL for the app: https://abdisalamabuker.pythonanywhere.com/

Instructions for deploying Meal Map on computer:
git clone https://github.com/WADteam10a/meal_map_project.git (inside a directory of your choice)
cd meal_map_project/meal_map_project
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python populate_meal_map.py
python manage.py runserver
