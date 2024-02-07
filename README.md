**#WEB APPLICATION REQUIREMENTS:**

**Getting Started**
--------------------------------------------------------------------------------------------------------------------------------------------------------

**INSTALL PYTHON VERSION 3 and PIP**

Refer to the documents: 
  - https://www.python.org/downloads/
  - https://pip.pypa.io/en/stable/installation/

Install the required libraries by running command:
  - pip install -r requirements.txt
    
Create a postgres database by following below instructions:
  - install postgresql v.16 : https://www.postgresql.org/download/
  - start and enable postgresql service
  - create database 'user_ip_mapping' on your postgresql
  - Look for 'pg_hba_conf' file, usually stored in "/var/lib/pgsql/data/" and change the authentication method from 'ident' to trust for each line.

Now once you have completed all the steps:
 - Run the application by using 'Python3 Application.py' command
 - Test all the scenarios.



