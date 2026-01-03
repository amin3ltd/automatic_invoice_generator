from flask import Flask, render_template, make_response
from xhtml2pdf import pisa
import io
import datetime

app = Flask(__name__)

def get_invoice_data():
    line_items = [
        {"name": "Website Design", "price": 300.00},
        {"name": "Hosting (3 months)", "price": 75.00},
        {"name": "Domain Name (1 year)", "price": 10.00}
    ]

    total = sum(item["price"] for item in line_items)

    return {
        "invoice_number": "123",
        "created_date": datetime.date.today().strftime("%B %d, %Y"),
        "due_date": (datetime.date.today() + datetime.timedelta(days=30)).strftime("%B %d, %Y"),
        "company": {
            "name": "Sparksuite, Inc.",
            "address": "12345 Sunny Road",
            "city": "Sunnyville, CA 12345"
        },
        "customer": {
            "name": "Acme Corp.",
            "contact": "John Doe",
            "email": "john@example.com"
        },
        "line_items": line_items,   # ✅ renamed (IMPORTANT)
        "total": total,
        "notes": "Thank you for your business!"
    }

@app.route("/")
def index():
    invoice = get_invoice_data()
    return render_template("invoice.html", invoice=invoice)

@app.route("/download")
def download_pdf():
    invoice = get_invoice_data()
    html = render_template("invoice.html", invoice=invoice)

    pdf_buffer = io.BytesIO()
    result = pisa.CreatePDF(html, dest=pdf_buffer)

    if result.err:
        return "Error generating PDF", 500

    response = make_response(pdf_buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f'inline; filename=invoice_{invoice["invoice_number"]}.pdf'
    )
    return response

if __name__ == "__main__":
    app.run(debug=True)
