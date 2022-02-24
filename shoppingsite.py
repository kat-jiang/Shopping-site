"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session
import jinja2
import os
import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = os.environ['SECRET_KEY']

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""
    session["cart"] = {}
    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""
    
    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    #create and return a list of melon objects that also had quantity and total cost
    #what we have is a dictionary of key melon_id and value quantity

    cart_dict = session["cart"]
    melons_list = []
    total_cost = 0

    for id in cart_dict:   
        melon_purchase = melons.Melon(id,
                                melons.melon_types[id],
                                melons.melon_types[id].common_name,
                                melons.melon_types[id].price,
                                melons.melon_types[id].image_url,
                                melons.melon_types[id].color,
                                melons.melon_types[id].seedless,
                                cart_dict[id]
                                )
        melon_purchase.update_line_price()
        melons_list.append(melon_purchase)
        total_cost += melon_purchase.line_price


    #-----------------------solution list in list------------------#
    # for melon in cart_dict:
    #     display_name = melons.melon_types[melon].common_name
    #     unit_cost = melons.melon_types[melon].price
    #     quantity = cart_dict[melon]
    #     line_total = unit_cost * quantity
        
    #     total_cost += line_total

    #     single_melon_list = [display_name, unit_cost, quantity, line_total]

    #     melons_list.append(single_melon_list)

    return render_template("cart.html", melons_list=melons_list, total=total_cost)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # TODO: Finish shopping cart functionality

    #if cart exists in current sesssion
   
    if session.get("cart") == None:
        session["cart"] = {}

    #use get to increment the count of this melon in the cart by one
    session["cart"][melon_id] = session["cart"].get(melon_id, 0) + 1

    #flash message to confirm addition to cart, will fix this later to say the actual melon
    flash(f"Your melon has been added to your cart!")

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!


    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
