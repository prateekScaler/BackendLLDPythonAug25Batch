"""
TDD Tests for User Service

This test file demonstrates TDD practices:
1. Tests were written BEFORE the implementation
2. Each test focuses on one behavior
3. Tests follow the Arrange-Act-Assert pattern
4. Tests are grouped logically by component

HOW TO RUN:
    pytest test_tdd_example_user_service.py -v
    pytest test_tdd_example_user_service.py -v --cov=tdd_example_user_service

TDD Journey (how these tests were written):
- Step 1: Write test_create_user_with_required_fields -> implement User class
- Step 2: Write test_hash_password_returns_hash -> implement PasswordHasher
- Step 3: Write test_valid_email_returns_true -> implement EmailValidator
- Step 4: Write repository tests -> implement UserRepository
- Step 5: Write service tests -> implement UserService
- Step 6: Write API tests -> implement UserAPI
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from tdd_example_user_service import (
    User,
    UserRole,
    PasswordHasher,
    EmailValidator,
    PasswordValidator,
    UserRepository,
    UserService,
    UserAPI,
    UserNotFoundError,
    DuplicateEmailError,
    ValidationError,
)


# =============================================================================
# Section 1: User Entity Tests
# =============================================================================

class TestUser:
    """
    TDD Step 1: Define the User entity
    These tests were written first to define what a User should look like.
    """

    def test_create_user_with_required_fields(self):
        """First test: Define minimum user requirements"""
        # Arrange & Act
        user = User(
            id=1,
            email="john@example.com",
            name="John Doe",
            password_hash="hashed_password"
        )

        # Assert
        assert user.id == 1
        assert user.email == "john@example.com"
        assert user.name == "John Doe"
        assert user.password_hash == "hashed_password"

    def test_user_has_default_role(self):
        """Second test: Users should have a default role"""
        user = User(
            id=1,
            email="john@example.com",
            name="John Doe",
            password_hash="hashed"
        )

        assert user.role == UserRole.USER

    def test_user_is_active_by_default(self):
        """Third test: Users should be active by default"""
        user = User(
            id=1,
            email="john@example.com",
            name="John Doe",
            password_hash="hashed"
        )

        assert user.is_active is True

    def test_user_created_at_is_set(self):
        """Fourth test: Created timestamp should be set"""
        before = datetime.now()
        user = User(
            id=1,
            email="john@example.com",
            name="John Doe",
            password_hash="hashed"
        )
        after = datetime.now()

        assert before <= user.created_at <= after

    def test_user_to_dict_returns_dictionary(self):
        """Fifth test: Users should be serializable to dict"""
        user = User(
            id=1,
            email="john@example.com",
            name="John Doe",
            password_hash="hashed"
        )

        result = user.to_dict()

        assert result["id"] == 1
        assert result["email"] == "john@example.com"
        assert result["name"] == "John Doe"
        assert "password_hash" not in result  # Should not expose password


# =============================================================================
# Section 2: Password Hasher Tests
# =============================================================================

class TestPasswordHasher:
    """
    TDD Step 2: Define password hashing behavior
    """

    def test_hash_password_returns_hash(self):
        """Hashing a password should return a hash string"""
        password = "SecurePass123"

        result = PasswordHasher.hash(password)

        assert result is not None
        assert result != password  # Hash should be different from input
        assert len(result) == 64  # SHA-256 produces 64 hex characters

    def test_same_password_produces_same_hash(self):
        """Same password should produce same hash (deterministic)"""
        password = "SecurePass123"

        hash1 = PasswordHasher.hash(password)
        hash2 = PasswordHasher.hash(password)

        assert hash1 == hash2

    def test_different_passwords_produce_different_hashes(self):
        """Different passwords should produce different hashes"""
        hash1 = PasswordHasher.hash("Password1")
        hash2 = PasswordHasher.hash("Password2")

        assert hash1 != hash2

    def test_verify_password_returns_true_for_correct(self):
        """Verify should return True for correct password"""
        password = "SecurePass123"
        password_hash = PasswordHasher.hash(password)

        result = PasswordHasher.verify(password, password_hash)

        assert result is True

    def test_verify_password_returns_false_for_incorrect(self):
        """Verify should return False for incorrect password"""
        password_hash = PasswordHasher.hash("CorrectPassword")

        result = PasswordHasher.verify("WrongPassword", password_hash)

        assert result is False


# =============================================================================
# Section 3: Email Validator Tests
# =============================================================================

class TestEmailValidator:
    """
    TDD Step 3: Define email validation rules
    """

    def test_valid_email_returns_true(self):
        """Standard email format should be valid"""
        assert EmailValidator.is_valid("user@example.com") is True
        assert EmailValidator.is_valid("user.name@example.com") is True
        assert EmailValidator.is_valid("user+tag@example.co.uk") is True

    def test_email_without_at_is_invalid(self):
        """Email without @ symbol should be invalid"""
        assert EmailValidator.is_valid("userexample.com") is False

    def test_email_without_domain_is_invalid(self):
        """Email without proper domain should be invalid"""
        assert EmailValidator.is_valid("user@") is False
        assert EmailValidator.is_valid("user@.com") is False

    def test_email_without_tld_is_invalid(self):
        """Email without top-level domain should be invalid"""
        assert EmailValidator.is_valid("user@example") is False

    def test_empty_email_is_invalid(self):
        """Empty string should be invalid"""
        assert EmailValidator.is_valid("") is False

    def test_none_email_is_invalid(self):
        """None should be invalid"""
        assert EmailValidator.is_valid(None) is False


# =============================================================================
# Section 4: Password Validator Tests
# =============================================================================

class TestPasswordValidator:
    """
    TDD Step 4: Define password strength rules
    """

    def test_password_too_short_is_invalid(self):
        """Password under 8 characters should fail"""
        is_valid, errors = PasswordValidator.validate("Short1A")

        assert is_valid is False
        assert any("8 characters" in e for e in errors)

    def test_password_without_uppercase_is_invalid(self):
        """Password without uppercase should fail"""
        is_valid, errors = PasswordValidator.validate("lowercase123")

        assert is_valid is False
        assert any("uppercase" in e for e in errors)

    def test_password_without_lowercase_is_invalid(self):
        """Password without lowercase should fail"""
        is_valid, errors = PasswordValidator.validate("UPPERCASE123")

        assert is_valid is False
        assert any("lowercase" in e for e in errors)

    def test_password_without_number_is_invalid(self):
        """Password without number should fail"""
        is_valid, errors = PasswordValidator.validate("NoNumbers!")

        assert is_valid is False
        assert any("number" in e for e in errors)

    def test_valid_password_passes_all_checks(self):
        """Password meeting all criteria should pass"""
        is_valid, errors = PasswordValidator.validate("SecurePass123")

        assert is_valid is True
        assert errors == []

    def test_validator_returns_multiple_errors(self):
        """Validator should return all applicable errors"""
        is_valid, errors = PasswordValidator.validate("short")

        assert is_valid is False
        assert len(errors) >= 2  # Too short + missing uppercase + missing number


# =============================================================================
# Section 5: User Repository Tests
# =============================================================================

class TestUserRepository:
    """
    TDD Step 5: Define data access layer behavior
    """

    @pytest.fixture
    def repository(self):
        """Fresh repository for each test"""
        return UserRepository()

    @pytest.fixture
    def sample_user(self):
        """Sample user for testing"""
        return User(
            id=None,
            email="test@example.com",
            name="Test User",
            password_hash="hashed"
        )

    def test_save_user_assigns_id(self, repository, sample_user):
        """Saving a new user should assign an ID"""
        assert sample_user.id is None

        saved_user = repository.save(sample_user)

        assert saved_user.id is not None
        assert saved_user.id == 1

    def test_save_multiple_users_assigns_sequential_ids(self, repository):
        """Multiple saves should assign sequential IDs"""
        user1 = User(None, "a@example.com", "A", "hash")
        user2 = User(None, "b@example.com", "B", "hash")

        repository.save(user1)
        repository.save(user2)

        assert user1.id == 1
        assert user2.id == 2

    def test_find_by_id_returns_user(self, repository, sample_user):
        """Finding by ID should return the correct user"""
        repository.save(sample_user)

        found = repository.find_by_id(sample_user.id)

        assert found is not None
        assert found.email == "test@example.com"

    def test_find_by_id_returns_none_for_missing(self, repository):
        """Finding non-existent ID should return None"""
        found = repository.find_by_id(999)

        assert found is None

    def test_find_by_email_returns_user(self, repository, sample_user):
        """Finding by email should return the correct user"""
        repository.save(sample_user)

        found = repository.find_by_email("test@example.com")

        assert found is not None
        assert found.name == "Test User"

    def test_find_by_email_is_case_insensitive(self, repository, sample_user):
        """Email lookup should be case insensitive"""
        repository.save(sample_user)

        found = repository.find_by_email("TEST@EXAMPLE.COM")

        assert found is not None

    def test_get_all_returns_all_users(self, repository):
        """get_all should return all saved users"""
        repository.save(User(None, "a@example.com", "A", "hash"))
        repository.save(User(None, "b@example.com", "B", "hash"))
        repository.save(User(None, "c@example.com", "C", "hash"))

        users = repository.get_all()

        assert len(users) == 3

    def test_delete_removes_user(self, repository, sample_user):
        """Delete should remove user from repository"""
        repository.save(sample_user)
        user_id = sample_user.id

        result = repository.delete(user_id)

        assert result is True
        assert repository.find_by_id(user_id) is None

    def test_delete_nonexistent_returns_false(self, repository):
        """Deleting non-existent user should return False"""
        result = repository.delete(999)

        assert result is False

    def test_count_returns_user_count(self, repository):
        """Count should return number of users"""
        assert repository.count() == 0

        repository.save(User(None, "a@example.com", "A", "hash"))
        assert repository.count() == 1

        repository.save(User(None, "b@example.com", "B", "hash"))
        assert repository.count() == 2


# =============================================================================
# Section 6: User Service Tests
# =============================================================================

class TestUserService:
    """
    TDD Step 6: Define business logic layer
    This is where most of the application logic lives.
    """

    @pytest.fixture
    def service(self):
        """Fresh service for each test"""
        return UserService()

    # --- Registration Tests ---

    def test_register_user_creates_user(self, service):
        """Registering should create a new user"""
        user = service.register_user(
            email="new@example.com",
            name="New User",
            password="SecurePass123"
        )

        assert user.id is not None
        assert user.email == "new@example.com"
        assert user.name == "New User"

    def test_register_user_hashes_password(self, service):
        """Password should be hashed, not stored plain"""
        user = service.register_user(
            email="new@example.com",
            name="New User",
            password="SecurePass123"
        )

        assert user.password_hash != "SecurePass123"
        assert PasswordHasher.verify("SecurePass123", user.password_hash)

    def test_register_user_lowercases_email(self, service):
        """Email should be stored lowercase"""
        user = service.register_user(
            email="NEW@EXAMPLE.COM",
            name="New User",
            password="SecurePass123"
        )

        assert user.email == "new@example.com"

    def test_register_user_trims_name(self, service):
        """Name should be trimmed of whitespace"""
        user = service.register_user(
            email="new@example.com",
            name="  Spaced Name  ",
            password="SecurePass123"
        )

        assert user.name == "Spaced Name"

    def test_register_user_with_invalid_email_raises(self, service):
        """Invalid email should raise ValidationError"""
        with pytest.raises(ValidationError, match="Invalid email"):
            service.register_user(
                email="invalid-email",
                name="User",
                password="SecurePass123"
            )

    def test_register_user_with_weak_password_raises(self, service):
        """Weak password should raise ValidationError"""
        with pytest.raises(ValidationError):
            service.register_user(
                email="user@example.com",
                name="User",
                password="weak"
            )

    def test_register_user_with_duplicate_email_raises(self, service):
        """Duplicate email should raise DuplicateEmailError"""
        service.register_user(
            email="taken@example.com",
            name="First User",
            password="SecurePass123"
        )

        with pytest.raises(DuplicateEmailError):
            service.register_user(
                email="taken@example.com",
                name="Second User",
                password="SecurePass123"
            )

    # --- Authentication Tests ---

    def test_authenticate_with_correct_credentials_returns_user(self, service):
        """Correct credentials should return user"""
        service.register_user(
            email="auth@example.com",
            name="Auth User",
            password="SecurePass123"
        )

        user = service.authenticate("auth@example.com", "SecurePass123")

        assert user is not None
        assert user.email == "auth@example.com"

    def test_authenticate_with_wrong_password_returns_none(self, service):
        """Wrong password should return None"""
        service.register_user(
            email="auth@example.com",
            name="Auth User",
            password="SecurePass123"
        )

        user = service.authenticate("auth@example.com", "WrongPass123")

        assert user is None

    def test_authenticate_with_unknown_email_returns_none(self, service):
        """Unknown email should return None"""
        user = service.authenticate("unknown@example.com", "AnyPass123")

        assert user is None

    def test_authenticate_inactive_user_returns_none(self, service):
        """Inactive users should not be able to authenticate"""
        registered = service.register_user(
            email="inactive@example.com",
            name="Inactive User",
            password="SecurePass123"
        )
        service.deactivate_user(registered.id)

        user = service.authenticate("inactive@example.com", "SecurePass123")

        assert user is None

    # --- Get User Tests ---

    def test_get_user_returns_user(self, service):
        """get_user should return user by ID"""
        registered = service.register_user(
            email="find@example.com",
            name="Find Me",
            password="SecurePass123"
        )

        found = service.get_user(registered.id)

        assert found.email == "find@example.com"

    def test_get_user_not_found_raises_error(self, service):
        """get_user should raise UserNotFoundError for missing ID"""
        with pytest.raises(UserNotFoundError):
            service.get_user(999)

    def test_get_user_by_email_returns_user(self, service):
        """get_user_by_email should return user"""
        service.register_user(
            email="find@example.com",
            name="Find Me",
            password="SecurePass123"
        )

        found = service.get_user_by_email("find@example.com")

        assert found is not None
        assert found.name == "Find Me"

    def test_get_user_by_email_returns_none_for_missing(self, service):
        """get_user_by_email should return None if not found"""
        found = service.get_user_by_email("notfound@example.com")

        assert found is None

    # --- Update User Tests ---

    def test_update_user_name(self, service):
        """Updating name should persist"""
        registered = service.register_user(
            email="update@example.com",
            name="Old Name",
            password="SecurePass123"
        )

        updated = service.update_user(registered.id, name="New Name")

        assert updated.name == "New Name"

    def test_update_user_role(self, service):
        """Updating role should persist"""
        registered = service.register_user(
            email="admin@example.com",
            name="Admin",
            password="SecurePass123"
        )

        updated = service.update_user(registered.id, role=UserRole.ADMIN)

        assert updated.role == UserRole.ADMIN

    def test_update_user_sets_updated_at(self, service):
        """Updating should set updated_at timestamp"""
        registered = service.register_user(
            email="update@example.com",
            name="User",
            password="SecurePass123"
        )
        assert registered.updated_at is None

        updated = service.update_user(registered.id, name="New Name")

        assert updated.updated_at is not None

    def test_update_user_not_found_raises_error(self, service):
        """Updating non-existent user should raise error"""
        with pytest.raises(UserNotFoundError):
            service.update_user(999, name="New Name")

    # --- Change Password Tests ---

    def test_change_password_with_correct_old_password(self, service):
        """Changing password with correct old password should succeed"""
        registered = service.register_user(
            email="pwd@example.com",
            name="User",
            password="OldPass123"
        )

        result = service.change_password(
            registered.id,
            old_password="OldPass123",
            new_password="NewPass456"
        )

        assert result is True
        # Verify new password works
        assert service.authenticate("pwd@example.com", "NewPass456") is not None

    def test_change_password_with_wrong_old_password_fails(self, service):
        """Changing password with wrong old password should fail"""
        registered = service.register_user(
            email="pwd@example.com",
            name="User",
            password="OldPass123"
        )

        result = service.change_password(
            registered.id,
            old_password="WrongPass",
            new_password="NewPass456"
        )

        assert result is False

    def test_change_password_with_weak_new_password_fails(self, service):
        """Changing to weak password should raise ValidationError"""
        registered = service.register_user(
            email="pwd@example.com",
            name="User",
            password="OldPass123"
        )

        with pytest.raises(ValidationError):
            service.change_password(
                registered.id,
                old_password="OldPass123",
                new_password="weak"
            )

    # --- Deactivate/Activate Tests ---

    def test_deactivate_user_sets_inactive(self, service):
        """Deactivating should set is_active to False"""
        registered = service.register_user(
            email="active@example.com",
            name="Active User",
            password="SecurePass123"
        )

        deactivated = service.deactivate_user(registered.id)

        assert deactivated.is_active is False

    def test_activate_user_sets_active(self, service):
        """Activating should set is_active to True"""
        registered = service.register_user(
            email="active@example.com",
            name="User",
            password="SecurePass123"
        )
        service.deactivate_user(registered.id)

        activated = service.activate_user(registered.id)

        assert activated.is_active is True

    # --- Delete Tests ---

    def test_delete_user_removes_from_repository(self, service):
        """Deleting should remove user permanently"""
        registered = service.register_user(
            email="delete@example.com",
            name="Delete Me",
            password="SecurePass123"
        )

        result = service.delete_user(registered.id)

        assert result is True
        with pytest.raises(UserNotFoundError):
            service.get_user(registered.id)

    def test_delete_nonexistent_user_returns_false(self, service):
        """Deleting non-existent user should return False"""
        result = service.delete_user(999)

        assert result is False

    # --- List Users Tests ---

    def test_list_users_returns_all_users(self, service):
        """list_users should return all registered users"""
        service.register_user("a@example.com", "A", "SecurePass123")
        service.register_user("b@example.com", "B", "SecurePass123")

        users = service.list_users()

        assert len(users) == 2

    def test_list_users_active_only(self, service):
        """list_users with active_only should filter inactive"""
        user1 = service.register_user("a@example.com", "A", "SecurePass123")
        service.register_user("b@example.com", "B", "SecurePass123")
        service.deactivate_user(user1.id)

        users = service.list_users(active_only=True)

        assert len(users) == 1
        assert users[0].email == "b@example.com"

    def test_list_users_by_role(self, service):
        """list_users with role filter should filter by role"""
        user1 = service.register_user("admin@example.com", "Admin", "SecurePass123")
        service.register_user("user@example.com", "User", "SecurePass123")
        service.update_user(user1.id, role=UserRole.ADMIN)

        users = service.list_users(role=UserRole.ADMIN)

        assert len(users) == 1
        assert users[0].email == "admin@example.com"


# =============================================================================
# Section 7: API Layer Tests (Integration-style)
# =============================================================================

class TestUserAPI:
    """
    TDD Step 7: Define API interface
    These tests ensure the API layer works correctly end-to-end.
    """

    @pytest.fixture
    def api(self):
        """Fresh API instance for each test"""
        return UserAPI()

    # --- Register Endpoint Tests ---

    def test_api_register_success(self, api):
        """Successful registration should return success response"""
        response = api.register({
            "email": "new@example.com",
            "name": "New User",
            "password": "SecurePass123"
        })

        assert response["success"] is True
        assert "data" in response
        assert response["data"]["email"] == "new@example.com"

    def test_api_register_validation_error(self, api):
        """Validation error should return error response"""
        response = api.register({
            "email": "invalid-email",
            "name": "User",
            "password": "SecurePass123"
        })

        assert response["success"] is False
        assert response["error"]["code"] == "VALIDATION_ERROR"

    def test_api_register_duplicate_email(self, api):
        """Duplicate email should return error response"""
        api.register({
            "email": "taken@example.com",
            "name": "First",
            "password": "SecurePass123"
        })

        response = api.register({
            "email": "taken@example.com",
            "name": "Second",
            "password": "SecurePass123"
        })

        assert response["success"] is False
        assert response["error"]["code"] == "DUPLICATE_EMAIL"

    # --- Login Endpoint Tests ---

    def test_api_login_success(self, api):
        """Successful login should return user and token"""
        api.register({
            "email": "login@example.com",
            "name": "User",
            "password": "SecurePass123"
        })

        response = api.login({
            "email": "login@example.com",
            "password": "SecurePass123"
        })

        assert response["success"] is True
        assert "token" in response["data"]
        assert response["data"]["user"]["email"] == "login@example.com"

    def test_api_login_invalid_credentials(self, api):
        """Invalid credentials should return error"""
        response = api.login({
            "email": "unknown@example.com",
            "password": "WrongPass123"
        })

        assert response["success"] is False
        assert response["error"]["code"] == "INVALID_CREDENTIALS"

    # --- Get User Endpoint Tests ---

    def test_api_get_user_success(self, api):
        """Getting existing user should return user data"""
        register_response = api.register({
            "email": "get@example.com",
            "name": "Get Me",
            "password": "SecurePass123"
        })
        user_id = register_response["data"]["id"]

        response = api.get_user(user_id)

        assert response["success"] is True
        assert response["data"]["name"] == "Get Me"

    def test_api_get_user_not_found(self, api):
        """Getting non-existent user should return error"""
        response = api.get_user(999)

        assert response["success"] is False
        assert response["error"]["code"] == "NOT_FOUND"

    # --- Update User Endpoint Tests ---

    def test_api_update_user_success(self, api):
        """Updating user should return updated data"""
        register_response = api.register({
            "email": "update@example.com",
            "name": "Old Name",
            "password": "SecurePass123"
        })
        user_id = register_response["data"]["id"]

        response = api.update_user(user_id, {"name": "New Name"})

        assert response["success"] is True
        assert response["data"]["name"] == "New Name"

    def test_api_update_user_not_found(self, api):
        """Updating non-existent user should return error"""
        response = api.update_user(999, {"name": "New Name"})

        assert response["success"] is False
        assert response["error"]["code"] == "NOT_FOUND"

    # --- List Users Endpoint Tests ---

    def test_api_list_users_returns_all(self, api):
        """List users should return all users"""
        api.register({"email": "a@example.com", "name": "A", "password": "SecurePass123"})
        api.register({"email": "b@example.com", "name": "B", "password": "SecurePass123"})

        response = api.list_users()

        assert response["success"] is True
        assert response["data"]["total"] == 2
        assert len(response["data"]["users"]) == 2

    def test_api_list_users_filtered(self, api):
        """List users with filter should apply filter"""
        api.register({"email": "a@example.com", "name": "A", "password": "SecurePass123"})
        api.register({"email": "b@example.com", "name": "B", "password": "SecurePass123"})
        # Deactivate first user
        api.service.deactivate_user(1)

        response = api.list_users({"active_only": True})

        assert response["data"]["total"] == 1


# =============================================================================
# Section 8: Edge Case and Integration Tests
# =============================================================================

class TestEdgeCases:
    """
    Additional tests for edge cases and integration scenarios.
    These were added after the main TDD cycles to ensure robustness.
    """

    @pytest.fixture
    def service(self):
        return UserService()

    def test_email_normalization_prevents_duplicates(self, service):
        """Email should be normalized to prevent case-based duplicates"""
        service.register_user("USER@EXAMPLE.COM", "User 1", "SecurePass123")

        with pytest.raises(DuplicateEmailError):
            service.register_user("user@example.com", "User 2", "SecurePass123")

    def test_multiple_password_changes_all_work(self, service):
        """User should be able to change password multiple times"""
        user = service.register_user("pwd@example.com", "User", "FirstPass1")

        service.change_password(user.id, "FirstPass1", "SecondPass2")
        service.change_password(user.id, "SecondPass2", "ThirdPass3")

        assert service.authenticate("pwd@example.com", "ThirdPass3") is not None
        assert service.authenticate("pwd@example.com", "SecondPass2") is None
        assert service.authenticate("pwd@example.com", "FirstPass1") is None

    def test_reactivated_user_can_login(self, service):
        """Reactivated user should be able to login"""
        user = service.register_user("reactive@example.com", "User", "SecurePass123")
        service.deactivate_user(user.id)

        # Cannot login while deactivated
        assert service.authenticate("reactive@example.com", "SecurePass123") is None

        # Can login after reactivation
        service.activate_user(user.id)
        assert service.authenticate("reactive@example.com", "SecurePass123") is not None

    def test_empty_update_preserves_values(self, service):
        """Updating with no changes should preserve existing values"""
        user = service.register_user("preserve@example.com", "Original", "SecurePass123")

        updated = service.update_user(user.id)  # No changes

        assert updated.name == "Original"
        assert updated.role == UserRole.USER


# =============================================================================
# Run tests
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
