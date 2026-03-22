# 🎬 Movie & Customer Analytics System

A Flask-based web application built on top of the Sakila MySQL database, focused on dynamic data exploration and backend-driven analytics.

---

## 🚀 Features

* 🎥 Filter movies by:

  * Rating
  * Actor name
* 👤 Search customers by:

  * Full name
  * Country
* 📊 Sales dashboard:

  * Aggregated revenue by film category
  * Monthly breakdown using SQL analytics
* ⚡ Dynamic query building (no hardcoded queries)
* 🔒 Input validation for safer data handling

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** MySQL (Sakila DB)
* **Frontend:** Jinja2 Templates + HTML/CSS
* **Queries:** Raw SQL with dynamic conditions

---

## 🧠 Key Concepts Applied

* Dynamic SQL query construction
* Prepared statements (SQL Injection prevention)
* Relational database joins (multi-table queries)
* Aggregation & analytics queries (SUM, CASE WHEN)
* Input validation and error handling

---

## 📂 Project Structure

```
project/
│── app.py
│── templates/
│   ├── movies.html
│   ├── customer.html
│   ├── dashboard.html
│   ├── error_customer.html
│   ├── error_actor.html
│   ├── error_city.html
│   ├── error_rating.html
│   ├── layout.html
│   ├── no_result.html
│
```

---

## ⚙️ Setup & Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Install dependencies:

```bash
pip install flask mysql-connector-python
```

3. Configure MySQL:

* Import the **Sakila database**
* Update database credentials in `app.py`

4. Run the app:

```bash
python app.py
```

5. Open in browser:

```
http://127.0.0.1:5000/
```

---

## ⚠️ Notes

* This project is focused on backend logic and SQL handling
* Not optimized yet for production (no connection pooling / caching)
* Uses raw SQL instead of ORM for learning and control

---

## 🎯 Future Improvements

* Add REST API layer
* Implement pagination & caching
* Integrate ORM (SQLAlchemy)
* Add authentication & security layers
* Connect with AI (Natural Language → SQL)


