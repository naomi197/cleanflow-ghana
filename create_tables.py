from app.db.session import Base, engine
from app.models.pollution_report import PollutionReport

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
