# video-ipub-lambda

Lambda function to drive the Interactive Publisher database.
This replaces the older interactivepublisher.pl script running on Workflowmaster.

This repository contains a lambda function that is designed to respond to
SNS messages.

Its function is to parse the XML payload of the message, extract out relevant
metadata fields and then insert them into the interactive publisher database.

The schema of this database is contained at tests/testdata/dbschema.sql.

## Deployment

This is an AWS lambda function and as such requires no server build.
However, deployment still functions in the normal way - there is a Cloudformation
template in the multimedia-infra repository which will set up the necessary permissions,
Lambda function itself and optionally the database.

The code is built by CircleCI and is deployable using RiffRaff, provided
that a cloudformation stack is present for the relevant stage.

If you want to build the artifact locally, then you will need to install NodeJS 6.x
and run npm install before running ./builddeployable.sh

## Running Locally
### Requirements:

 - Python 2.7
 - MySQL 5.6
 - Node.js (for build deployment only, not for development)
 
### Setup:

#### Database
Firstly, you need to install mysql. If you're on linux this should be as simple
as

        # yum install mysql-server
or

        # apt-get install mysql-server
    
If you're on a Mac, the easiest way is probably by using MacPorts - https://www.macports.org/
Once you've installed the dmg, you should simply be able to run:

        # port install mysql56-server
    
Once mysql is installed, you need to create a database to use and a user for the program:
 
        # mysql -u root [ -S /path/to/socket]
        mysql> create database interactivepublisher;
        mysql> grant all on interactivepublisher to ipubuser identified by 'password';
        mysql> ^D
        #

Then, you need to install the schema:

        # cd /path/to/your/checkout
        # mysql -u root interactivepublisher < tests/testdata/dbschema.sql
        
Lastly for the database, you need to set up the connection parameters.  In the Lambda environment,
this is done using the environment variables DB_USER, DB_PASSWD, DB_HOST and DB_NAME.
For convenience though you can specify the values in src/config.py.
In the example above, the username is ipubuser, the password is 'password' (without the quotes),
and the database is called interactivepublisher

**Note** that most default installations of mysql do not allow network connection by default.
The easiest way around this is to set unix_socket: in config.py and remove the hostname.
This will make mysql-connector talk to the unix socket and not attempt a network connection.
Your other option is to allow network connection from localhost by modifiying your
mysql server configuration.  There are plenty of guides online about how to do this.

#### Python
I would highly recommend that you set up a virtual environment (virtualenv) to run this.
This is a Python feature that allows you to keep libraries and versions seperate between projects.

**Note** - you can also set up virtualenvs with PyCharm or Intellij, if you have their Python plugin installed.
If you want to do it that way, disregard the instructions below and consult the Intellij
documentation.

If you have not set one up before, then you first need to ensure that you have Python and pip (Python's
package management tool) installed.  Pretty much all Linux and Macs do.

        $ python --version
        Python 2.7.12
        
There is a good guide about how to set up virtualenvs here: http://docs.python-guide.org/en/latest/dev/virtualenvs/
In brief, though:

        $ sudo pip install virtualenv
        $ cd /path/to/checkout
        $ virtualenv venv
        $ source ./venv/bin/activate
        
Once you're in the virtualenv, your prompt is changed to show you're in it:
        (venv) $ pip install -r requirements.txt
        
Unfortunately, mysql-connector/Python is not available through pip.
So, you need to install it seperately:

        (venv) $ curl http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.4.tar.gz > /tmp/mysql-connector-python-2.1.4.tar.gz
        (venv) $ cd /tmp; tar xvzf mysql-connector-python-2.1.4.tar.gz
        (venv) $ cd /tmp/mysql-connector-python-2.1.4; python ./setup.py install
        
Once this is done, you should be able to run the **tests**.
 
## Tests
### Automated
        (venv) $ cd /path/to/checkout
        (venv) $ python -m unittest discover -s tests

Running the tests requires that all of the Python requirements are installed, that there is a Mysql
installation working with the schema installed and that config.py or the environment variables are
set up for the program to access them (see **Requirements**)
These tests are run automatically on commit by CircleCI.

### Manual - in Code environment
Once deployed into the CODE environment, find the SNS topic associated with the stack in the AWS Console.
Then, click 'Publish to Topic' and paste a sample XML (see "XML Format", below) into the box.
Go back to the Lambda control panel and view the logs of the function. Before
long you should see it pop up with the result.

### Detailed - locally
At the moment, you can't. It just does the automated tests.

## XML Format
The supported XML format looks something like this.  It is composed of three
separate sections:

- meta-source (abbreviated to meta) - general key/value pairs. Pluto provided metadata
- movie - specific information about the media container format
- track - specific information about each track. Each track has its own copy of this section

Within these sections, each key/value pair is described by the following line:

    <meta name="key" value="value"/>

Putting it all together looks like this:

        <?xml version="1.0"?>
        <!DOCTYPE meta-data SYSTEM "meta.dtd">
        <meta-data version="1.0">
          <meta name="meta-source" value="inmeta">
              <meta name="key" value="value"/>
          </meta>
          <meta name="movie" value="">
              <meta name="key" value="value"/>
          </meta>
          <meta name="track" value="1">
            <meta name="type" value="vide"/>
            <meta name="index" value="1"/>
          </meta>
        
          <meta name="track" value="2">
            <meta name="type" value="audi"/>
            <meta name="index" value="2"/>
          </meta>
        </meta-data>

Example fully-formed XMLs are in tests/testdata.

## Mapping
Mappings are defined in the Mapper.py module.  They tell the software how to map from the
key-value pairs as provided in the XML to the database fieldnames.

The XML mappings are specified as a sequence of elements delimited by a colon.

- The first item in the sequence is the section - either meta, movie or track.
- If the section is "track", then the second item in the sequence should specify
either the type of the track ("type" key, above; usually vide or audi) or its
index ("value" attribute above)
- The last item in the sequence is the actual key.

So, for the above example XML *meta:key* will map to the string "*value*", or
*track:audi:index* will map to the string "*2*".  Consult the example metadata and the "graveyards"
in the live system for details of the kind of metadata available.

Mapper.py defines a number of complete mappings in a list.  The first set to completely
match the incoming data is used.  In order to be valid, **every** mapping must find a
value; an exception is raised if not.

You can test your mappings by running Mapper.py directly from the Terminal:

    (venv) $ python src/Mapper.py {/path/to/test/file.meta.xml}
    
This will either output a dictionary of mapped metadata or an exception if none of the mappings worked:

    Traceback (most recent call last):
      File "src/Mapper.py", line 78, in <module>
        pprint(m.map_metadata(p))
      File "src/Mapper.py", line 66, in map_metadata
        raise NoMappingFound("No mapping matched the provided metadata.  Failed mappings were: {0}".format(failed_mappings))
    __main__.NoMappingFound: No mapping matched the provided metadata.  Failed mappings were: ["u'movie:format'", "u'meta:is_multirate'"]
