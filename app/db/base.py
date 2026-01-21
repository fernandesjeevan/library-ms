from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
















# import psycopg2
# from psycopg2.extras import RealDictCursor
# import os
# from dotenv import load_dotenv


# # this is to load variables from dotenv
# # load_dotenv()

# # conn = psycopg2.connect(
# #      database=os.getenv("PG_DATABASE"),
# #      user=os.getenv("PG_USER"),
# #      password=os.getenv("PG_PASSWORD"),
# #      host="localhost",
# #      port="5432",
# #      cursor_factory=RealDictCursor)

