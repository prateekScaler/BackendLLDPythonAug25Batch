"""
User Service - A Practical TDD Example

This module was built using TDD. Each method corresponds to a test
that was written FIRST, then the implementation was added to make it pass.

TDD Progression:
1. Started with User class creation
2. Added UserRepository for storage
3. Added UserService for business logic
4. Added validation rules
5. Added error handling

To see how this was built step-by-step, read the test file alongside this code.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum
import re
import hashlib


class UserRole(Enum):
    """User roles for authorization"""
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"


class UserServiceError(Exception):
    """Base exception for user service errors"""
    pass


class UserNotFoundError(UserServiceError):
    """Raised when a user is not found"""
    pass


class DuplicateEmailError(UserServiceError):
    """Raised when email already exists"""
    pass


class ValidationError(UserServiceError):
    """Raised when validation fails"""
    pass


@dataclass
class User:
    """
    User entity representing a user in the system.

    Built with TDD:
    - Test 1: test_create_user_with_required_fields
    - Test 2: test_user_has_default_role
    - Test 3: test_user_created_at_is_set
    """
    id: Optional[int]
    email: str
    name: str
    password_hash: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """Convert user to dictionary (for API responses)"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class PasswordHasher:
    """
    Password hashing utility.

    Built with TDD:
    - Test 1: test_hash_password_returns_hash
    - Test 2: test_verify_password_returns_true_for_correct
    - Test 3: test_verify_password_returns_false_for_incorrect
    """

    @staticmethod
    def hash(password: str) -> str:
        """Hash a password using SHA-256 (simplified for demo)"""
        # In production, use bcrypt or argon2
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify(password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        return PasswordHasher.hash(password) == password_hash


class EmailValidator:
    """
    Email validation utility.

    Built with TDD:
    - Test 1: test_valid_email_returns_true
    - Test 2: test_invalid_email_returns_false
    - Test 3: test_email_without_at_is_invalid
    - Test 4: test_email_without_domain_is_invalid
    """

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    @classmethod
    def is_valid(cls, email: str) -> bool:
        """Check if email format is valid"""
        if not email:
            return False
        return bool(cls.EMAIL_REGEX.match(email))


class PasswordValidator:
    """
    Password validation utility.

    Built with TDD:
    - Test 1: test_password_too_short_is_invalid
    - Test 2: test_password_without_uppercase_is_invalid
    - Test 3: test_password_without_number_is_invalid
    - Test 4: test_valid_password_passes_all_checks
    """

    MIN_LENGTH = 8

    @classmethod
    def validate(cls, password: str) -> tuple[bool, List[str]]:
        """
        Validate password and return (is_valid, list of errors)
        """
        errors = []

        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters")

        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")

        return (len(errors) == 0, errors)


class UserRepository:
    """
    In-memory user repository (simulates database).

    Built with TDD:
    - Test 1: test_save_user_assigns_id
    - Test 2: test_find_by_id_returns_user
    - Test 3: test_find_by_id_returns_none_for_missing
    - Test 4: test_find_by_email_returns_user
    - Test 5: test_get_all_returns_all_users
    - Test 6: test_delete_removes_user
    """

    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1

    def save(self, user: User) -> User:
        """Save a user, assigning an ID if new"""
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        else:
            user.updated_at = datetime.now()

        self._users[user.id] = user
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by ID"""
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        for user in self._users.values():
            if user.email.lower() == email.lower():
                return user
        return None

    def get_all(self) -> List[User]:
        """Get all users"""
        return list(self._users.values())

    def delete(self, user_id: int) -> bool:
        """Delete a user by ID"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def count(self) -> int:
        """Count total users"""
        return len(self._users)


class UserService:
    """
    User Service - Business logic layer for user operations.

    Built with TDD - each public method has corresponding tests:
    - register_user: Tests for validation, duplicate check, creation
    - authenticate: Tests for correct/incorrect credentials
    - get_user: Tests for found/not found cases
    - update_user: Tests for updating existing users
    - deactivate_user: Tests for soft-delete functionality
    - list_users: Tests for filtering and pagination
    """

    def __init__(self, repository: Optional[UserRepository] = None):
        self.repository = repository or UserRepository()

    def register_user(self, email: str, name: str, password: str) -> User:
        """
        Register a new user.

        TDD Tests:
        - test_register_user_creates_user
        - test_register_user_with_invalid_email_raises
        - test_register_user_with_weak_password_raises
        - test_register_user_with_duplicate_email_raises
        """
        # Validate email
        if not EmailValidator.is_valid(email):
            raise ValidationError("Invalid email format")

        # Validate password
        is_valid, errors = PasswordValidator.validate(password)
        if not is_valid:
            raise ValidationError("; ".join(errors))

        # Check for duplicate email
        if self.repository.find_by_email(email):
            raise DuplicateEmailError(f"Email {email} is already registered")

        # Create and save user
        user = User(
            id=None,
            email=email.lower(),
            name=name.strip(),
            password_hash=PasswordHasher.hash(password)
        )

        return self.repository.save(user)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.

        TDD Tests:
        - test_authenticate_with_correct_credentials_returns_user
        - test_authenticate_with_wrong_password_returns_none
        - test_authenticate_with_unknown_email_returns_none
        - test_authenticate_inactive_user_returns_none
        """
        user = self.repository.find_by_email(email)

        if not user:
            return None

        if not user.is_active:
            return None

        if not PasswordHasher.verify(password, user.password_hash):
            return None

        return user

    def get_user(self, user_id: int) -> User:
        """
        Get a user by ID.

        TDD Tests:
        - test_get_user_returns_user
        - test_get_user_not_found_raises_error
        """
        user = self.repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.

        TDD Tests:
        - test_get_user_by_email_returns_user
        - test_get_user_by_email_returns_none_for_missing
        """
        return self.repository.find_by_email(email)

    def update_user(self, user_id: int, name: Optional[str] = None,
                    role: Optional[UserRole] = None) -> User:
        """
        Update a user's information.

        TDD Tests:
        - test_update_user_name
        - test_update_user_role
        - test_update_user_not_found_raises_error
        """
        user = self.get_user(user_id)

        if name is not None:
            user.name = name.strip()

        if role is not None:
            user.role = role

        return self.repository.save(user)

    def change_password(self, user_id: int, old_password: str,
                        new_password: str) -> bool:
        """
        Change a user's password.

        TDD Tests:
        - test_change_password_with_correct_old_password
        - test_change_password_with_wrong_old_password_fails
        - test_change_password_with_weak_new_password_fails
        """
        user = self.get_user(user_id)

        # Verify old password
        if not PasswordHasher.verify(old_password, user.password_hash):
            return False

        # Validate new password
        is_valid, errors = PasswordValidator.validate(new_password)
        if not is_valid:
            raise ValidationError("; ".join(errors))

        # Update password
        user.password_hash = PasswordHasher.hash(new_password)
        self.repository.save(user)
        return True

    def deactivate_user(self, user_id: int) -> User:
        """
        Deactivate a user (soft delete).

        TDD Tests:
        - test_deactivate_user_sets_inactive
        - test_deactivate_user_not_found_raises_error
        """
        user = self.get_user(user_id)
        user.is_active = False
        return self.repository.save(user)

    def activate_user(self, user_id: int) -> User:
        """
        Activate a deactivated user.

        TDD Tests:
        - test_activate_user_sets_active
        """
        user = self.get_user(user_id)
        user.is_active = True
        return self.repository.save(user)

    def delete_user(self, user_id: int) -> bool:
        """
        Permanently delete a user.

        TDD Tests:
        - test_delete_user_removes_from_repository
        - test_delete_nonexistent_user_returns_false
        """
        return self.repository.delete(user_id)

    def list_users(self, active_only: bool = False,
                   role: Optional[UserRole] = None) -> List[User]:
        """
        List users with optional filtering.

        TDD Tests:
        - test_list_users_returns_all_users
        - test_list_users_active_only
        - test_list_users_by_role
        """
        users = self.repository.get_all()

        if active_only:
            users = [u for u in users if u.is_active]

        if role is not None:
            users = [u for u in users if u.role == role]

        return users

    def get_user_count(self) -> int:
        """Get total user count"""
        return self.repository.count()


# API-style response wrappers (simulating REST API patterns)

class APIResponse:
    """Helper class for API-style responses"""

    @staticmethod
    def success(data, message: str = "Success") -> Dict:
        return {
            "success": True,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message: str, code: str = "ERROR") -> Dict:
        return {
            "success": False,
            "error": {
                "code": code,
                "message": message
            }
        }


class UserAPI:
    """
    API-style wrapper for UserService.
    Simulates how you might expose the service as REST endpoints.

    Built with TDD:
    - Each endpoint method has corresponding integration tests
    """

    def __init__(self, service: Optional[UserService] = None):
        self.service = service or UserService()

    def register(self, data: Dict) -> Dict:
        """
        POST /api/users/register

        TDD Tests:
        - test_api_register_success
        - test_api_register_validation_error
        - test_api_register_duplicate_email
        """
        try:
            user = self.service.register_user(
                email=data.get("email", ""),
                name=data.get("name", ""),
                password=data.get("password", "")
            )
            return APIResponse.success(
                user.to_dict(),
                "User registered successfully"
            )
        except ValidationError as e:
            return APIResponse.error(str(e), "VALIDATION_ERROR")
        except DuplicateEmailError as e:
            return APIResponse.error(str(e), "DUPLICATE_EMAIL")

    def login(self, data: Dict) -> Dict:
        """
        POST /api/users/login

        TDD Tests:
        - test_api_login_success
        - test_api_login_invalid_credentials
        """
        user = self.service.authenticate(
            email=data.get("email", ""),
            password=data.get("password", "")
        )

        if user:
            return APIResponse.success(
                {"user": user.to_dict(), "token": "fake-jwt-token"},
                "Login successful"
            )
        else:
            return APIResponse.error(
                "Invalid email or password",
                "INVALID_CREDENTIALS"
            )

    def get_user(self, user_id: int) -> Dict:
        """
        GET /api/users/{user_id}

        TDD Tests:
        - test_api_get_user_success
        - test_api_get_user_not_found
        """
        try:
            user = self.service.get_user(user_id)
            return APIResponse.success(user.to_dict())
        except UserNotFoundError as e:
            return APIResponse.error(str(e), "NOT_FOUND")

    def update_user(self, user_id: int, data: Dict) -> Dict:
        """
        PUT /api/users/{user_id}

        TDD Tests:
        - test_api_update_user_success
        - test_api_update_user_not_found
        """
        try:
            role = None
            if "role" in data:
                role = UserRole(data["role"])

            user = self.service.update_user(
                user_id=user_id,
                name=data.get("name"),
                role=role
            )
            return APIResponse.success(
                user.to_dict(),
                "User updated successfully"
            )
        except UserNotFoundError as e:
            return APIResponse.error(str(e), "NOT_FOUND")
        except ValueError as e:
            return APIResponse.error(str(e), "VALIDATION_ERROR")

    def list_users(self, params: Optional[Dict] = None) -> Dict:
        """
        GET /api/users

        TDD Tests:
        - test_api_list_users_returns_all
        - test_api_list_users_filtered
        """
        params = params or {}
        active_only = params.get("active_only", False)
        role = None
        if "role" in params:
            role = UserRole(params["role"])

        users = self.service.list_users(active_only=active_only, role=role)
        return APIResponse.success({
            "users": [u.to_dict() for u in users],
            "total": len(users)
        })
