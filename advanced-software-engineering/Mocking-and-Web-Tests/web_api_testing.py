"""
web_api_testing.py
==================
Testing Flask/FastAPI web applications.

This module demonstrates:
1. Flask test client usage
2. Testing API endpoints
3. Mocking external services in API tests
4. Request/Response testing patterns

Run tests: pytest web_api_testing.py -v
"""

import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import Optional
import json

# ============================================================
# Simple Flask Application (for demonstration)
# ============================================================

try:
    from flask import Flask, jsonify, request, abort
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not installed. Install with: pip install flask")


if FLASK_AVAILABLE:

    # --- Models ---
    @dataclass
    class User:
        id: int
        name: str
        email: str


    # --- External Services (to be mocked) ---
    class UserDatabase:
        """Simulates database operations"""
        _users = {
            1: User(1, "John Doe", "john@example.com"),
            2: User(2, "Jane Smith", "jane@example.com"),
        }

        @classmethod
        def get_user(cls, user_id: int) -> Optional[User]:
            return cls._users.get(user_id)

        @classmethod
        def create_user(cls, name: str, email: str) -> User:
            new_id = max(cls._users.keys()) + 1
            user = User(new_id, name, email)
            cls._users[new_id] = user
            return user

        @classmethod
        def get_all_users(cls):
            return list(cls._users.values())


    class EmailService:
        """External email service"""
        @staticmethod
        def send_welcome_email(email: str, name: str) -> bool:
            # In reality, calls external API
            print(f"[REAL] Sending welcome email to {email}")
            return True


    # --- Flask Application ---
    app = Flask(__name__)


    @app.route('/api/users', methods=['GET'])
    def list_users():
        """List all users"""
        users = UserDatabase.get_all_users()
        return jsonify({
            "users": [{"id": u.id, "name": u.name, "email": u.email} for u in users],
            "count": len(users)
        })


    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        """Get a specific user"""
        user = UserDatabase.get_user(user_id)
        if not user:
            abort(404, description="User not found")

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })


    @app.route('/api/users', methods=['POST'])
    def create_user():
        """Create a new user"""
        data = request.get_json()

        # Validation
        if not data:
            return jsonify({"error": "No data provided"}), 400

        if 'name' not in data or 'email' not in data:
            return jsonify({"error": "Name and email required"}), 400

        if '@' not in data['email']:
            return jsonify({"error": "Invalid email format"}), 400

        # Create user
        user = UserDatabase.create_user(data['name'], data['email'])

        # Send welcome email
        EmailService.send_welcome_email(user.email, user.name)

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "message": "User created successfully"
        }), 201


    @app.route('/api/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        """Update a user"""
        user = UserDatabase.get_user(user_id)
        if not user:
            abort(404, description="User not found")

        data = request.get_json()

        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "message": "User updated successfully"
        })


    @app.route('/api/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """Delete a user"""
        user = UserDatabase.get_user(user_id)
        if not user:
            abort(404, description="User not found")

        del UserDatabase._users[user_id]

        return jsonify({"message": f"User {user_id} deleted"}), 200


    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy"})


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": str(error.description)}), 404


# ============================================================
# TESTS - Flask Test Client
# ============================================================

@pytest.mark.skipif(not FLASK_AVAILABLE, reason="Flask not installed")
class TestFlaskAPI:
    """Testing Flask API endpoints"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture(autouse=True)
    def reset_database(self):
        """Reset database before each test"""
        UserDatabase._users = {
            1: User(1, "John Doe", "john@example.com"),
            2: User(2, "Jane Smith", "jane@example.com"),
        }

    # --- GET Tests ---

    def test_health_check(self, client):
        """Test health endpoint returns 200"""
        response = client.get('/health')

        assert response.status_code == 200
        assert response.json['status'] == 'healthy'

    def test_list_users(self, client):
        """Test listing all users"""
        response = client.get('/api/users')

        assert response.status_code == 200
        data = response.json
        assert 'users' in data
        assert data['count'] == 2

    def test_get_user_success(self, client):
        """Test getting existing user"""
        response = client.get('/api/users/1')

        assert response.status_code == 200
        data = response.json
        assert data['id'] == 1
        assert data['name'] == 'John Doe'
        assert data['email'] == 'john@example.com'

    def test_get_user_not_found(self, client):
        """Test getting non-existent user returns 404"""
        response = client.get('/api/users/999')

        assert response.status_code == 404
        assert 'error' in response.json

    # --- POST Tests ---

    def test_create_user_success(self, client):
        """Test creating a new user"""
        with patch.object(EmailService, 'send_welcome_email', return_value=True) as mock_email:
            response = client.post(
                '/api/users',
                data=json.dumps({
                    'name': 'New User',
                    'email': 'new@example.com'
                }),
                content_type='application/json'
            )

            assert response.status_code == 201
            data = response.json
            assert data['name'] == 'New User'
            assert data['email'] == 'new@example.com'
            assert 'id' in data

            # Verify email was sent
            mock_email.assert_called_once_with('new@example.com', 'New User')

    def test_create_user_missing_fields(self, client):
        """Test creating user without required fields"""
        response = client.post(
            '/api/users',
            data=json.dumps({'name': 'Only Name'}),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'error' in response.json

    def test_create_user_invalid_email(self, client):
        """Test creating user with invalid email"""
        response = client.post(
            '/api/users',
            data=json.dumps({
                'name': 'Test User',
                'email': 'invalid-email'
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        assert 'Invalid email' in response.json['error']

    def test_create_user_no_body(self, client):
        """Test creating user with no request body"""
        response = client.post('/api/users')

        assert response.status_code == 400

    # --- PUT Tests ---

    def test_update_user_success(self, client):
        """Test updating existing user"""
        response = client.put(
            '/api/users/1',
            data=json.dumps({'name': 'Updated Name'}),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.json['name'] == 'Updated Name'
        assert response.json['email'] == 'john@example.com'  # Unchanged

    def test_update_user_not_found(self, client):
        """Test updating non-existent user"""
        response = client.put(
            '/api/users/999',
            data=json.dumps({'name': 'Test'}),
            content_type='application/json'
        )

        assert response.status_code == 404

    # --- DELETE Tests ---

    def test_delete_user_success(self, client):
        """Test deleting existing user"""
        response = client.delete('/api/users/1')

        assert response.status_code == 200

        # Verify user is gone
        response = client.get('/api/users/1')
        assert response.status_code == 404

    def test_delete_user_not_found(self, client):
        """Test deleting non-existent user"""
        response = client.delete('/api/users/999')

        assert response.status_code == 404


# ============================================================
# Testing with Mocked External Services
# ============================================================

@pytest.mark.skipif(not FLASK_AVAILABLE, reason="Flask not installed")
class TestAPIWithMockedServices:
    """Testing API with mocked external dependencies"""

    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture(autouse=True)
    def reset_database(self):
        UserDatabase._users = {
            1: User(1, "John Doe", "john@example.com"),
        }

    def test_create_user_email_service_failure(self, client):
        """Test behavior when email service fails"""
        with patch.object(
            EmailService,
            'send_welcome_email',
            side_effect=Exception("SMTP Error")
        ):
            # User creation should still work even if email fails
            # (depending on your error handling strategy)
            response = client.post(
                '/api/users',
                data=json.dumps({
                    'name': 'Test User',
                    'email': 'test@example.com'
                }),
                content_type='application/json'
            )

            # This test might fail - showing that we need better error handling!
            # In real code, you'd want to catch the email exception

    def test_verify_email_called_with_correct_data(self, client):
        """Test that email service is called with correct arguments"""
        with patch.object(EmailService, 'send_welcome_email') as mock_email:
            mock_email.return_value = True

            client.post(
                '/api/users',
                data=json.dumps({
                    'name': 'Alice',
                    'email': 'alice@example.com'
                }),
                content_type='application/json'
            )

            mock_email.assert_called_once_with('alice@example.com', 'Alice')


# ============================================================
# Testing Request/Response Patterns
# ============================================================

@pytest.mark.skipif(not FLASK_AVAILABLE, reason="Flask not installed")
class TestRequestResponsePatterns:
    """Common API testing patterns"""

    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_json_content_type(self, client):
        """Test that API returns JSON"""
        response = client.get('/api/users/1')

        assert response.content_type == 'application/json'

    def test_response_structure(self, client):
        """Test response has expected structure"""
        response = client.get('/api/users/1')
        data = response.json

        # Verify all expected fields exist
        required_fields = ['id', 'name', 'email']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    def test_pagination_headers(self, client):
        """Test pagination (if implemented)"""
        # Example of testing pagination headers
        response = client.get('/api/users?page=1&limit=10')

        # In a real API, you might have:
        # assert 'X-Total-Count' in response.headers
        # assert 'X-Page' in response.headers

    def test_cors_headers(self, client):
        """Test CORS headers (if implemented)"""
        # Example of testing CORS
        response = client.options('/api/users')

        # In a real API with CORS:
        # assert 'Access-Control-Allow-Origin' in response.headers


# ============================================================
# Demonstration - Running the app
# ============================================================

if __name__ == "__main__":
    if FLASK_AVAILABLE:
        print("=" * 60)
        print("Flask Web API Testing Demo")
        print("=" * 60)
        print("\nEndpoints:")
        print("  GET    /api/users          - List all users")
        print("  GET    /api/users/<id>     - Get specific user")
        print("  POST   /api/users          - Create new user")
        print("  PUT    /api/users/<id>     - Update user")
        print("  DELETE /api/users/<id>     - Delete user")
        print("  GET    /health             - Health check")
        print("\nTo run the server:")
        print("  flask run")
        print("\nTo run tests:")
        print("  pytest web_api_testing.py -v")

        # Run tests
        pytest.main([__file__, "-v"])
    else:
        print("Flask not installed. Run: pip install flask")
