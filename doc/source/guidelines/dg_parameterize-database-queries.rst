.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Parameterize Database Queries
=============================

Often we write code that interacts with a database using parameters
provided by the application's users. These parameters include
credentials, resource identifiers and other user-supplied data.

Care must be taken when dynamically creating database queries to
prevent them being subverted by user supplied malicious input, this is
generally referred to as SQL injection (SQLi). SQL injection works because the
user input changes the logic of the SQL query, resulting in behaviour
that is not intended by the application developer.

The results of a successful SQL injection attack can include
disclosure of sensitive information such as user passwords, modification or
deletion of data, and gaining execution privileges, which would allow
an attacker to run arbitrary commands on the database server.

SQL injection can typically be mitigated by using some combination of
`prepared statements <https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet#Defense_Option_1:_Prepared_Statements_.28Parameterized_Queries.29>`__
, `stored procedures <https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet#Defense_Option_2:_Stored_Procedures>`__ and
`escaping <https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet#Defense_Option_3:_Escaping_All_User_Supplied_Input>`__
of user supplied input. Most secure web applications will use all three
and we have described their use below.

Code Examples
-------------

SQLAlchemy
~~~~~~~~~~

Incorrect
^^^^^^^^^

This example uses the built-in parameter substitution mechanism '%' to
insert a value into the query string, this will perform an unsafe
literal insertion and not provide any escaping.

.. code:: python

    import sqlalchemy

    connection = engine.connect()
    myvar = 'jsmith' # our intended usage
    myvar = 'jsmith or 1=1' # this will return all users
    myvar = 'jsmith; DROP TABLE users' # this drops (removes) the users table
    query = "select username from users where username = %s" % myvar
    result = connection.execute(query)
    for row in result:
        print "username:", row['username']
    connection.close()

Correct
^^^^^^^

This example uses SQLAlchemy's built in parameter substitution
mechanism to safely replace the ':name' variable with a provided value.

.. code:: python

    import sqlalchemy

    connection = engine.connect()
    myvar = 'jsmith' # our intended usage
    myvar = 'jsmith or 1=1' # only matches this odd username
    query = "select username from users where username = :name"
    result = connection.execute(query, name = myvar)
    for row in result:
        print "username:", row['username']
    connection.close()

MySQL
~~~~~

Incorrect
^^^^^^^^^

Without using any escaping mechanism, potentially unsafe queries can
be created.

.. code:: python

    import MySQLdb

    query = "select username from users where username = '%s'" % name
    con = MySQLdb.connect('localhost', 'testuser', 'test623', 'testdb');

    with con:
        cur = con.cursor()
        cur.execute(query)

Better
^^^^^^

In this example the query is created using pythons standard, unsafe
'%' operator. MySQL's 'escape\_string' method is used to perform escaping
on the user input string prior to inclusion in the string.

.. code:: python

    import MySQLdb

    query = "select username from users where username = '%s'" % MySQLdb.escape_string(name)
    con = MySQLdb.connect('localhost', 'testuser', 'test623', 'testdb');

    with con:
        cur = con.cursor()
        cur.execute(query)

Correct
^^^^^^^

The correct way to do this using a parameterized
query might look like the following:

.. code:: python

    import MySQLdb

    query = "select username from users where username = '%s'"
    con = MySQLdb.connect('localhost', 'testuser', 'test623', 'testdb');

    with con:
        cur = con.cursor()
        cur.execute(query, (username_value,))

This works because the logic of the query is compiled before the user
input is considered.

PostgreSQL (Psycop2)
~~~~~~~~~~~~~~~~~~~~

Incorrect
^^^^^^^^^

This example uses python's unsafe default parameter substitution
mechanism to build a query string. This will not perform any escaping,
unlike the correct example below the string is processed and passed as
a single parameter to 'execute'.

.. code:: python

    import psycopg2

    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()
    cur.execute("select username from users where username = '%s'" % name)

Correct
^^^^^^^

This example uses Psycop2's parameter substitution mechanism to build
a query string. Despite the use '%' to indicate the substitution token,
it is not the same as Python's built in string operator %. Note the
value(s) are passed as parameters to 'execute' separately.

.. code:: python

    import psycopg2

    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()
    cur.execute("select username from users where username = '%s'", (name,))

Consequences
~~~~~~~~~~~~

-  Potential for full disclosure of data
-  Potential for remote code execution

References
~~~~~~~~~~

-  `More information about SQL
   Injection <https://www.owasp.org/index.php/SQL_Injection>`__
-  `SQL Injection
   Prevention <https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet>`__
