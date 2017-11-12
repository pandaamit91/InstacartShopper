# InstacartShopper

Running part 1:
I have used Django web framework for this part of the question. Please follow the instructions below to setup Django and run the webserver.
1. Install Python
2. Install pip 
   $pip install -U pip
3. Install dependencies
	a. Install Django 
   $sudo pip install Django
4. Running server
   cd <Directory to webapp folder>
   python manage.py runserver 0.0.0.0:8000
5. Access webapp folder in browser
   http://localhost:8000/

Running part 2:
Please update the location to the sqlite DB file in `instacart.py` file and `make sure that there is no other client connection open to the Database` while you are running the script as it will cause the DB to be locked.
Using python 2.7.

Example run:
python instacart.py '2014-12-20' '2014-12-20'

Explanation of workflow:
1. I am creating an auxillary table which can store data for future reuse. 
2. During each execution, I am fetching data from auxillary table first, which has derived data from previous runs. 
3. Next, I identify if we need to query the base (applicants) table for any of the missing data for which no query has been run so far. 
  a) If yes, I get data from the base table, merge it with auxillary table data for computation and update auxillary table with the new data at the same time.
  b) If not, we have all the data that we need for our final computation from the auxillary table.
6. Finally, I compute the week wise grouping and print the result.

Assumptions:
1. Applicants data does not get modified, and hence the derived data in the auxillary table is suitable for future re-use
2. It is ok to create and update an auxillary table (for faster re-computation) :)



