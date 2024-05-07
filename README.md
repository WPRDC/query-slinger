# PYTHON SCRIPTS FOR RUNNING SQL QUERIES ON CKAN TABLES

This README file guides you through installing Python and the necessary libraries to learn the basics of running SQL queries through API calls on data tables on a CKAN instance. (It's hard-coded to query the WPRDC open data portal, but the queried site may be changed.)

This README concludes with a script that facilitates editing SQL queries and running them for easy data analysis.

## GETTING STARTED WITH PYTHON

Everything below assumes you have a Python interpreter installed on your computer. If you are working on a Mac, you should just be able to open a terminal window and type 
`> python -V`
to confirm that you have Python installed. Otherwise you'd need to install it. One option is to download a Python installer from python.org; this has the advantage that it will automatically install the pip package manager, which you need to install the ckanpi Python library.

If you have Python and the pip package manager installed, you can type

`> python -m pip install ckanapi`

to install the ckanapi library.

Also run

`> python -m pip install tabulate`

to install a library for pretty-printing tables.


If you need to install pip, there are instructions here:
https://pip.pypa.io/en/stable/installation/


## RUNNING SCRIPTS FROM THE COMMAND LINE

Normally, you can run a Python script (in this case the one in the file called `simple_sql_queries.py`) from the command line by typing 

`> python simple_sql_queries.py`

and the results (basically anything the script says to print, as well as any errors/exceptions the script encounters) will be printed to your screen.

## THE PYTHON REPL

If you want to enter the interactive REPL (Read-Eval-Print-Loop) add the "i" flag, like this:

`> python -i simple_sql_queries.py`

That will do exactly the same thing, but at the end, it starts you in the REPL (you'll know you're in the REPL when you see a >>> prompt), so you can type something like `query`, hit return, and get the value of the query variable.

You can also type
`>>> query = 'SELECT * FROM some_table LIMIT 5'`

And then

`>>> query_small_resource(query)`

And you'll get the full list of results printed in the REPL.

To exit the REPL, you can 1) hit Control-D or 2) type `quit()` or `exit()`.

More about the REPL here: https://realpython.com/python-repl/

## ALTERNATIVES TO THE COMMAND LINE AND PYTHON REPL

There are definitely other ways of editing/running Python scripts. For instance, some people 1) use Python IDEs (Integrated Developer Environments) like PyCharm (a non-free product) or 2) use Jupyter notebooks (free and open source). See https://jupyter.org/ for instructions on installing/using Jupyter.

## INTRODUCTION TO RUNNING CKAN QUERIES FROM PYTHON

Read the `simple_sql_queries.py` script and run it, to see it in action! Comments in the script explain how it works.

## MORE ADVANCED QUERIES

`more_sql_queries.py` introduces a generalized `query_resource()` function that can use multiple API calls to pull records from data tables on the WPRDC data portal.

## INTERACTIVE QUERY EDITOR/RUNNER

To use the interactive query terminal, run 

`> python -i interactive.py

You should see some explanatory text and the triple prompt of the Python REPL.

Enter 

`> tab(run(q))`

to run the query preloaded in `q` and print the results in tabular format.

Enter 

`> q`

to see the preloaded query.

Assign whatever query you want to run to `q`,

`> q = 'SELECT "Breed" FROM "f8ab32f7-44c7-43ca-98bf-c1b444724598" WHERE "DogName" = \'ROVER\' '

and run it with the 

`> tab(run(q))`

command.

One last trick:

`>>> write_to_csv('rover.csv', run(q))`

will write the results of the run query to a CSV file named `rover.csv`.
