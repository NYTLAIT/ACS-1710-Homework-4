# Homework 4: Weather API

This is the starter code for the 4th homework assignment for WEB 1.1. Follow the instructions here: https://github.com/Tech-at-DU/ACS-1710-Web-Architecture/blob/master/Assignments/03-APIs.md


Sure! Here's a short and beginner-friendly description of RESTful routing tailored specifically to your **Flask weather app project**:

---

## 🌦️ RESTful Routing in the Weather App

In this project, we use **RESTful routing** to make our Flask app’s URLs clean, meaningful, and easy to understand.

### 🔹 What is RESTful Routing?

RESTful routes follow a convention where:

* **URLs represent resources** (like weather data),
* **HTTP methods** represent actions (like GET to read data).

This helps keep your app organized and easier to scale or connect with APIs and frontends.

### 📍 Routes in This Project

Here’s how we apply RESTful naming to our weather app:

| URL Path              | Purpose                            | RESTful Naming Tip                   |
| --------------------- | ---------------------------------- | ------------------------------------ |
| `/`                   | Homepage with weather search forms | This is a standard homepage route. ✅ |
| `/weather`            | Shows current weather for a city   | Describes the resource: weather. ✅   |
| `/weather/comparison` | Compares weather for two cities    | Nested route shows relationship. ✅   |

Instead of generic names like `/results` or `/comparison_results`, we use routes that **clearly describe the type of data** we’re showing.

### ✅ Why It Matters

* Makes your code easier to read and maintain.
* Helps frontend developers or future you understand what each route does.
* Prepares you for building scalable apps and APIs.

### 🧠 Quick Tip

Use nouns for resources (`weather`) and avoid verbs in your URLs. The **HTTP method** already tells the app what to do (e.g., GET gets data).
