import os
from flask import Flask, jsonify, request
import requests
import socket
from googletrans import Translator
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # This line enables CORS for all routes on all origins


def get_book_data_by_isbn(isbn):
    url = (
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    )
    response = requests.get(url)

    if response.status_code == 200:
        book_data = response.json()
        if book_data:
            key = f"ISBN:{isbn}"
            if key in book_data:
                book_info = book_data[key]

                # Agregar URL de la portada
                cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

                return {
                    "cover_url": cover_url,  # Agregar la URL de la portada
                }
            else:
                return {"error": "No data found for this ISBN."}
        else:
            return {"error": "No data found for this ISBN."}
    else:
        return {"error": f"Error fetching data. Status code: {response.status_code}"}


@app.route("/api/book", methods=["GET"])
def get_book():
    isbn = request.args.get("isbn")
    if not isbn:
        return jsonify({"error": "Please provide an ISBN"}), 400

    book_data = get_book_data_by_isbn(isbn)
    return jsonify(book_data)

# DOTENV
load_dotenv()

if __name__ == "__main__":
    _port = os.getenv("PORT")
    _host = os.getenv("HOST")
    ip_address = socket.gethostbyname(socket.gethostname())
    app.run(debug=False, host=_host, port=_port)
    print(f"Servidor flask corriendo en http://{ip_address}:{_port}")
