"""
test_mocking_basics.py
======================
Comprehensive mocking examples using unittest.mock and pytest.

This file demonstrates:
1. Basic mocking with Mock and MagicMock
2. Patching (decorator, context manager, manual)
3. Return values and side effects
4. Assertions on mock calls
5. Real-world test scenarios

Run: pytest test_mocking_basics.py -v
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime

from mocking_basics import (
    OrderService,
    Order,
    OrderStatus,
    PaymentGateway,
    EmailService,
    InventoryService,
    NotificationService,
)


# ============================================================
# Section 1: Basic Mock Objects
# ============================================================

class TestBasicMocking:
    """Understanding Mock and MagicMock basics"""

    def test_mock_returns_mock_for_any_attribute(self):
        """Mock objects return new mocks for any attribute access"""
        mock = Mock()

        # Any attribute access returns a Mock
        assert isinstance(mock.foo, Mock)
        assert isinstance(mock.bar.baz, Mock)
        assert isinstance(mock.anything.you.want, Mock)

    def test_mock_returns_mock_for_any_method_call(self):
        """Mock objects return mocks for any method call"""
        mock = Mock()

        # Any method call returns a Mock
        result = mock.some_method(1, 2, 3)
        assert isinstance(result, Mock)

    def test_configure_return_value(self):
        """Configure what a mock returns"""
        mock = Mock()

        # Set return value
        mock.get_user.return_value = {"id": 1, "name": "John"}

        result = mock.get_user(user_id=1)

        assert result == {"id": 1, "name": "John"}

    def test_configure_nested_return_value(self):
        """Configure nested mock return values"""
        mock = Mock()

        # Nested configuration
        mock.db.query.execute.return_value = [{"id": 1}, {"id": 2}]

        result = mock.db.query.execute()

        assert result == [{"id": 1}, {"id": 2}]

    def test_magic_mock_supports_magic_methods(self):
        """MagicMock supports __len__, __iter__, etc."""
        # Regular Mock doesn't support magic methods by default
        mock = Mock()
        # len(mock)  # Would raise TypeError!

        # MagicMock supports them
        magic = MagicMock()
        magic.__len__.return_value = 5

        assert len(magic) == 5

    def test_magic_mock_iteration(self):
        """MagicMock can be iterated"""
        mock = MagicMock()
        mock.__iter__.return_value = iter([1, 2, 3])

        result = list(mock)

        assert result == [1, 2, 3]


# ============================================================
# Section 2: Patching
# ============================================================

class TestPatching:
    """Different ways to patch objects"""

    def test_patch_as_decorator(self):
        """Using @patch decorator"""

        @patch('mocking_basics.PaymentGateway')
        def inner_test(mock_gateway_class):
            # mock_gateway_class is the mocked CLASS
            mock_instance = mock_gateway_class.return_value
            mock_instance.charge.return_value = {"status": "success"}

            gateway = PaymentGateway()
            result = gateway.charge("1234", 100)

            assert result == {"status": "success"}

        inner_test()

    def test_patch_as_context_manager(self):
        """Using patch as context manager"""
        with patch('mocking_basics.PaymentGateway') as mock_gateway_class:
            mock_instance = mock_gateway_class.return_value
            mock_instance.charge.return_value = {"status": "success"}

            gateway = PaymentGateway()
            result = gateway.charge("1234", 100)

            assert result == {"status": "success"}

    def test_patch_object(self):
        """Patching a specific method on an existing object"""
        gateway = PaymentGateway()

        with patch.object(gateway, 'charge', return_value={"status": "mocked"}):
            result = gateway.charge("1234", 100)
            assert result == {"status": "mocked"}

        # After context, original method is restored
        # result = gateway.charge("1234", 100)  # Would call real method!


# ============================================================
# Section 3: Return Values and Side Effects
# ============================================================

class TestReturnValuesAndSideEffects:
    """Controlling mock behavior"""

    def test_simple_return_value(self):
        """Return the same value every time"""
        mock = Mock()
        mock.get_price.return_value = 99.99

        assert mock.get_price() == 99.99
        assert mock.get_price() == 99.99  # Same every time

    def test_side_effect_list(self):
        """Return different values on successive calls"""
        mock = Mock()
        mock.get_next.side_effect = [1, 2, 3]

        assert mock.get_next() == 1
        assert mock.get_next() == 2
        assert mock.get_next() == 3
        # mock.get_next()  # Would raise StopIteration

    def test_side_effect_exception(self):
        """Raise an exception"""
        mock = Mock()
        mock.risky_operation.side_effect = ValueError("Something went wrong")

        with pytest.raises(ValueError, match="Something went wrong"):
            mock.risky_operation()

    def test_side_effect_function(self):
        """Use a function to compute return value"""
        mock = Mock()

        def double(x):
            return x * 2

        mock.calculate.side_effect = double

        assert mock.calculate(5) == 10
        assert mock.calculate(3) == 6

    def test_side_effect_mixed(self):
        """Mix of values and exceptions"""
        mock = Mock()
        mock.api_call.side_effect = [
            {"status": "success"},
            TimeoutError("Network timeout"),
            {"status": "success"},
        ]

        # First call succeeds
        assert mock.api_call()["status"] == "success"

        # Second call fails
        with pytest.raises(TimeoutError):
            mock.api_call()

        # Third call succeeds
        assert mock.api_call()["status"] == "success"


# ============================================================
# Section 4: Assertions on Mocks
# ============================================================

class TestMockAssertions:
    """Verifying how mocks were called"""

    def test_assert_called(self):
        """Check if method was called at all"""
        mock = Mock()

        mock.save()

        mock.save.assert_called()

    def test_assert_called_once(self):
        """Check if method was called exactly once"""
        mock = Mock()

        mock.save()

        mock.save.assert_called_once()

        mock.save()
        # mock.save.assert_called_once()  # Would fail! Called twice

    def test_assert_called_with(self):
        """Check the arguments passed"""
        mock = Mock()

        mock.create_user(name="John", email="john@example.com")

        mock.create_user.assert_called_with(name="John", email="john@example.com")

    def test_assert_called_once_with(self):
        """Check called exactly once with specific args"""
        mock = Mock()

        mock.send_email("user@example.com", "Hello!")

        mock.send_email.assert_called_once_with("user@example.com", "Hello!")

    def test_call_count(self):
        """Check number of calls"""
        mock = Mock()

        mock.log("message 1")
        mock.log("message 2")
        mock.log("message 3")

        assert mock.log.call_count == 3

    def test_call_args(self):
        """Access the arguments of the last call"""
        mock = Mock()

        mock.process(1, 2, key="value")

        # call_args is a tuple of (args, kwargs)
        assert mock.process.call_args[0] == (1, 2)
        assert mock.process.call_args[1] == {"key": "value"}

        # Or use call_args.args and call_args.kwargs
        assert mock.process.call_args.args == (1, 2)
        assert mock.process.call_args.kwargs == {"key": "value"}

    def test_call_args_list(self):
        """Access all calls made"""
        mock = Mock()

        mock.log("first")
        mock.log("second")
        mock.log("third")

        assert mock.log.call_args_list == [
            call("first"),
            call("second"),
            call("third"),
        ]

    def test_assert_any_call(self):
        """Check if a specific call was made (among many)"""
        mock = Mock()

        mock.process("a")
        mock.process("b")
        mock.process("c")

        mock.process.assert_any_call("b")

    def test_assert_not_called(self):
        """Check method was never called"""
        mock = Mock()

        # Don't call it

        mock.dangerous_operation.assert_not_called()


# ============================================================
# Section 5: Real-World Order Service Tests
# ============================================================

class TestOrderServiceWithMocks:
    """Testing OrderService with all dependencies mocked"""

    @pytest.fixture
    def mock_dependencies(self):
        """Create mock instances of all dependencies"""
        return {
            "payment": Mock(spec=PaymentGateway),
            "email": Mock(spec=EmailService),
            "inventory": Mock(spec=InventoryService),
            "notification": Mock(spec=NotificationService),
        }

    @pytest.fixture
    def order_service(self, mock_dependencies):
        """Create OrderService with mocked dependencies"""
        return OrderService(
            payment_gateway=mock_dependencies["payment"],
            email_service=mock_dependencies["email"],
            inventory_service=mock_dependencies["inventory"],
            notification_service=mock_dependencies["notification"],
        )

    @pytest.fixture
    def sample_order(self):
        """Create a sample order for testing"""
        return Order(
            id="ORD-001",
            user_email="user@example.com",
            user_phone="9876543210",
            product_id="PROD-123",
            quantity=2,
            amount=999.00
        )

    # --- Happy Path Tests ---

    def test_place_order_success(self, order_service, mock_dependencies, sample_order):
        """Test successful order placement"""
        # Arrange - configure mocks
        mock_dependencies["inventory"].check_stock.return_value = 100
        mock_dependencies["inventory"].reserve_stock.return_value = True
        mock_dependencies["payment"].charge.return_value = {
            "status": "success",
            "transaction_id": "txn_123"
        }
        mock_dependencies["email"].send_email.return_value = True
        mock_dependencies["notification"].send_sms.return_value = True

        # Act
        result = order_service.place_order(sample_order)

        # Assert - verify result
        assert result.status == OrderStatus.CONFIRMED
        assert result.transaction_id == "txn_123"

        # Assert - verify interactions
        mock_dependencies["inventory"].check_stock.assert_called_once_with("PROD-123")
        mock_dependencies["inventory"].reserve_stock.assert_called_once_with("PROD-123", 2)
        mock_dependencies["payment"].charge.assert_called_once()
        mock_dependencies["email"].send_email.assert_called_once()
        mock_dependencies["notification"].send_sms.assert_called_once()

    def test_place_order_sends_correct_email(self, order_service, mock_dependencies, sample_order):
        """Test that correct email is sent"""
        # Arrange
        mock_dependencies["inventory"].check_stock.return_value = 100
        mock_dependencies["inventory"].reserve_stock.return_value = True
        mock_dependencies["payment"].charge.return_value = {
            "status": "success",
            "transaction_id": "txn_123"
        }

        # Act
        order_service.place_order(sample_order)

        # Assert - verify email content
        mock_dependencies["email"].send_email.assert_called_once_with(
            to="user@example.com",
            subject="Order ORD-001 Confirmed!",
            body="Your order for 2 items is confirmed."
        )

    # --- Failure Scenario Tests ---

    def test_place_order_insufficient_stock(self, order_service, mock_dependencies, sample_order):
        """Test order fails when stock is insufficient"""
        # Arrange - not enough stock
        mock_dependencies["inventory"].check_stock.return_value = 1  # Only 1 available

        # Act & Assert
        with pytest.raises(ValueError, match="Insufficient stock"):
            order_service.place_order(sample_order)

        # Verify no payment was attempted
        mock_dependencies["payment"].charge.assert_not_called()

    def test_place_order_payment_failure(self, order_service, mock_dependencies, sample_order):
        """Test order fails when payment fails"""
        # Arrange
        mock_dependencies["inventory"].check_stock.return_value = 100
        mock_dependencies["inventory"].reserve_stock.return_value = True
        mock_dependencies["payment"].charge.return_value = {
            "status": "failed",
            "error": "Card declined"
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Payment failed"):
            order_service.place_order(sample_order)

        # Verify stock was released (rollback)
        mock_dependencies["inventory"].release_stock.assert_called_once_with("PROD-123", 2)

    def test_place_order_payment_timeout(self, order_service, mock_dependencies, sample_order):
        """Test order handles payment gateway timeout"""
        # Arrange
        mock_dependencies["inventory"].check_stock.return_value = 100
        mock_dependencies["inventory"].reserve_stock.return_value = True
        mock_dependencies["payment"].charge.side_effect = TimeoutError("Gateway timeout")

        # Act & Assert
        with pytest.raises(TimeoutError):
            order_service.place_order(sample_order)

        # Verify stock was released
        mock_dependencies["inventory"].release_stock.assert_called_once()

    # --- Refund Tests ---

    def test_refund_order_success(self, order_service, mock_dependencies):
        """Test successful refund"""
        # Arrange - confirmed order
        order = Order(
            id="ORD-001",
            user_email="user@example.com",
            user_phone="9876543210",
            product_id="PROD-123",
            quantity=2,
            amount=999.00,
            status=OrderStatus.CONFIRMED,
            transaction_id="txn_123"
        )

        mock_dependencies["payment"].refund.return_value = {
            "status": "refunded",
            "refund_id": "ref_456"
        }

        # Act
        result = order_service.refund_order(order)

        # Assert
        assert result.status == OrderStatus.REFUNDED
        mock_dependencies["payment"].refund.assert_called_once_with("txn_123", 999.00)
        mock_dependencies["inventory"].release_stock.assert_called_once()
        mock_dependencies["email"].send_email.assert_called_once()

    def test_refund_pending_order_fails(self, order_service, mock_dependencies):
        """Test can't refund pending order"""
        order = Order(
            id="ORD-001",
            user_email="user@example.com",
            user_phone="9876543210",
            product_id="PROD-123",
            quantity=2,
            amount=999.00,
            status=OrderStatus.PENDING  # Not confirmed
        )

        with pytest.raises(ValueError, match="Cannot refund"):
            order_service.refund_order(order)


# ============================================================
# Section 6: Testing with spec and autospec
# ============================================================

class TestSpecAndAutospec:
    """Using spec to catch API mismatches"""

    def test_mock_without_spec_allows_typos(self):
        """Without spec, typos go unnoticed"""
        mock = Mock()

        # Typo! But mock doesn't care
        mock.chearge(100)  # Should be 'charge'

        mock.chearge.assert_called()  # Passes, but bug in test!

    def test_mock_with_spec_catches_typos(self):
        """With spec, invalid attributes raise errors"""
        mock = Mock(spec=PaymentGateway)

        # mock.chearge(100)  # Would raise AttributeError!

        mock.charge(card_number="1234", amount=100)  # Works

    def test_autospec_validates_signatures(self):
        """autospec validates method signatures too"""
        with patch('mocking_basics.PaymentGateway', autospec=True) as mock_class:
            mock_instance = mock_class.return_value

            # This would fail because signature doesn't match:
            # mock_instance.charge(100)  # Missing required args!

            # This works:
            mock_instance.charge(
                card_number="1234",
                amount=100,
                currency="INR"
            )


# ============================================================
# Section 7: Patching Best Practices
# ============================================================

class TestPatchingBestPractices:
    """Where and how to patch correctly"""

    def test_patch_where_used_not_where_defined(self):
        """
        KEY PRINCIPLE: Patch where the object is USED, not where it's DEFINED.

        If module_a imports SomeClass from module_b,
        and you're testing module_a,
        patch 'module_a.SomeClass', not 'module_b.SomeClass'
        """
        # mocking_basics imports PaymentGateway
        # So we patch 'mocking_basics.PaymentGateway'

        with patch('mocking_basics.PaymentGateway') as mock:
            mock.return_value.charge.return_value = {"status": "success"}

            # Now when mocking_basics creates PaymentGateway(), it gets our mock
            from mocking_basics import PaymentGateway as PG
            gateway = PG()
            result = gateway.charge("1234", 100)

            assert result == {"status": "success"}


# ============================================================
# Run tests
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
