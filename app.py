from website import create_app

app = create_app()

@app.route("/")
def index():
    return "wsdecvqefvii"

if __name__ == "__main__":
    app.run(debug=True)

