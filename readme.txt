A brief overview of how our code is structured:
- forms.py leverages WTForms to define the form objects on our website
- models.py defines how data stored in our database can be mapped to Python objects
- app.py is the main file that sets up the app, defines views and URLs mappings
- anonymous-phrases.txt is the list of key phrases used in retrieving the data
- anonymous.txt is the sample JSON data retrieved from Google API and ready to be parsed.
- dataRetriever.py retrieves and parse data from Google API into a csv file ready to upload to the VM.
- anonsdb folder: our data stored in csv format as well as .sql and .sh files to create and set up the database
- static folder: images and .css file to modify the static layout (including background color, font, and the browser icon) 
- templates folder: all the .html files used to modify user interface, web form layout, and interactive graph layout

How to compile, set up, deploy, and use our system:

1. Download and unzip anonymousSourcing-master.zip in the VM shared folder

2. Run setup.sh from the folder anonymousSourcing-master/anonsdb in your VM (terminal command: ./setup.sh) to create and load the database

3. Install pygal (terminal command: sudo pip install pygal)

4. Run app.py from the folder anonymousSourcing-master (terminal command: python app.py)

5. Go to http://localhost:5000/ in your browser and the set up is complete (refer to the screen-shot in our final report for more details)

6. To access the SQL database within the VM, type the command "psql anons"

Any limitations in our current implementation:

We want to allow users to be able to download a csv file with the query output after they submit the web form. However, we cannot achieve this since this requires us to write a file in the VM, yet we do not have the permission.
