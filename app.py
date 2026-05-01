from flask import Flask, render_template, request
from data_loader import load_all_data
from evo_engine import evolve_population

app = Flask(__name__)

# تحميل المنتجات مرة واحدة
_, products_df, _, _ = load_all_data()


# الصفحة الرئيسية (مع pagination)
@app.route("/")
def landing():

    page = int(request.args.get("page", 1))
    per_page = 6

    all_products = products_df.to_dict(orient="records")

    start = (page - 1) * per_page
    end = start + per_page

    products = all_products[start:end]

    total_pages = (len(all_products) + per_page - 1) // per_page

    return render_template(
        "home.html",
        products=products,
        page=page,
        total_pages=total_pages
    )


# صفحة التوصيات
@app.route("/run", methods=["POST"])
def generate():

    user_key = request.form["user_key"]

    recommended_ids = evolve_population(user_key)

    return render_template(
        "output.html",
        recommendations=recommended_ids,
        user=user_key
    )


if __name__ == "__main__":
    app.run(debug=True)