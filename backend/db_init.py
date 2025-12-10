from models import Base, User, get_engine, get_session

engine = get_engine('sqlite:///finance.db')

# Reset tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = get_session(engine)

# Create demo user
demo = User(name="Demo User", email="demo@example.com")
demo.set_password("demo123")
session.add(demo)
session.commit()
session.close()

print("Database initialized. Demo user: demo@example.com / demo123")
