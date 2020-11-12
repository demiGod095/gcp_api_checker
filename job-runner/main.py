import os
import time
import base64

import requests
from requests.exceptions import RequestException
from sqlalchemy import engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from sqlalchemy_declarative import Job, Base


def db_connect_session():
    # get the db conf from env

    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST", "localhost:3306")

    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_hostname,
            port=db_port,
            database=db_name,
        ),
        # option to enable concurrent updates and reads only committed
        isolation_level="READ COMMITTED"
    )

    Base.metadata.bind = pool

    DBSession = sessionmaker(bind=pool)
    return DBSession()


# function to connect to try the provided url
def try_url(url):
    # keep track of number of tries
    tries = 0

    while True:
        # increment tries
        tries += 1
        try:
            # request url and raise if status codes are errors 4xx or 5xx
            response = requests.request("GET", url)
            response.raise_for_status()

            # response has non-exception based code.. return it
            return tries, response.status_code

        except RequestException as e:
            # inspect error for code
            if e.response is not None:
                response_code = e.response.status_code
            else:
                # no response object, so no code
                # reasons are too many redirects, timeouts, or other connection errors
                # set code as 404 .. representing url not found
                response_code = 404

        # need to check 3 times, break when limit reached
        if tries == 3:
            break

        # sleep for a while before next try
        time.sleep(2)

    #  return the errored response code
    return tries, response_code


# inject function
def job_runner():
    # connect to db session
    session = db_connect_session()

    # everything in try block for sql Exception
    try:
        # keep checking for new jobs once executed
        while True:

            # start transaction for concurrency
            session.execute("START TRANSACTION")

            # locks the row returned
            job = session.query(Job).filter(Job.tries == 0).order_by(Job.created_at.asc()).with_for_update().first()

            # no job found, can stop execution
            if not job:
                print(f'No more jobs')
                return

            # job found, process the url
            tries, code = try_url(job.url)

            print(f'{job.url=} (RESULT: {tries=}, {code=})')

            # update the job
            job.tries = tries
            job.code = code
            job.response = my_inverted_codes.get(code, 'unknown')

            # commit the update and unlock the job
            session.commit()

    except SQLAlchemyError as e:
        print(f'Error {e=}')
        session.rollback()
    finally:
        session.close()


def job_runner_sub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    timeout = base64.b64decode(event['data']).decode('utf-8')

    if timeout is not None:
        try:
            sec = int(timeout)
            time.sleep(sec)
        except ValueError:
            pass

    job_runner()


if __name__ == 'main':
    # calc invert of dictionary on boot
    my_inverted_codes = {requests.codes.get(key): key for key in dir(requests.codes)}

    # run job
    job_runner()
