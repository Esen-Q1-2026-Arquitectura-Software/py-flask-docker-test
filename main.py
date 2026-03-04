from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        a = float(request.form["a"])
        b = float(request.form["b"])
        result = a + b
        return redirect(url_for("result", action="Addition", a=a, b=b, result=result))
    return render_template("add.html")


@app.route("/multiply", methods=["GET", "POST"])
def multiply():
    if request.method == "POST":
        a = float(request.form["a"])
        b = float(request.form["b"])
        result = a * b
        return redirect(url_for("result", action="Multiplication", a=a, b=b, result=result))
    return render_template("multiply.html")


@app.route("/power", methods=["GET", "POST"])
def power():
    if request.method == "POST":
        a = float(request.form["a"])
        result = a ** 2
        return redirect(url_for("result", action="Power", a=a, result=result))
    return render_template("power.html")


@app.route("/result")
def result():
    action = request.args.get("action")
    a = request.args.get("a")
    b = request.args.get("b")
    result = request.args.get("result")
    return render_template("result.html", action=action, a=a, b=b, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
