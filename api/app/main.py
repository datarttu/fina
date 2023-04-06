import os
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, Response, status

app = FastAPI(title='REST API for personal finance planning')


@app.get('/')
def hello_world():
    '''
    The root route which returns a JSON response.
    The JSON response is delivered as:
    {
      'message': 'Hello, World!'
    }
    '''
    return {'message': 'Hello, World!'}

@app.get('/health')
def healthcheck(response: Response):
    '''
    Checks and returns the status of the database connection (API dependency).
    '''
    try:
        with psycopg.connect(os.environ['POSTGRES_URL']) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT 1")
                return {'message': 'Database up and running.'}
    except psycopg.OperationalError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {'message': 'Database connection failed.'}