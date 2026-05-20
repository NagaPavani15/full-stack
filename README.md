# Library Management System - Beginner Guide

This guide explains everything in simple terms for someone who is new to programming.

---

## PART 1: HOW TO RUN THIS PROJECT

### Step 1: Install Python
If you don't have Python, download from: https://python.org

### Step 2: Install Requirements
Open your terminal/command prompt and run:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Program
```bash
python demo.py
```

You will see a menu. Enter a number (0-11) to do different things:
- 1 = Create a new user
- 2 = Create a new book
- 3 = Add copies of a book
- 4 = Borrow a book
- 5 = Return a book
- 8 = See available books
- 10 = See all users
- 11 = See all books
- 0 = Exit

### Step 4: Run Tests
```bash
python -m pytest -v
```

This runs automatic tests to make sure everything works correctly.

---

## PART 2: WHAT DOES THIS SYSTEM DO?

This is a **Library Management System** - like a computer program that helps manage a real library.

### Main Features:

1. **User Management**
   - Create library members (people who can borrow books)
   - Each user has: name, email, role (member or admin)
   - Email must be unique (no two users can have same email)

2. **Book Management**
   - Create books with title, author, and category
   - Each book can have multiple COPIES (like having 3 physical books of the same title)
   - Track how many copies are available

3. **Loan System (Borrowing)**
   - User can borrow a book copy
   - Due date is set to 14 days from borrowing
   - Maximum 3 books per user at a time
   - Cannot borrow if no copies available

4. **Return System**
   - User returns the book
   - Copy becomes available again
   - Cannot return same book twice

5. **Fine System**
   - If returned late, calculate fine: $1 per day
   - Track fines and allow payment

### Business Rules:
- Max 3 books per user
- Cannot borrow if no copies available
- Cannot return same book twice
- Fine = $1 × number of days late

---

## PART 3: WHAT IS SQLALCHEMY?

### What is a Database?
A database is like a digital filing cabinet that stores information. Common databases:
- **SQLite** - Simple, used in this project (stored in a file)
- **MySQL** - Used for large websites
- **PostgreSQL** - Advanced database

### What is SQL?
**SQL** (Structured Query Language) is a language to talk to databases. Example:
```sql
SELECT * FROM users WHERE email = 'john@example.com'
```
This means: "Find the user with email john@example.com"

### What is SQLAlchemy?
**SQLAlchemy** is a Python library that makes it easy to work with databases. Instead of writing SQL, you write Python code.

#### Without SQLAlchemy (complex):
```python
# Raw SQL - hard to read and maintain
cursor.execute("INSERT INTO users (name, email) VALUES ('John', 'john@example.com')")
```

#### With SQLAlchemy (simple):
```python
# Python code - easy to understand
user = User(name="John", email="john@example.com")
session.add(user)
```

### Key Differences:

| Feature | Raw SQL | SQLAlchemy |
|--------|--------|------------|
| Learning curve | Hard | Easier |
| Code readability | Complex | Simple |
| Database support | One | Multiple |
| Security | Manual | Automatic |
| Maintenance | Difficult | Easier |

### How SQLAlchemy Works in This Project:

1. **Models** (app/models/) = Define what a "table" looks like
   ```python
   class User(Base):
       id = Column(Integer, primary_key=True)
       name = Column(String(255))
       email = Column(String(255), unique=True)
   ```

2. **Session** (app/db/session.py) = Connection to database

3. **CRUD Operations** = Create, Read, Update, Delete
   ```python
   # Create
   user = User(name="John", email="john@example.com")
   session.add(user)
   
   # Read
   user = session.get(User, 1)  # Get user with id=1
   
   # Update
   user.name = "Jane"
   session.add(user)
   
   # Delete
   session.delete(user)
   ```

---

## PART 4: WHAT IS TESTING?

### What is Testing?
Testing is like having a **exam** for your program. You create questions (tests) and the program answers them.

### Why Testing is Important:
1. **Catches bugs** before users see them
2. **Ensures features work** correctly
3. **Prevents breaking** changes when updating code
4. **Documents** how the code should work

### How Testing Works in This Project:

#### Test File Location: tests/
- `test_models.py` - Test database models
- `test_services.py` - Test business logic
- `test_loans.py` - Test borrowing/returning
- `test_fines.py` - Test fine calculation


#### Example Test:
```python
def test_create_user_success():
    # Test: Can we create a user?
    
    # Step 1: Create user
    user = user_service.create_user("john@example.com", "John Doe")
    
    # Step 2: Check if it worked
    assert user.name == "John Doe"           # This should be TRUE
    assert user.email == "john@example.com"  # This should be TRUE
    
    # If both true, test PASSES
    # If any false, test FAILS
```

#### Types of Tests in This Project:

1. **Model Tests** - Test database structures
   ```python
   def test_user_creation():
       user = User(email="test@test.com", name="Test")
       assert user.email == "test@test.com"
   ```

2. **Service Tests** - Test business logic
   ```python
   def test_create_duplicate_user_fails():
       user_service.create_user("test@test.com", "Test")
       # Try creating same user again
       with pytest.raises(UserAlreadyExistsError):
           user_service.create_user("test@test.com", "Test")
   ```

3. **Integration Tests** - Test complete features
   ```python
   def test_borrow_and_return_book():
       loan = loan_service.issue_book(user_id, book_id)
       returned = loan_service.return_book(loan.id)
       assert returned.status == "returned"
   ```

#### Test Results:
```
37 passed = All tests passed!
0 failed = No errors found!
```

---

## QUICK START SUMMARY

1. **Install**: `pip install -r requirements.txt`
2. **Run program**: `python demo.py`
3. **Run tests**: `python -m pytest -v`
4. **Enjoy!**

---

## PROJECT STRUCTURE EXPLAINED

```
library-management-system/
├── app/                    # Main application code
│   ├── db/                 # Database setup
│   │   ├── base.py        # Defines database structure
│   │   └── session.py    # Connection to database
│   ├── models/            # Data models (User, Book, Loan, etc.)
│   ├── repositories/     # Data access layer
│   └── services/        # Business logic
├── tests/                 # Test files
│   ├── conftest.py       # Test setup
│   ├── test_models.py   # Model tests
│   ├── test_services.py # Service tests
│   ├── test_loans.py   # Loan tests
│   └── test_fines.py   # Fine tests
├── requirements.txt      # Python packages needed
└── README.md           # This file
```

---

## GLOSSARY (Simple Definitions)

| Term | Definition |
|------|------------|
| **ORM** | Object-Relational Mapping - converts between Python and Database |
| **Model** | A Python class that represents a database table |
| **Session** | A connection to the database |
| **Service** | Code that handles business logic |
| **Repository** | Code that handles database operations |
| **Fixture** | A test setup - creates test data |
| **Assert** | Check if something is true |
| **pytest** | A tool that runs tests |
| **SQLite** | A simple file-based database |
| **Primary Key** | Unique ID for each record |
| **Foreign Key** | Link to another table |

---

## NEED HELP?

If something doesn't work:
1. Check Python is installed: `python --version`
2. Check requirements installed: `pip list`
3. Run tests: `pytest` (should show 37 passed)
4. Try running demo: `python demo.py`

---

**Happy Learning!**