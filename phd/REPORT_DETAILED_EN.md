# Project Report

## 1. Project Title

LedgerLite: A Simple Accounting Transaction Management System

## 2. Introduction

This project is a small web-based application developed in the accounting field with the aim of digitizing the daily recording of income and expenses in a simple yet professional way. The main idea is to move from manual record-keeping to a digital system that allows users to enter data, store it, edit it, delete it, and export it into reusable files.

The project achieves the concept of a **Vertical Slice**, because it follows a complete path starting from the user interface, then the processing logic in Python, then data storage in the database, and finally the display of results again in the application.

## 3. Project Objective

The objective of this project is to solve a common problem in daily accounting work, namely the difficulty of tracking financial transactions when they are recorded manually or in an unstructured way. Therefore, the application provides an organized solution for:

- recording income and expenses
- calculating the net balance
- searching and filtering transactions
- storing data in a database
- generating backup files in multiple formats

## 4. Tools and Technologies Used

- Programming language: Python
- Framework: Flask
- Database: SQLite
- File formats: CSV, JSON, and TXT
- Frontend design: HTML and CSS
- Programming approach: Object-Oriented Programming (OOP)

SQLite was selected because it is a lightweight database that is easy to integrate into a small academic project, and it is highly suitable for building a simple yet well-structured professional application.

## 5. Accounting Idea of the Project

The application is designed to manage daily accounting transactions for a small office or a simple business activity. Each transaction contains:

- transaction date
- transaction type: income or expense
- category
- description
- amount
- payment method
- transaction reference
- additional notes

After storing these data, the user can monitor the overall financial situation through a dashboard that displays total income, total expenses, the number of transactions, and the final balance.

## 6. Project Development Steps

### Step 1: Requirement Analysis

At the beginning, the project description file was analyzed and the main requirements were extracted:

- use Python
- provide file handling features
- use a database
- create a Flask web interface
- apply OOP principles

After that, the **accounting** domain was selected because it matches the specialization and provides a clear and realistic idea that can be implemented easily.

### Step 2: Choosing a Simple and Professional Topic

The topic of **accounting transaction management** was chosen because it is:

- simple in concept
- clear in terms of inputs and outputs
- very suitable for academic presentation
- convenient for implementing CRUD operations, a database, and reporting features

### Step 3: Building the General Project Structure

The project was divided into organized files so that it would be clear and easy to understand:

- `app.py` to run the application
- `routes.py` to manage pages and navigation
- `services.py` to apply business logic
- `repositories.py` to interact with the database
- `models.py` to define the core entity, which is the transaction
- `templates` folder for the web pages
- `static` folder for styling

This structure gives the project a professional shape instead of putting everything in one file.

### Step 4: Creating the Transaction Object Model

A class named `Transaction` was created to represent the accounting transaction. This class contains the transaction attributes and the methods used to validate the data and convert it into a record that can be stored or displayed.

In this way, each transaction has a structured representation inside the project instead of handling data in a random or unorganized way.

### Step 5: Creating the Database Layer

A class named `TransactionRepository` was created, and it is responsible for all operations related to the database, such as:

- creating the table
- listing transactions
- retrieving a specific transaction
- adding a transaction
- updating a transaction
- deleting a transaction
- calculating the financial summary

This layer separates the database from the rest of the project, which is an important engineering practice.

### Step 6: Creating the Service Layer

A class named `AccountingService` was created to handle the actual business logic of the project. In this layer, the application:

- builds the transaction from form data
- validates the transaction
- sends it to the repository
- exports the data into files
- imports backup files

This means that the service layer acts as the bridge between the user interface and the database.

### Step 7: Building the Flask Interface

A web interface was developed using Flask, and it contains:

- a main dashboard showing the financial summary and transaction list
- a page for adding a new transaction
- a page for editing a transaction
- a page for managing backups

The interface was designed in a simple but organized way so that the project appears professional without unnecessary complexity.

### Step 8: Adding File Management

To satisfy the file handling requirement, the following features were added:

- exporting data to CSV
- exporting data to JSON
- generating a TXT report
- importing a backup from CSV or JSON

These features are useful in accounting because they allow data storage, restoration, and simple reporting.

### Step 9: Preparing the Documentation

Documentation files were prepared to explain the project, including:

- a technical report in English
- an Arabic report
- a README file explaining how to run the project

A UML diagram was also included to illustrate the relationship between the main classes.

## 7. How the Project Works Step by Step

When the application is used, the following sequence takes place:

1. The user enters transaction data through the web interface.
2. The data are sent to `routes.py`.
3. `AccountingService` builds a `Transaction` object.
4. The data are validated.
5. If the data are valid, `AccountingService` sends them to `TransactionRepository`.
6. `TransactionRepository` stores them in SQLite.
7. When the user returns to the main page, all transactions are retrieved and the financial summary is calculated.
8. The results are displayed on the dashboard.

When exporting or importing data, the project follows the same logic with additional file processing depending on the selected format.

## 8. Explanation of the Diagram

The diagram is very good in terms of structure and organization because it clearly shows the three main layers:

- `AccountingService`
- `TransactionRepository`
- `Transaction`

This division is logical and correct because:

- `Transaction` represents the data
- `TransactionRepository` handles the database
- `AccountingService` contains the processing logic

### My Opinion About the Diagram

The diagram is well organized and gives a professional impression, especially because it shows the direction of dependency from the upper layer to the lower layer:

- the service depends on the repository
- the repository depends on the transaction

### Small Suggestions for Improvement

- It would be better to mention that this is a **backend class diagram only**, because it does not show the Flask pages or the interface layer.
- If needed, a second diagram could be added later to represent the `Routes / Flask Layer`.
- It is also possible to include return types for some methods, but this remains optional.

Overall, the diagram is successful and very suitable for inclusion in the report.

## 9. Compliance with the Assignment Requirements

The project satisfies the main assignment requirements as follows:

- Python Basics: achieved
- Files and Data Handling: achieved
- Database Management: achieved
- Flask Web Interface: achieved
- OOP and Classes: achieved
- Good engineering organization: achieved

## 10. Conclusion

This project provides a simple and practical solution for monitoring daily accounting transactions while respecting the academic requirements of the assignment. It also demonstrates the ability to combine Python, Flask, database management, and file handling within one organized and coherent project.

Its main strength is that it is not overly complex, yet it still appears professional and remains easy to explain during a presentation or discussion.
