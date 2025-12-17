# Quick Start Guide

Get up and running with Splitwise CLI in 5 minutes.

## One-Line Setup (macOS/Linux)

```bash
bash setup.sh && python cli.py
```

## Manual Setup

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup Database

```bash
python manage.py migrate
python manage.py seed_data
```

### 3. Run CLI

```bash
python cli.py
```

## First Commands to Try

```bash
# Show help
splitwise> HELP

# Check balance for user 1 (Rajesh from seed data)
splitwise> SHOW_BALANCE 1

# Show expenses for user 1
splitwise> SHOW_USER_EXPENSES 1

# Show group expenses (Group 1 is "Goa Trip")
splitwise> SHOW_GROUP_EXPENSES 1 1

# Settle up user 1
splitwise> SETTLE_USER 1

# Settle up group 1
splitwise> SETTLE_GROUP 1 1

# Exit
splitwise> EXIT
```

## Seed Data Users

| ID | Name           | Username      | Password |
|----|----------------|---------------|----------|
| 1  | Rajesh Sharma  | rajesh_sharma | pass123  |
| 2  | Priya Patel    | priya_patel   | pass123  |
| 3  | Amit Kumar     | amit_kumar    | pass123  |
| 4  | Sneha Reddy    | sneha_reddy   | pass123  |
| 5  | Vikram Singh   | vikram_singh  | pass123  |

## Seed Data Groups

| ID | Name                    | Creator        |
|----|-------------------------|----------------|
| 1  | Goa Trip 2025           | Rajesh Sharma  |
| 2  | Office Lunch Group      | Priya Patel    |
| 3  | Roommates - Mumbai      | Amit Kumar     |

## Try Adding Your Own Expense

```bash
# Register a new user
splitwise> REGISTER your_username "Your Name" your@email.com 9999999999 yourpass

# Create a group
splitwise> CREATE_GROUP "Your Group" 6

# Add an expense
# Format: ADD_EXPENSE <description> <amount> <created_by> <group_id> <paid_by> <owed_by>
splitwise> ADD_EXPENSE "Pizza" 1200 6 4 6:1200 6:400,1:400,2:400

# Check balance
splitwise> SHOW_BALANCE 6
```

## Documentation

- **[README.md](README.md)** - Complete documentation
- **[docs/COMMAND_PATTERN.md](docs/COMMAND_PATTERN.md)** - Command pattern explained
- **[docs/DEBT_SIMPLIFICATION.md](docs/DEBT_SIMPLIFICATION.md)** - Algorithm walkthrough
- **[docs/EXAMPLES.md](docs/EXAMPLES.md)** - More usage examples
- **[docs/QUIZ.md](docs/QUIZ.md)** - Test your understanding

## Troubleshooting

### Virtual environment not activated?
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Database issues?
```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_data
```

### Module not found?
```bash
pip install -r requirements.txt
```

## Project Structure

```
splitwise/
├── cli.py              # Run this for CLI
├── manage.py           # Django management
├── splitwise_app/      # Main app
│   ├── models/         # Database models
│   └── commands/       # Command pattern
├── docs/               # Documentation
└── README.md           # Full guide
```

## Next Steps

1. ✅ Run the CLI and try basic commands
2. 📚 Read the [Command Pattern docs](docs/COMMAND_PATTERN.md)
3. 🧮 Understand the [Debt Simplification algorithm](docs/DEBT_SIMPLIFICATION.md)
4. 🎯 Take the [Quiz](docs/QUIZ.md)
5. 💡 Check out [more examples](docs/EXAMPLES.md)

Happy coding! 🚀
