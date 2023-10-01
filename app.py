from website import create_app, create_database

app = create_app()

# Create the database schema (tables)
create_database(app)

@app.route("/")
def index():
    return "wsdecvqefvii"

if __name__ == "__main__":
    app.run(debug=True)
