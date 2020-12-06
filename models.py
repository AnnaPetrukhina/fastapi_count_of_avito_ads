import os
from databases import Database
from dotenv import load_dotenv
import sqlalchemy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

engine = sqlalchemy.create_engine(os.environ["DATABASE_URL"])
db = Database(os.environ["DATABASE_URL"])

metadata = sqlalchemy.MetaData()


search_params = sqlalchemy.Table(
    "Params",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("region", sqlalchemy.String),
    sqlalchemy.Column("query", sqlalchemy.String),
)


counter = sqlalchemy.Table(
    "Counter",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("id_search", sqlalchemy.Integer, sqlalchemy.ForeignKey("Params.id")),
    sqlalchemy.Column("timestamp", sqlalchemy.String),
    sqlalchemy.Column("count", sqlalchemy.Integer),
)
