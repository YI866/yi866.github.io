import sqlalchemy as db

url = "mysql+pymysql://root:ikas@localhost:3306/eap?charset=utf8"
print(url)
engine = db.create_engine(url)
meta = db.MetaData()
meta.reflect(bind=engine)
# print(meta.tables['equipment'].primary_key.columns)
with engine.begin() as conn:
    res = conn.scalar((db.select(db.func.count(1)).select_from((meta.tables["equipment"]))))
    # res = conn.scalar(db.text("SELECT count(1) FROM equipment"))
    print(res)