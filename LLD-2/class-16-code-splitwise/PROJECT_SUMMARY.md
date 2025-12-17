# Splitwise Django CLI - Project Summary

## 🎯 Project Overview

A fully-functional expense management system built with Django, implementing clean architecture principles, design patterns, and efficient algorithms.

## ✅ What's Implemented

### Core Features
- ✅ User registration and profile management
- ✅ Group creation and member management (creator-only permissions)
- ✅ Expense tracking with flexible splits
- ✅ Balance calculation per user
- ✅ Expense history viewing
- ✅ Smart debt settlement with transaction minimization
- ✅ Group-based expense organization

### Technical Implementation

#### 1. **Models** (Django ORM)
- `BaseModel` - Abstract base with audit fields (`created_at`, `updated_at`)
- `User` - User profile with hashed passwords
- `Group` - Expense groups with many-to-many relationships
- `GroupMembership` - Through model for group membership metadata
- `Expense` - Expense records with flexible currency support (INR)
- `UserExpense` - Junction model tracking paid/owed amounts per user

#### 2. **Command Design Pattern**
```
Command (Abstract) → Concrete Commands → Invoker → Parser → CLI
```

**Components:**
- `base.py` - Abstract Command interface
- `command_invoker.py` - Command executor with history
- `command_parser.py` - Input tokenizer and command factory
- `user_commands.py` - User operations (Register, Update, ShowBalance, ShowExpenses)
- `group_commands.py` - Group operations (Create, AddMember, RemoveMember, ShowExpenses)
- `expense_commands.py` - Expense operations (AddExpense with validation)
- `settle_commands.py` - Settlement algorithms (SettleUser, SettleGroup)

#### 3. **Debt Minimization Algorithm**
- **Algorithm**: Greedy with Max Heaps
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Approach**: Match largest debts with largest credits iteratively
- **Result**: Minimal number of transactions (at most n-1 for n people)

#### 4. **CLI Interface**
- Interactive command-line interface
- Tokenization with quoted string support
- Comprehensive help system
- Error handling with user-friendly messages
- Command history tracking

## 📁 File Structure

```
class-16-code-splitwise/
│
├── README.md                           # Main documentation
├── QUICKSTART.md                       # 5-minute setup guide
├── PROJECT_SUMMARY.md                  # This file
├── requirements.txt                    # Python dependencies
├── setup.sh                            # Automated setup script
├── manage.py                           # Django management
├── cli.py                              # CLI entry point
│
├── docs/
│   ├── COMMAND_PATTERN.md             # Command pattern with UML
│   ├── DEBT_SIMPLIFICATION.md         # Algorithm walkthrough
│   ├── EXAMPLES.md                    # Usage examples
│   └── QUIZ.md                        # Model design quiz (6 questions)
│
├── splitwise_project/                  # Django project
│   ├── settings.py                    # Configuration
│   ├── urls.py                        # URL routing
│   └── ...
│
└── splitwise_app/                      # Main application
    ├── models/                        # Data models
    │   ├── base.py                    # BaseModel (audit fields)
    │   ├── user.py                    # User model
    │   ├── group.py                   # Group & Membership models
    │   └── expense.py                 # Expense & UserExpense models
    │
    ├── commands/                      # Command pattern
    │   ├── base.py                    # Abstract Command
    │   ├── command_invoker.py         # Executor
    │   ├── command_parser.py          # Parser
    │   ├── user_commands.py           # User operations
    │   ├── group_commands.py          # Group operations
    │   ├── expense_commands.py        # Expense operations
    │   └── settle_commands.py         # Settlement algorithms
    │
    ├── management/commands/
    │   └── seed_data.py               # Database seeding
    │
    └── admin.py                       # Django admin configuration
```

## 🎓 Learning Objectives Covered

### 1. Django & Database Design
- ✅ Model inheritance (abstract base classes)
- ✅ Foreign keys and relationships
- ✅ Many-to-many with through models
- ✅ Query optimization
- ✅ Database indexes
- ✅ Audit fields pattern

### 2. Design Patterns
- ✅ Command Pattern (behavioral)
- ✅ Separation of concerns
- ✅ Single Responsibility Principle
- ✅ Open/Closed Principle (easy to extend)
- ✅ Dependency Inversion

### 3. Algorithms & Data Structures
- ✅ Greedy algorithms
- ✅ Heap data structure (priority queues)
- ✅ Graph theory (debt simplification)
- ✅ Time/space complexity analysis
- ✅ Algorithm correctness proof

### 4. Software Engineering
- ✅ Clean code principles
- ✅ Input validation
- ✅ Error handling
- ✅ Code organization
- ✅ Documentation
- ✅ DRY (Don't Repeat Yourself)

## 📊 Complexity Analysis

### Database Queries
- User balance: O(E) where E = number of expense records for user
- Group settlement: O(E_g + n log n) where E_g = group expenses, n = members
- Add expense: O(1) with proper indexes

### Algorithms
- Debt minimization: O(n log n) using heaps
- Balance calculation: O(E) where E = expense records
- Transaction generation: O(n) where n = people with non-zero balance

## 🧪 Validation & Testing

### Built-in Validations
- ✅ Username/email uniqueness
- ✅ Password strength (minimum length)
- ✅ Expense amount validation (paid = owed = total)
- ✅ Group membership checks
- ✅ Permission checks (only creator can add/remove members)
- ✅ Foreign key constraints

### Test Scenarios Covered
- Equal splits (most common)
- Unequal splits (based on consumption)
- Multiple payers
- Group vs personal expenses
- Edge cases (already settled, single person)

## 📝 Seed Data

### Users (5)
- Rajesh, Priya, Amit Kumar, Sneha Reddy, Vikram

### Groups (3)
- Goa Trip 2025 (4 members)
- Office Lunch Group (3 members)
- Roommates - Mumbai (2 members)

### Expenses (9)
- Hotel bookings, dinners, cabs, groceries, utility bills
- Amounts in INR (Indian Rupees)

## 🎯 Command Reference Quick Look

```bash
# User Management
REGISTER <username> <name> <email> <phone> <password>
UPDATE_USER <user_id> <field> <value>
SHOW_BALANCE <user_id>
SHOW_USER_EXPENSES <user_id>

# Group Management
CREATE_GROUP <name> <creator_id>
ADD_MEMBER <group_id> <user_id> <added_by_id>
REMOVE_MEMBER <group_id> <user_id> <removed_by_id>
SHOW_GROUP_EXPENSES <group_id> <user_id>

# Expense Management
ADD_EXPENSE <desc> <amount> <creator_id> <group_id> <paid_by> <owed_by>
# Format: paid_by and owed_by are user_id:amount,user_id:amount

# Settlement
SETTLE_USER <user_id>
SETTLE_GROUP <group_id> <user_id>

# Utility
HELP
EXIT
```

## 🚀 Setup Instructions

### Quick Start
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py migrate
python manage.py seed_data

# 4. Run CLI
python cli.py
```

### Or use setup script
```bash
bash setup.sh
python cli.py
```

## 📚 Documentation Files

| File | Description | Purpose |
|------|-------------|---------|
| `README.md` | Main documentation | Complete guide to the project |
| `QUICKSTART.md` | Quick setup | Get started in 5 minutes |
| `docs/COMMAND_PATTERN.md` | Design pattern | Command pattern with UML diagrams |
| `docs/DEBT_SIMPLIFICATION.md` | Algorithm | Debt minimization algorithm walkthrough |
| `docs/EXAMPLES.md` | Usage examples | Real-world scenarios |
| `docs/QUIZ.md` | Quiz questions | Test understanding (6 questions) |
| `PROJECT_SUMMARY.md` | This file | Project overview |

## 🎨 Design Decisions

### Why Command Pattern?
- Separates parsing from execution
- Easy to add new commands
- Testable in isolation
- Command history tracking
- Better error handling

### Why Through Model for Groups?
- Store membership metadata (joined_at)
- Extensible (can add role, added_by, etc.)
- Maintains referential integrity
- Allows complex queries

### Why Calculate Balance Dynamically?
- Single source of truth (expenses are source)
- No risk of inconsistency
- Can show per-person breakdown
- Easier to debug and verify

### Why Greedy Algorithm?
- Optimal for debt minimization
- Efficient O(n log n)
- Easy to understand and implement
- Proven correctness

## 🔍 Key Features Demonstrated

### 1. Clean Architecture
```
CLI → Parser → Command → Invoker → Models → Database
```

### 2. Separation of Concerns
- Models: Data structure
- Commands: Business logic
- Parser: Input handling
- Invoker: Execution control
- CLI: User interface

### 3. Design Principles
- Single Responsibility
- Open/Closed (easy to extend)
- Liskov Substitution (commands are interchangeable)
- Dependency Inversion (depends on abstractions)
- DRY (BaseModel, command pattern)

### 4. Error Handling
- Validation before execution
- Clear error messages
- Fail fast approach
- Exception propagation

## 🎓 For Students

### What You Can Learn
1. How to design models with relationships
2. When and how to use design patterns
3. Algorithm optimization techniques
4. Clean code and architecture
5. Django ORM best practices
6. CLI application development

### Study Path
1. ✅ Set up and run the project
2. ✅ Try all commands with seed data
3. 📚 Read Command Pattern documentation
4. 🧮 Understand debt minimization algorithm
5. 🎯 Take the quiz
6. 💡 Try adding new features

### Suggested Exercises
1. Add EDIT_EXPENSE command
2. Implement DELETE_EXPENSE with validation
3. Add support for multiple currencies
4. Create a VIEW_GROUP command
5. Add expense categories
6. Implement recurring expenses

## 🏆 Project Highlights

### What Makes This Special
- ✨ Production-ready code structure
- 📚 Comprehensive documentation
- 🎯 Educational quiz questions
- 💡 Real-world scenarios
- 🧮 Optimized algorithms
- 🔧 Easy to extend
- 📊 Well-commented code
- 🌍 Indian context (names, amounts)

### Industry Best Practices
- ✅ Virtual environment usage
- ✅ requirements.txt for dependencies
- ✅ .gitignore for version control
- ✅ Abstract base models for common fields
- ✅ Through models for metadata
- ✅ Index optimization
- ✅ Command history tracking
- ✅ Validation at multiple levels

## 🤝 Contributing & Extending

### Easy Extensions
1. **Add REST API**: Use Django REST Framework
2. **Add Tests**: Unit tests for models and commands
3. **Add Frontend**: Web UI with Django templates
4. **Add Features**: Categories, recurring expenses, currency conversion
5. **Optimize**: Query optimization, caching

### Architecture Supports
- Easy to add new commands (just implement Command interface)
- Easy to change settlement algorithm (just modify settle_commands.py)
- Easy to add new models (inherit from BaseModel)
- Easy to change database (Django ORM abstraction)

## 📈 Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Register User | O(1) | Single insert |
| Add Expense | O(k) | k = number of users in expense |
| Show Balance | O(E) | E = user's expense count |
| Show Expenses | O(E) | With pagination can be O(1) |
| Settle User | O(E + n log n) | E = expenses, n = related users |
| Settle Group | O(E_g + n log n) | E_g = group expenses |

## 🎉 Conclusion

This project demonstrates a complete, well-architected expense management system with:
- Clean code and design patterns
- Efficient algorithms
- Comprehensive documentation
- Real-world applicability
- Educational value

Perfect for learning backend development, design patterns, algorithms, and Django!

---

**Created for**: Backend LLD Python Course - August 2025 Batch
**Documentation**: 5 comprehensive guides
**Quiz Questions**: 6 detailed scenarios

Happy Learning! 🚀📚
