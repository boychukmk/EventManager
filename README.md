# Django Rest Event Manager 
```
✅ CRUD with UI
✅ CRUD via API with access tokens
✅ User Registration and Authentication.
✅ Event Registration with email notifications
✅ Event Search by location, name or description
```

---

## Installation with Docker 
1. Clone repo 
```bash
git clone https://github.com/boychukmk/EventManager.git
cd EventManager
```
2. (Optional)     
    If you want to use mail sending feature create .env file with variables. Don`t forget to allow IMAP connections!
 ```angular2html
EMAIL_HOST_USER=your@ukr.net
EMAIL_HOST_PASSWORD=password
```
3. Build and Start Container 
```bash
docker build -t event-manager .
docker run -p 8000:8000 --name event-manager event-manager
 ```
4. Set up database
```bash
docker exec -it event-manager python manage.py makemigrations
docker exec -it event-manager python manage.py migrate
```
5. Create superuser 

```bash
docker exec -it event-manager python manage.py createsuperuser
```
```
 username = root 
 password = root
```
6. Load fixtures 
```bash
docker exec -it event-manager python manage.py loaddata fixtures/events.json
 ```
7. Go to [http://localhost:8000](http://localhost:8000).

---
## How to use?

You can use app as regular web app, or via API

### API guide

- Obtain a token with superuser credentials:
  ```
  POST /api-token-auth/
  ```
  ```json
  {
    "username": "root",
    "password": "root"
  }
  ```

- Example CURL:
  ```bash
  curl -X POST http://localhost:8000/api-token-auth/ -H "Content-Type: application/json" -d '{"username": "root", "password": "root"}'
  ```

---

### Events Management

#### 1. List all events
- Retrieve a list of all events.
  ```
  GET /api/events
  ```

- Example CURL:
  ```bash
  curl -X GET http://localhost:8000/api/events
  ```

---

#### 2. View a specific event
- Get detailed information about a particular event by its ID.
  ```
  GET /api/events/<event_id>/
  ```

- Example CURL:
  ```bash
  curl -X GET http://localhost:8000/api/events/1/
  ```

---

#### 3. Create a new event
- Requires authentication. Token should be provided in the header.
  ```
  POST /api/events/create/
  ```
  Request Body:
  ```json
  {
    "title": "New Event",
    "description": "Event Description",
    "date": "2024-10-25",
    "location": "Conference Hall A"
  }
  ```

- Example CURL:
  ```bash
  curl -X POST http://localhost:8000/api/events/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token Your_Token" \
  -d '{
    "title": "New Event",
    "description": "Event Description",
    "date": "2024-10-25",
    "location": "Conference Hall A"
  }'
  ```

---

#### 4. Update an existing event
- Requires authentication. Token should be provided in the header.
  ```
  PUT /api/events/<event_id>/update
  ```
  Request Body:
  ```json
  {
    "title": "Updated Event Title",
    "description": "Updated Description",
    "date": "2024-12-31T20:00:00Z",
    "location": "Conference Hall B"
  }
  ```

- Example CURL:
  ```bash
  curl -X PUT http://localhost:8000/api/events/1/update \
  -H "Content-Type: application/json" \
  -H "Authorization: Token Your_Token" \
  -d '{
    "title": "Updated Event Title",
    "description": "Updated Description",
    "date": "2024-12-31",
    "location": "Conference Hall B"
  }'
  ```

---

#### 5. Delete an event
- Requires authentication. Token should be provided in the header.
  ```
  DELETE /api/events/<event_id>/delete
  ```

- Example CURL:
  ```bash
  curl -X DELETE http://localhost:8000/api/events/1/delete \
  -H "Authorization: Token Your_Token"
  ```

---


### Admin Interface
Once the superuser is created, you can manage all events, users, and registrations via the Django admin interface at:
```
/admin
```
Accessible at [http://localhost:8000/admin](http://localhost:8000/admin).

