
# Django Event Management Application

This is a Django-based event management application. It allows users to create, manage, and view events. The application is containerized using Docker for easy deployment and development.

---

## Table of Contents

- [Installation with Docker](#installation-with-docker)
- [Installation without Docker](#installation-without-docker)
- [Event Management System: Detailed Functionality](#event-management-system-detailed-functionality)
  - [User Authentication](#1-user-authentication)
  - [Event Creation](#2-event-creation)
  - [Event Management by Owners](#3-event-management-by-owners)
  - [Event Registration](#4-event-registration)
  - [Searching and Viewing Events](#5-searching-and-viewing-events)
  - [Accessing Event Details](#6-accessing-event-details)
  - [Admin Interface](#7-admin-interface)

---

## Installation with Docker

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/boychukmk/EventManager.git
cd EventManager
```

### 2. Build and Start the Docker Container

The application is set up with Docker to simplify the deployment. Run the following command to build and start the container:

```bash
docker build -t event-manager .
docker run -p 8000:8000 --name event-manager event-manager
```

After that, the application will be available at [http://localhost:8000](http://localhost:8000).

### 3. Database Setup

By default, the app uses **SQLite** for the database, so there is no need for complex setup. To apply migrations and initialize the database, run:

```bash
docker exec -it event-manager python manage.py makemigrations
docker exec -it event-manager python manage.py makemigrations events
docker exec -it event-manager python manage.py migrate
```

### 4. Create Superuser 

```bash
docker exec -it event-manager python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password for the superuser. 

Now let`s move to [Event Management Functionality](#event-management-system-detailed-functionality)


To stop the running container:

```bash
docker stop event-manager
```

## Installation without Docker

If you prefer to run the app without Docker:

1. Clone the repository:

```bash
git clone https://github.com/boychukmk/EventManager.git
cd EventManager
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

Now, the app will be available at [http://localhost:8000](http://localhost:8000).

---

## **Event Management System: Detailed Functionality**

### **1. User Authentication**

To interact fully with the application (create events, edit events, register for events), **users must first be authenticated**. Here's how the system works for authenticated and unauthenticated users:

#### **Authentication Required Features:**

- **Create Events**: Only authenticated users can create events by providing details such as the event title, description, date, and location.
- **Edit Events**: If a user is the **owner** (organizer) of an event, they can edit the event's details.
- **Delete Events**: Only the **owner** of an event can delete it. This ensures that only the person who created the event can remove it from the system.
- **Register for Events**: Authenticated users can register for events they wish to attend.

#### **Unauthenticated User Access:**

- **View Events**: Unauthenticated users (non-logged-in users) can only **view** and **search** for events. They are **not able to create, edit, or register for events**.
- **Search**: Unauthenticated users can also search for events.

### **2. Event Creation**

Once logged in, authenticated users can create new events. This involves providing information such as:

- **Title**: The name of the event.
- **Description**: A detailed description of the event.
- **Date**: The scheduled date and time of the event.
- **Location**: Where the event is taking place.

Once the event is created, it will be listed on the event page, and the creator becomes the **organizer**.

### **3. Event Management by Owners**

If a user is the **owner** (organizer) of an event, they have special privileges for managing that event:

- **Edit**: The organizer can update the event details at any time (change the title, description, date, or location).
- **Delete**: The organizer can delete the event from the system if it is no longer needed.

To edit or delete an event, the owner will access the event detail page, where they can make changes or remove the event entirely.

### **4. Event Registration**

Authenticated users can register for an event. Once registered, users can keep track of their events and receive updates if available. Only logged-in users can perform this action.

### **5. Searching and Viewing Events**

Both **authenticated** and **unauthenticated users** can search for events. Users can filter events based on:

- **Keywords**: Users can search for events by title/description or even matching symbols.
- **Location**: Filter events by location to find nearby happenings.

Unauthenticated users can view the event details but are limited in their actions to only viewing and searching. Only **authenticated users** can register, create, edit, or delete events.

### **6. Accessing Event Details**

When viewing an event, the following information is displayed:
- **Event Title**
- **Event Description**
- **Event Date and Time**
- **Event Location**
- **Organizer Name**: The user who created the event.

### **Summary of Permissions:**

| Action                        | Authenticated User | Unauthenticated User |
|-------------------------------|--------------------|----------------------|
| **Create Event**               | Yes                | No                   |
| **Edit Event**                 | Yes (if organizer) | No                   |
| **Delete Event**               | Yes (if organizer) | No                   |
| **Register for Event**         | Yes                | No                   |
| **Search and View Events**     | Yes                | Yes                  |

### **7. Admin Interface**

Once the superuser is created, you can manage all events, users, and their registrations via the Django admin interface at `/admin`.
