from sqlalchemy import Column, Integer, String, MetaData, Table

metadata = MetaData()

meetings = Table(
    "meetings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
)
