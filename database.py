import psycopg2

#def get_connection():
   # return psycopg2.connect(
       # host="localhost",
       # database="user_db",
       # user="postgres",
       # password="0000"
  #  )
def get_connection():
    return psycopg2.connect(
        host="host.docker.internal",
        database="user_db",
        user="postgres",
        password="0000"
    )