💳 Online Banking Management System
A command-line based Online Banking Management System built with Python and SQL. This project simulates essential banking operations such as account management, fund transfers, loan tracking, and transaction history — all backed by a secure database.
📁 Project Structure
online-banking-management/
├── main.py             # Main application logic
├── db_setup.sql        # SQL script to initialize the database
├── screenshots/        # Screenshots of sample outputs
└── README.md           # Project documentation


🚀 Features
This system provides a menu-driven interface with the following modules:
- 🔐 Account Settings: Create, update, or delete user accounts
- 💰 Check Balance: View current account balance
- 💳 Cards: Manage debit/credit card details
- 🏦 Loan: Apply for loans and view loan status
- 🔄 Transfer Funds: Send money between accounts securely
- 📜 Transaction History: View detailed logs of all transactions
🛠️ Technologies Used
- Python 3 for application logic (main.py)
- SQLite / MySQL for database management (db_setup.sql)
- SQL for schema creation and data manipulation
- Command-line interface for user interaction
🧱 Setup Instructions
- Clone the repository
git clone https://github.com/purvii123/Online-Banking-Management-System
cd online-banking-management
- Set up the database
- Run the SQL script to initialize the database:
sqlite3 bank.db < db_setup.sql
- (Replace sqlite3 with your preferred SQL engine if needed)
- Run the application
python main.py


🖼️ Screenshots
Screenshots of the application in action are available in the screenshots/ folder, showcasing:
- Account creation and updates
- Balance checks and fund transfers
- Loan applications
- Transaction logs
📌 Future Improvements
- Add GUI using Tkinter or Flask
- Implement user authentication and role-based access
- Add support for multiple currencies and interest calculations
- Export transaction history to PDF/CSV
- Integrate SMS/email notifications
📄 License
This project is licensed under the MIT License. Feel free to use and modify it for educational or commercial purposes.


