# Role-Based Access Control (RBAC)

> *"Authentication tells you WHO someone is. Authorization tells you WHAT they can do. RBAC is HOW you manage what they can do at scale."*

---

## What is RBAC?

**Role-Based Access Control (RBAC)** is an approach to restricting system access based on the roles of individual users. Instead of assigning permissions directly to users, permissions are assigned to roles, and users are assigned to roles.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE RBAC MODEL                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Without RBAC (Direct Permissions):                            │
│   ┌──────┐                                                      │
│   │ User │──────────────────────────┬─► Permission 1            │
│   └──────┘                          ├─► Permission 2            │
│   ┌──────┐                          ├─► Permission 3            │
│   │ User │──────────────────────────┼─► Permission 4            │
│   └──────┘                          └─► Permission 5            │
│   (Nightmare to manage at scale!)                               │
│                                                                  │
│   With RBAC (Role-Based):                                       │
│   ┌──────┐      ┌──────┐      ┌─────────────┐                   │
│   │ User │─────►│ Role │─────►│ Permissions │                   │
│   └──────┘      └──────┘      └─────────────┘                   │
│   ┌──────┐          │                                           │
│   │ User │──────────┘                                           │
│   └──────┘                                                      │
│   (Clean, scalable, auditable!)                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## The ELI5 Version

### Think of a Company

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPANY ANALOGY                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ROLES (Job Titles):                                           │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│   │   CEO      │  │  Manager   │  │  Employee  │               │
│   └────────────┘  └────────────┘  └────────────┘               │
│                                                                  │
│   PERMISSIONS (What each role can do):                          │
│                                                                  │
│   CEO:      ✓ View all data    ✓ Fire anyone    ✓ Set budgets  │
│   Manager:  ✓ View team data   ✓ Approve leave  ✗ Fire anyone  │
│   Employee: ✓ View own data    ✗ Approve leave  ✗ Fire anyone  │
│                                                                  │
│   When Alice joins as a Manager:                                │
│   - We don't set 50 individual permissions                      │
│   - We just assign her the "Manager" role                       │
│   - She instantly gets all Manager permissions!                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core RBAC Components

### 1. Users
The individuals who need access to the system.

### 2. Roles
Named collections of permissions (e.g., "Admin", "Editor", "Viewer").

### 3. Permissions
Specific actions that can be performed (e.g., "read:posts", "write:posts", "delete:users").

### 4. Role Assignment
Mapping between users and roles.

### 5. Permission Assignment
Mapping between roles and permissions.

```
┌─────────────────────────────────────────────────────────────────┐
│                    RBAC COMPONENTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  USERS              ROLES              PERMISSIONS               │
│  ┌─────────┐        ┌─────────┐        ┌──────────────────┐     │
│  │  Alice  │───────►│  Admin  │───────►│ users:create     │     │
│  └─────────┘        └─────────┘    ┌──►│ users:read       │     │
│                          │         │   │ users:update     │     │
│  ┌─────────┐             │         │   │ users:delete     │     │
│  │   Bob   │─────────────┘         │   │ posts:create     │     │
│  └─────────┘                       │   │ posts:read       │     │
│       │             ┌─────────┐    │   │ posts:update     │     │
│       └────────────►│  Editor │────┘   │ posts:delete     │     │
│                     └─────────┘        └──────────────────┘     │
│  ┌─────────┐             │                                      │
│  │ Charlie │─────────────┘                                      │
│  └─────────┘                                                    │
│       │             ┌─────────┐        ┌──────────────────┐     │
│       └────────────►│  Viewer │───────►│ posts:read       │     │
│                     └─────────┘        └──────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## RBAC vs Other Access Control Models

### Comparison Table

| Aspect | DAC | MAC | RBAC | ABAC |
|--------|-----|-----|------|------|
| **Full Name** | Discretionary Access Control | Mandatory Access Control | Role-Based Access Control | Attribute-Based Access Control |
| **Who decides?** | Resource owner | System/Policy | Administrator | Policy engine |
| **Based on** | Owner's discretion | Security labels | User's role | Multiple attributes |
| **Flexibility** | High | Low | Medium | Very High |
| **Complexity** | Low | High | Medium | High |
| **Best for** | Small systems | Military/Government | Enterprises | Complex policies |
| **Example** | Unix file permissions | Top Secret clearance | Admin/User roles | Time + Location + Role |

### Visual Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACCESS CONTROL MODELS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DAC (Discretionary):                                           │
│  "I own this file, I decide who can access it"                  │
│  ┌──────┐     ┌──────┐                                          │
│  │ Owner│────►│ File │ "I give Bob read access"                 │
│  └──────┘     └──────┘                                          │
│                                                                  │
│  MAC (Mandatory):                                               │
│  "System labels determine access, no exceptions"                │
│  ┌────────────┐                                                 │
│  │ TOP SECRET │ ─► Only users with TOP SECRET clearance         │
│  └────────────┘                                                 │
│                                                                  │
│  RBAC (Role-Based):                                             │
│  "Your job title determines your access"                        │
│  ┌──────────┐     ┌─────────────┐                               │
│  │ Manager  │────►│ Can approve │                               │
│  └──────────┘     │ expenses    │                               │
│                   └─────────────┘                               │
│                                                                  │
│  ABAC (Attribute-Based):                                        │
│  "Multiple factors determine access"                            │
│  ┌─────────────────────────────────────────┐                    │
│  │ IF role=Manager AND time=9am-5pm        │                    │
│  │ AND location=office AND department=HR   │ ─► ALLOW           │
│  └─────────────────────────────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## RBAC Levels (NIST Standard)

The NIST (National Institute of Standards and Technology) defines four levels of RBAC:

### Level 1: Flat RBAC
- Basic user-role assignment
- Basic role-permission assignment
- Users can have multiple roles

### Level 2: Hierarchical RBAC
- Roles can inherit from other roles
- Senior roles inherit junior role permissions

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROLE HIERARCHY                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌───────────────┐                            │
│                    │  Super Admin  │                            │
│                    └───────┬───────┘                            │
│                            │ inherits                           │
│                    ┌───────▼───────┐                            │
│                    │     Admin     │                            │
│                    └───────┬───────┘                            │
│              ┌─────────────┼─────────────┐                      │
│              │ inherits    │ inherits    │ inherits             │
│       ┌──────▼──────┐ ┌────▼────┐ ┌──────▼──────┐              │
│       │   Editor    │ │ Moderator│ │   Analyst  │              │
│       └──────┬──────┘ └────┬────┘ └──────┬──────┘              │
│              │             │             │                      │
│              └─────────────┼─────────────┘                      │
│                     ┌──────▼──────┐                             │
│                     │    Viewer   │ (Base role)                 │
│                     └─────────────┘                             │
│                                                                  │
│  Super Admin has ALL permissions (inherited down the chain)     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Level 3: Constrained RBAC
- Separation of Duties (SoD)
- Mutually exclusive roles (can't be both Approver AND Requester)

### Level 4: Symmetric RBAC
- Permission-role review
- Role-role review
- Full administrative capabilities

---

## Real-World RBAC Examples

### 1. AWS IAM (Identity and Access Management)

```python
# AWS IAM Policy Example (JSON)
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::my-bucket/*"
        }
    ]
}

# Users are assigned to Groups (Roles)
# Groups have Policies (Permissions) attached
```

### 2. GitHub Repository Roles

| Role | Permissions |
|------|------------|
| **Read** | Clone, pull, view issues |
| **Triage** | + Manage issues and PRs |
| **Write** | + Push to branches |
| **Maintain** | + Manage settings (not sensitive) |
| **Admin** | + Full access including dangerous actions |

### 3. Database Roles (PostgreSQL)

```sql
-- Create roles
CREATE ROLE readonly;
CREATE ROLE readwrite;
CREATE ROLE admin;

-- Grant permissions to roles
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO readwrite;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;

-- Assign users to roles
GRANT readonly TO analyst_user;
GRANT readwrite TO app_user;
GRANT admin TO dba_user;
```

---

## Python RBAC Implementation

### Simple RBAC System

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Set, Dict, Optional

class Permission(Enum):
    # User permissions
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"

    # Post permissions
    POST_CREATE = "post:create"
    POST_READ = "post:read"
    POST_UPDATE = "post:update"
    POST_DELETE = "post:delete"

    # Admin permissions
    ADMIN_PANEL = "admin:panel"
    SYSTEM_CONFIG = "system:config"


@dataclass
class Role:
    name: str
    permissions: Set[Permission] = field(default_factory=set)
    parent: Optional['Role'] = None  # For hierarchical RBAC

    def get_all_permissions(self) -> Set[Permission]:
        """Get permissions including inherited ones."""
        perms = self.permissions.copy()
        if self.parent:
            perms.update(self.parent.get_all_permissions())
        return perms


@dataclass
class User:
    id: str
    username: str
    roles: Set[Role] = field(default_factory=set)

    def has_permission(self, permission: Permission) -> bool:
        """Check if user has a specific permission."""
        for role in self.roles:
            if permission in role.get_all_permissions():
                return True
        return False

    def has_any_permission(self, permissions: Set[Permission]) -> bool:
        """Check if user has any of the given permissions."""
        return any(self.has_permission(p) for p in permissions)

    def has_all_permissions(self, permissions: Set[Permission]) -> bool:
        """Check if user has all of the given permissions."""
        return all(self.has_permission(p) for p in permissions)


class RBACManager:
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}

    def create_role(self, name: str, permissions: Set[Permission],
                    parent: Optional[str] = None) -> Role:
        """Create a new role with permissions."""
        parent_role = self.roles.get(parent) if parent else None
        role = Role(name=name, permissions=permissions, parent=parent_role)
        self.roles[name] = role
        return role

    def assign_role(self, user: User, role_name: str) -> bool:
        """Assign a role to a user."""
        if role_name not in self.roles:
            return False
        user.roles.add(self.roles[role_name])
        return True

    def revoke_role(self, user: User, role_name: str) -> bool:
        """Revoke a role from a user."""
        if role_name not in self.roles:
            return False
        user.roles.discard(self.roles[role_name])
        return True

    def check_access(self, user: User, permission: Permission) -> bool:
        """Check if a user has access to perform an action."""
        return user.has_permission(permission)


# Example Usage
if __name__ == "__main__":
    # Initialize RBAC Manager
    rbac = RBACManager()

    # Create role hierarchy
    viewer_role = rbac.create_role(
        "viewer",
        {Permission.POST_READ, Permission.USER_READ}
    )

    editor_role = rbac.create_role(
        "editor",
        {Permission.POST_CREATE, Permission.POST_UPDATE},
        parent="viewer"  # Inherits viewer permissions
    )

    admin_role = rbac.create_role(
        "admin",
        {Permission.USER_CREATE, Permission.USER_DELETE,
         Permission.POST_DELETE, Permission.ADMIN_PANEL},
        parent="editor"  # Inherits editor (and viewer) permissions
    )

    # Create users
    alice = User(id="1", username="alice")
    bob = User(id="2", username="bob")
    charlie = User(id="3", username="charlie")

    # Assign roles
    rbac.assign_role(alice, "admin")
    rbac.assign_role(bob, "editor")
    rbac.assign_role(charlie, "viewer")

    # Check permissions
    print(f"Alice can delete users: {alice.has_permission(Permission.USER_DELETE)}")  # True
    print(f"Alice can read posts: {alice.has_permission(Permission.POST_READ)}")      # True (inherited)
    print(f"Bob can create posts: {bob.has_permission(Permission.POST_CREATE)}")      # True
    print(f"Bob can delete users: {bob.has_permission(Permission.USER_DELETE)}")      # False
    print(f"Charlie can read posts: {charlie.has_permission(Permission.POST_READ)}")  # True
    print(f"Charlie can create posts: {charlie.has_permission(Permission.POST_CREATE)}")  # False
```

### Flask Decorator for RBAC

```python
from functools import wraps
from flask import g, abort, request
import jwt

def require_permission(permission: Permission):
    """Decorator to check if current user has required permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get current user from request context
            user = get_current_user()

            if not user:
                abort(401, description="Authentication required")

            if not user.has_permission(permission):
                abort(403, description=f"Permission denied: {permission.value}")

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_role(role_name: str):
    """Decorator to check if current user has required role."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()

            if not user:
                abort(401, description="Authentication required")

            if not any(r.name == role_name for r in user.roles):
                abort(403, description=f"Role required: {role_name}")

            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Usage in Flask routes
@app.route('/admin/users', methods=['DELETE'])
@require_permission(Permission.USER_DELETE)
def delete_user():
    # Only users with USER_DELETE permission can access this
    return {"status": "user deleted"}


@app.route('/admin/dashboard')
@require_role("admin")
def admin_dashboard():
    # Only admins can access this
    return {"status": "admin dashboard"}
```

---

## Database Schema for RBAC

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    parent_role_id INTEGER REFERENCES roles(id),  -- For hierarchy
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Permissions table
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,  -- e.g., "user:create"
    description TEXT,
    resource VARCHAR(50),  -- e.g., "user"
    action VARCHAR(50)     -- e.g., "create"
);

-- Role-Permission mapping (many-to-many)
CREATE TABLE role_permissions (
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    permission_id INTEGER REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

-- User-Role mapping (many-to-many)
CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER REFERENCES users(id),
    PRIMARY KEY (user_id, role_id)
);

-- Example: Check if user has permission (with hierarchy)
WITH RECURSIVE role_hierarchy AS (
    -- Base: user's direct roles
    SELECT r.id, r.parent_role_id
    FROM roles r
    JOIN user_roles ur ON r.id = ur.role_id
    WHERE ur.user_id = $1  -- user_id parameter

    UNION

    -- Recursive: parent roles
    SELECT r.id, r.parent_role_id
    FROM roles r
    JOIN role_hierarchy rh ON r.id = rh.parent_role_id
)
SELECT EXISTS (
    SELECT 1
    FROM role_hierarchy rh
    JOIN role_permissions rp ON rh.id = rp.role_id
    JOIN permissions p ON rp.permission_id = p.id
    WHERE p.name = $2  -- permission name parameter
) AS has_permission;
```

---

## Best Practices

### 1. Principle of Least Privilege
```
┌─────────────────────────────────────────────────────────────────┐
│   ✅ DO: Give minimum permissions needed                        │
│   ❌ DON'T: Give admin access "just in case"                    │
│                                                                  │
│   User needs to view reports?                                   │
│   ✅ Assign "report_viewer" role                                │
│   ❌ Assign "admin" role                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Role Naming Conventions
```python
# ✅ Good: Clear, descriptive names
roles = ["billing_admin", "content_editor", "support_agent"]

# ❌ Bad: Vague, generic names
roles = ["role1", "user_type_a", "special"]
```

### 3. Separation of Duties
```
┌─────────────────────────────────────────────────────────────────┐
│   MUTUALLY EXCLUSIVE ROLES                                       │
│                                                                  │
│   Payment System:                                               │
│   - payment_requester: Can request payments                     │
│   - payment_approver: Can approve payments                      │
│                                                                  │
│   ⚠️  Same person CANNOT have both roles!                       │
│   (Prevents fraud: can't request AND approve own payments)      │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Regular Audits
```python
def audit_user_permissions(user_id: str) -> dict:
    """Generate audit report for user permissions."""
    user = get_user(user_id)
    return {
        "user_id": user.id,
        "username": user.username,
        "roles": [r.name for r in user.roles],
        "all_permissions": [p.value for p in user.get_all_permissions()],
        "last_login": user.last_login,
        "role_assignments": [
            {"role": r.name, "assigned_at": r.assigned_at}
            for r in user.role_history
        ]
    }
```

### 5. Default Deny
```python
def check_access(user: User, permission: Permission) -> bool:
    """
    Default DENY policy.
    Access is only granted if explicitly permitted.
    """
    if not user:
        return False  # No user = no access

    if not user.roles:
        return False  # No roles = no access

    # Must explicitly have permission
    return user.has_permission(permission)
```

---

## Common Pitfalls

### 1. Role Explosion
```
❌ PROBLEM: Too many granular roles
   - viewer_posts_only
   - viewer_posts_and_comments
   - viewer_posts_comments_profiles
   - editor_posts_only
   - editor_posts_and_comments
   ... (100 more roles)

✅ SOLUTION: Use permission composition
   - viewer (base)
   - editor (base + edit)
   - Combine with resource-specific permissions
```

### 2. Hardcoded Role Checks
```python
# ❌ BAD: Checking role names directly
if user.role == "admin":
    allow_delete()

# ✅ GOOD: Checking permissions
if user.has_permission(Permission.USER_DELETE):
    allow_delete()
```

### 3. Missing Inheritance Checks
```python
# ❌ BAD: Only checking direct permissions
def has_permission(user, permission):
    return permission in user.role.permissions

# ✅ GOOD: Checking inherited permissions too
def has_permission(user, permission):
    return permission in user.role.get_all_permissions()
```

---

## Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    RBAC KEY POINTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. Users → Roles → Permissions (indirect assignment)          │
│                                                                  │
│   2. Benefits:                                                  │
│      • Simplified administration                                │
│      • Better security (least privilege)                        │
│      • Easy auditing and compliance                             │
│      • Scalable for large organizations                         │
│                                                                  │
│   3. Implementation Steps:                                      │
│      • Define permissions (resource:action)                     │
│      • Create roles with permission sets                        │
│      • Assign users to roles                                    │
│      • Check permissions in code                                │
│                                                                  │
│   4. Best Practices:                                            │
│      • Principle of least privilege                             │
│      • Separation of duties                                     │
│      • Regular audits                                           │
│      • Default deny policy                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Next**: Return to [README.md](./README.md) for the complete learning path.
