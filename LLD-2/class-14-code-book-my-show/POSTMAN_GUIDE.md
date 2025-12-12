# Postman Setup Guide for BookMyShow API

## 📦 Files Created

1. **BookMyShow_API_Collection.postman_collection.json** - Complete API collection
2. **BookMyShow_Local.postman_environment.json** - Local environment variables

## 🚀 How to Import in Postman

### Step 1: Import Collection

1. Open Postman
2. Click **Import** button (top left)
3. Drag and drop `BookMyShow_API_Collection.postman_collection.json`
   - OR click "Upload Files" and select the file
4. Click **Import**

You should see a new collection called **"BookMyShow API"** in your Collections tab.

### Step 2: Import Environment

1. Click the **Environments** icon (left sidebar, looks like a gear)
2. Click **Import**
3. Select `BookMyShow_Local.postman_environment.json`
4. Click **Import**

### Step 3: Select Environment

1. In the top-right corner, select **"BookMyShow - Local"** from the environment dropdown
2. This sets `base_url` to `http://localhost:8000/api`

## 📋 Collection Structure

```
BookMyShow API
├── Authentication
│   ├── Register User
│   └── Login (auto-saves token)
├── Cities
│   ├── List Cities
│   └── Get City Details
├── Theaters
│   ├── List Theaters
│   ├── List Theaters by City
│   ├── Search Theaters
│   └── Get Theater Details
├── Movies
│   ├── List Movies
│   ├── Search Movies (advanced filters)
│   ├── Get Movie Details
│   └── Get Movie Shows
├── Shows
│   ├── List Shows
│   ├── Filter Shows by Movie
│   ├── Filter Shows by Theater
│   ├── Get Show Details with Seats
│   └── Get Available Seats
├── Booking
│   ├── Book Tickets (requires auth)
│   ├── Confirm Payment (requires auth)
│   └── Validate Coupon (requires auth)
├── Tickets
│   ├── My Tickets (requires auth)
│   ├── Get Ticket Details (requires auth)
│   └── Cancel Ticket (requires auth)
└── Health Check
```

## 🔐 Authentication Flow

### Method 1: Using Login (Recommended)

1. **Register a user** (one time):
   - Open `Authentication → Register User`
   - Click **Send**
   - Creates user: `john_doe`

2. **Login**:
   - Open `Authentication → Login`
   - Click **Send**
   - The auth token is **automatically saved** to `{{auth_token}}` variable

3. **Use authenticated endpoints**:
   - All endpoints under Booking and Tickets use the token automatically
   - They have `Authorization: Bearer {{auth_token}}` header

### Method 2: Using Admin User

If you created a superuser via `python manage.py createsuperuser`:

1. Update the Login request body with your admin credentials:
   ```json
   {
       "username": "admin",
       "password": "your_admin_password"
   }
   ```
2. Send the request
3. Token is auto-saved

## 🎯 Testing the APIs

### Quick Start Flow

1. **Check Health**
   ```
   GET Health Check
   ```
   Should return: `{"status": "ok", "service": "bookmyshow"}`

2. **Browse Cities**
   ```
   GET Cities → List Cities
   ```

3. **Search Movies**
   ```
   GET Movies → Search Movies
   ```
   Edit query params: city, query, category, etc.

4. **View Show Details**
   ```
   GET Shows → Get Show Details with Seats
   ```
   Change `show-1` to actual show ID from previous response

5. **Book Tickets** (requires authentication)
   - First: Login (saves token)
   - Then: `POST Booking → Book Tickets`
   - Update `seat_ids` with actual IDs from show details

### Complete Booking Flow

```
1. Login → saves token
2. GET /movies/search/?city=mumbai
3. GET /movies/{id}/shows/
4. GET /shows/{show_id}/ → see available seats
5. POST /book/ → book selected seats
6. POST /tickets/{ticket_id}/confirm-payment/
7. GET /tickets/ → see your bookings
```

## 🔧 Environment Variables

The collection uses these variables:

| Variable | Value | Usage |
|----------|-------|-------|
| `base_url` | `http://localhost:8000/api` | API base URL |
| `auth_token` | Auto-set by Login | Authentication |
| `username` | `admin` | Default username |
| `password` | `admin123` | Default password |

### Changing Variables

1. Click environment dropdown (top right)
2. Click the eye icon
3. Edit values
4. Save

## 📝 Sample Requests

### Book Tickets

```json
POST {{base_url}}/book/
Authorization: Bearer {{auth_token}}

{
    "show_id": "show-1",
    "seat_ids": [
        "show-1-pvr-mumbai-1-screen-1-A1",
        "show-1-pvr-mumbai-1-screen-1-A2"
    ],
    "payment_mode": "UPI",
    "coupon_code": ""
}
```

### Search Movies

```
GET {{base_url}}/movies/search/?query=avengers&city=mumbai&min_rating=7
```

## 🧪 Testing Concurrency

To test concurrency control (the main feature!):

1. **Open the same request in 2 tabs**:
   - Right-click `Booking → Book Tickets`
   - Select "Duplicate"

2. **Use same seat IDs in both**:
   ```json
   {
       "show_id": "show-1",
       "seat_ids": ["show-1-pvr-mumbai-1-screen-1-A1"]
   }
   ```

3. **Send both quickly** (within 1 second)

4. **Result**:
   - One succeeds (201 Created)
   - One fails (400 Bad Request - "Seats not available")
   - This proves concurrency control works! 🎉

## 🐛 Troubleshooting

### Error: "Could not send request"
- **Solution**: Make sure Django server is running:
  ```bash
  python manage.py runserver
  ```

### Error: "401 Unauthorized"
- **Solution**: Login first to get auth token
  1. Run `Authentication → Login`
  2. Token is auto-saved to `{{auth_token}}`

### Error: "no such table"
- **Solution**: Run migrations:
  ```bash
  python manage.py migrate
  python manage.py seed_data
  ```

### Seat IDs don't match
- **Solution**: Get actual seat IDs from:
  ```
  GET /shows/{show-id}/
  ```
  Look in `show_seats` array for `id` field

### Variables not working
- **Solution**:
  1. Check environment is selected (top right)
  2. Click eye icon to verify variable values
  3. Re-import environment if needed

## 💡 Tips

1. **Save responses**: Click "Save Response" to keep examples

2. **Use Tests tab**: Auto-extract values
   - Login request already has a test that saves token
   - Check "Tests" tab in Login request

3. **Use Pre-request Script**: Set dynamic values
   ```javascript
   pm.variables.set("current_date", new Date().toISOString().split('T')[0]);
   ```

4. **Organize**: Create folders for different test scenarios

5. **Export**: Share collection with team
   - Right-click collection → Export
   - Share the JSON file

## 🎓 Interview Practice

Use this collection to:

1. **Understand API flow**: Follow the complete booking journey
2. **Test concurrency**: Duplicate requests, send simultaneously
3. **Explain in interviews**: Show you've tested the system
4. **Demo to interviewer**: Live API demonstration

## 📚 Related Files

- `guides/05_API_DOCUMENTATION.md` - Detailed API documentation
- `README.md` - Project setup and overview
- `SETUP_GUIDE.md` - Installation instructions

---

Happy testing! 🚀

For questions or issues, refer to the guides in `bookmyshow/guides/`.
