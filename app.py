from flask import Flask ,render_template ,request
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(host="localhost", user="root", password="", database='sakila')
app = Flask(__name__)
RATINGS = ['G' , 'PG' , 'PG-13' , 'R' , 'NC-17']
COUNTRIES = ['Afghanistan', 'Algeria', 'American Samoa', 'Angola', 'Anguilla', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Bolivia', 'Brazil', 'Brunei', 'Bulgaria', 'Cambodia', 'Cameroon', 'Canada', 'Chad', 'Chile', 'China', 'Colombia', 'Congo, The Democratic Republic of the', 'Czech Republic', 'Dominican Republic', 'Ecuador', 'Egypt', 'Estonia', 'Ethiopia', 'Faroe Islands', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Gambia', 'Germany', 'Greece', 'Greenland', 'Holy See (Vatican City State)', 'Hong Kong', 'Hungary', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Italy', 'Japan', 'Kazakstan', 'Kenya', 'Kuwait', 'Latvia', 'Liechtenstein', 'Lithuania', 'Madagascar', 'Malawi', 'Malaysia', 'Mexico', 'Moldova', 'Morocco', 'Mozambique', 'Myanmar', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nigeria', 'North Korea', 'Oman', 'Pakistan', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Puerto Rico', 'Romania', 'Réunion', 'Russian Federation', 'Saint Vincent and the Grenadines', 'Saudi Arabia', 'Senegal', 'Slovakia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland', 'Taiwan', 'Tanzania', 'Thailand', 'Tonga', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Venezuela', 'Vietnam', 'Virgin Islands, U.S.', 'Yemen', 'Yugoslavia', 'Zambia']



@app.route('/')
def dashboard():
    query  =  """ SELECT name ,
SUM(total_sales)  AS total ,
SUM(CASE WHEN paymentdate = 'May-2005' THEN total_sales ELSE 0 END ) AS 'May-2005',
SUM(CASE WHEN paymentdate = 'Jun-2005' THEN total_sales ELSE 0 END ) AS 'Jun-2005',
SUM(CASE WHEN paymentdate = 'Jul-2005' THEN total_sales ELSE 0 END ) AS 'Jul-2005',
SUM(CASE WHEN paymentdate = 'Aug-2005' THEN total_sales ELSE 0 END ) AS 'Aug-2005',
SUM(CASE WHEN paymentdate = 'Feb-2006' THEN total_sales ELSE 0 END ) AS 'Feb-2006'
FROM(
SELECT category.name ,date_format(payment_date , '%b-%Y') AS paymentdate ,  SUM(payment.amount) AS total_sales
FROM film 
JOIN film_category 
ON  film.film_id = film_category.film_id  
JOIN category 
ON film_category.category_id = category.category_id
JOIN inventory 
ON film.film_id = inventory.film_id
JOIN rental
ON inventory.inventory_id = rental.inventory_id
JOIN payment 
ON rental.rental_id = payment.rental_id
GROUP BY category.name , paymentdate) sales
GROUP BY  name
"""
    results = execute_fetch_all(query)
    return render_template('dashborad.html' ,results = results )

@app.route("/movies")
def movies():
    rating = request.args.get("rating")
    name_actor = request.args.get("actor")
    params = []
    conditions = []

    if rating:
        if rating not in RATINGS:
            return render_template("error_rating.html")  # صفحة rating غلط
        conditions.append("f.rating = %s")
        params.append(rating)

    if name_actor:
        full_name = name_actor.strip().split(" ")

        if len(full_name) < 2:
            return render_template("error_actor.html")  # اسم غير صحيح

        first_name, last_name = full_name

        conditions.append("a.first_name = %s AND a.last_name = %s")
        params.extend([first_name, last_name])

    if name_actor:
        query = """
        SELECT f.title, f.description
        FROM film f
        JOIN film_actor fa ON fa.film_id = f.film_id
        JOIN actor a ON a.actor_id = fa.actor_id
        """
    else:

        query = "SELECT f.title, f.description FROM film f"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " LIMIT 20"

    results = execute_fetch_all(query, tuple(params))


    if not results:
        return render_template("no_results.html")

    return render_template("movies.html", results=results, RATINGS=RATINGS)        


@app.route('/customer')
def customer():

    country = request.args.get("country")
    name_customer = request.args.get("customer_name")

    params = []
    conditions = []

    if country:
        if country not in COUNTRIES:
            return render_template("error_city.html")
        conditions.append("co.country = %s")
        params.append(country)

    if name_customer:
        full_name = name_customer.strip().split()

        if len(full_name) < 2:
            return render_template("error_customer.html")

        first_name, last_name = full_name[0], full_name[1]

        conditions.append("c.first_name = %s AND c.last_name = %s")
        params.extend([first_name, last_name])

    query = """
    SELECT 
        c.customer_id, 
        c.first_name, 
        c.last_name, 
        c.email, 
        a.address, 
        ct.city, 
        co.country
    FROM customer c
    JOIN address a ON c.address_id = a.address_id
    JOIN city ct ON a.city_id = ct.city_id
    JOIN country co ON ct.country_id = co.country_id
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " LIMIT 20"

    print(query)

    results = execute_fetch_all(query, tuple(params))
    print(results)
    if not results:
        return render_template("no_results.html")

    return render_template(
        'customer.html',
        countries=COUNTRIES,
        results=results
    )


def execute_fetch_all(query, params=None):

        cursor = connection.cursor(dictionary=True)   
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        return results

def execute_fetch_one(query, params=None):

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchone()
    cursor.close()
    return result


if __name__ == '__main__':
    app.run(debug=True)