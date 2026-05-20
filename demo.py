"""
Library Management System - Interactive CLI
This script provides an interactive CLI where user enters data from keyboard.
"""

import sys
from app.db.session import db_session
from app.services import (
    UserService,
    BookService,
    LoanService,
    FineService,
)
from app.services.loan_service import (
    UserNotFoundError,
    BookNotFoundError,
    NoCopiesAvailableError,
    MaxLoansExceededError,
    BookAlreadyReturnedError,
    LoanNotFoundError,
    LoanServiceError,
)
from app.services.user_service import UserAlreadyExistsError


def print_header(title):
    print("\n" + "=" * 50)
    print("  " + title)
    print("=" * 50)


def print_menu():
    print_header("LIBRARY MANAGEMENT SYSTEM - MAIN MENU")
    print("  1. Create New User")
    print("  2. Create New Book")
    print("  3. Add Book Copies")
    print("  4. Borrow Book")
    print("  5. Return Book")
    print("  6. View My Loans")
    print("  7. Calculate Fine")
    print("  8. View Available Books")
    print("  9. Pay Fine")
    print(" 10. List All Users")
    print(" 11. List All Books")
    print("  0. Exit")
    print("-" * 50)


def get_input(prompt):
    return input("  " + prompt + ": ").strip()


def handle_create_user(session, user_service):
    print_header("Create New User")
    email = get_input("Enter email")
    name = get_input("Enter name")
    role = get_input("Enter role (member/admin)")
    if not role:
        role = "member"
    
    try:
        user = user_service.create_user(email, name, role)
        session.commit()
        print("  [OK] User created: " + user.name + " (" + user.email + ") - " + user.role)
    except UserAlreadyExistsError:
        print("  [ERROR] User with this email already exists!")
    except Exception as e:
        print("  [ERROR] " + str(e))


def handle_create_book(session, book_service):
    print_header("Create New Book")
    title = get_input("Enter book title")
    author = get_input("Enter author name")
    category = get_input("Enter category (optional)")
    
    try:
        if category:
            book = book_service.create_book(title, author, category)
        else:
            book = book_service.create_book(title, author)
        session.commit()
        print("  [OK] Book created: " + book.title)
        print("  [OK] Author: " + book.author.name)
        print("  [OK] Category: " + (book.category.name if book.category else "None"))
    except Exception as e:
        print("  [ERROR] " + str(e))


def handle_add_copies(session, book_service):
    print_header("Add Book Copies")
    title = get_input("Enter book title")
    
    books = book_service.get_all_books()
    book = None
    for b in books:
        if b.title.lower() == title.lower():
            book = b
            break
    
    if not book:
        print("  [ERROR] Book not found!")
        return
    
    num = get_input("How many copies to add")
    try:
        num = int(num) if num else 1
        for i in range(num):
            book_service.add_book_copy(book.id, "COPY-" + str(i+1))
        session.commit()
        print("  [OK] Added " + str(num) + " copies to '" + book.title + "'")
    except Exception as e:
        print("  [ERROR] " + str(e))


def handle_borrow_book(session, user_service, book_service, loan_service):
    print_header("Borrow Book")
    email = get_input("Enter your email")
    
    try:
        user = user_service.get_user_by_email(email)
        if not user:
            print("  [ERROR] User not found!")
            return
        
        title = get_input("Enter book title to borrow")
        books = book_service.get_all_books()
        book = None
        for b in books:
            if b.title.lower() == title.lower():
                book = b
                break
        
        if not book:
            print("  [ERROR] Book not found!")
            return
        
        loan = loan_service.issue_book(user.id, book.id)
        session.commit()
        print("  [OK] Book borrowed successfully!")
        print("  [OK] Due date: " + loan.due_date.strftime('%Y-%m-%d'))
    except UserNotFoundError:
        print("  [ERROR] User not found!")
    except BookNotFoundError:
        print("  [ERROR] Book not found!")
    except NoCopiesAvailableError:
        print("  [ERROR] No copies available!")
    except MaxLoansExceededError:
        print("  [ERROR] You have reached maximum limit of 3 books!")
    except LoanServiceError as e:
        print("  [ERROR] " + str(e))
    except Exception as e:
        print("  [ERROR] " + str(e))


def handle_return_book(session, user_service, loan_service):
    print_header("Return Book")
    email = get_input("Enter your email")
    
    try:
        user = user_service.get_user_by_email(email)
        if not user:
            print("  [ERROR] User not found!")
            return
        
        loans = loan_service.get_user_borrowed_books(user.id)
        if not loans:
            print("  [INFO] You have no books to return!")
            return
        
        print("  Your borrowed books:")
        for l in loans:
            print("    Loan ID: " + str(l.id) + ", Copy ID: " + str(l.book_copy_id))
        
        loan_id = get_input("Enter Loan ID to return")
        loan_id = int(loan_id)
        
        returned = loan_service.return_book(loan_id)
        session.commit()
        print("  [OK] Book returned successfully!")
        print("  [OK] Return date: " + returned.return_date.strftime('%Y-%m-%d'))
    except LoanNotFoundError:
        print("  [ERROR] Loan not found!")
    except BookAlreadyReturnedError:
        print("  [ERROR] Book already returned!")
    except Exception as e:
        print("  [ERROR] " + str(e))


def handle_view_loans(user_service, loan_service):
    print_header("View My Loans")
    email = get_input("Enter your email")
    
    try:
        user = user_service.get_user_by_email(email)
        if not user:
            print("  [ERROR] User not found!")
            return
        
        loans = loan_service.get_user_loans(user.id)
        if not loans:
            print("  [INFO] No loan history!")
            return
        
        print("  Total loans: " + str(len(loans)))
        for l in loans:
            print("    Loan #" + str(l.id) + " - Status: " + l.status.value)
    except Exception as e:
        print("  [ERROR] " + str(e))


def handle_calculate_fine(fine_service):
    print_header("Calculate Fine")
    loan_id = get_input("Enter Loan ID")
    
    try:
        loan_id = int(loan_id)
        fine = fine_service.create_fine(loan_id)
        
        if fine:
            print("  [OK] Fine calculated: $" + str(fine.amount))
            print("  [OK] Days late: " + str(fine.days_late))
        else:
            print("  [OK] No fine - returned on time!")
    except LoanNotFoundError:
        print("  [ERROR] Loan not found!")
    except Exception as e:
        print("  [ERROR] " + str(e))


def handle_view_available(book_service):
    print_header("Available Books")
    
    books = book_service.get_available_books()
    if not books:
        print("  [INFO] No books available!")
        return
    
    print("  Available books: " + str(len(books)))
    for book in books:
        copies = book_service.count_available_copies(book.id)
        print("    - " + book.title + " (" + str(copies) + " copies)")


def handle_pay_fine(fine_service, session):
    print_header("Pay Fine")
    fine_id = get_input("Enter Fine ID")
    
    try:
        fine_id = int(fine_id)
        paid = fine_service.pay_fine(fine_id)
        session.commit()
        print("  [OK] Fine paid successfully!")
    except Exception as e:
        print("  [ERROR] " + str(e))


def handle_list_users(user_service):
    print_header("All Users")
    
    users = user_service.get_all_users()
    if not users:
        print("  [INFO] No users!")
        return
    
    print("  Total users: " + str(len(users)))
    for u in users:
        print("    - " + u.name + " (" + u.email + ") - " + u.role)


def handle_list_books(book_service):
    print_header("All Books")
    
    books = book_service.get_all_books()
    if not books:
        print("  [INFO] No books!")
        return
    
    print("  Total books: " + str(len(books)))
    for b in books:
        copies = book_service.count_available_copies(b.id)
        print("    - " + b.title + " by " + b.author.name + " (" + str(copies) + " available)")


def main():
    print_header("LIBRARY MANAGEMENT SYSTEM")
    print("Initializing database...")
    
    # Initialize database and services
    db_session.create_tables()
    session = db_session.get_session_context()
    user_service = UserService(session)
    book_service = BookService(session)
    loan_service = LoanService(session)
    fine_service = FineService(session)
    
    print("Database ready!")
    print("Enter 0 to exit")
    
    # Main menu loop
    while True:
        print_menu()
        choice = get_input("Choose option")
        
        # Switch statement using if/elif
        if choice == "0":
            print("\nThank you for using the Library Management System!")
            break
        elif choice == "1":
            handle_create_user(session, user_service)
        elif choice == "2":
            handle_create_book(session, book_service)
        elif choice == "3":
            handle_add_copies(session, book_service)
        elif choice == "4":
            handle_borrow_book(session, user_service, book_service, loan_service)
        elif choice == "5":
            handle_return_book(session, user_service, loan_service)
        elif choice == "6":
            handle_view_loans(user_service, loan_service)
        elif choice == "7":
            handle_calculate_fine(fine_service)
        elif choice == "8":
            handle_view_available(book_service)
        elif choice == "9":
            handle_pay_fine(fine_service, session)
        elif choice == "10":
            handle_list_users(user_service)
        elif choice == "11":
            handle_list_books(book_service)
        else:
            print("  [ERROR] Invalid option! Please try again.")
    
    session.close()


if __name__ == "__main__":
    main()