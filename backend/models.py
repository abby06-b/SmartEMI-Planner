from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

# -------------------- USER MODEL ------------------------
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)

    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")

    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# -------------------- LOAN MODEL ------------------------
class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    loan_type = Column(String)
    principal = Column(Float)
    interest_rate = Column(Float)
    tenure_months = Column(Integer)
    emi = Column(Float)

    user = relationship("User", back_populates="loans")


# -------------------- EXPENSE MODEL ------------------------
class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String)
    amount = Column(Float)

    user = relationship("User", back_populates="expenses")


# -------------------- GOAL MODEL ------------------------
class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    goal_name = Column(String)
    target_amount = Column(Float)
    target_month = Column(String)  # e.g. "2026-05"

    user = relationship("User", back_populates="goals")


# -------------------- DB HELPERS ------------------------

def get_engine(db_path='sqlite:///finance.db'):
    return create_engine(db_path, connect_args={"check_same_thread": False})

# keep this for app.py and db_init.py
def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# optional: scoped session if later needed
def get_scoped_session(engine):
    return scoped_session(sessionmaker(bind=engine))
