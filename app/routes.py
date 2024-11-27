from flask import render_template, request, Blueprint, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import json
from flask import send_from_directory
from bson.objectid import ObjectId


main = Blueprint("main", __name__)

UPLOAD_FOLDER = "./app/static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "docx", "txt"}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Use the MongoDB Atlas connection string
MONGO_URI = os.getenv("MONGO_URI")  # Load from environment or use .env setup
client = MongoClient(MONGO_URI)
db = client["cluster"]  # Database name
help_collection = db["help_submissions"]  # Collection name

@main.route("/")
def index():
    # Load resources and sources from JSON files
    with open("data/resources.json") as resources_file:
        resources = json.load(resources_file)
    
    with open("data/sources.json") as sources_file:
        sources = json.load(sources_file)
    
    # Calculate dynamic statistics
    stats = {
        "total_resources": len(resources),
        "unique_categories": len(set(res["category"] for res in resources)),
        "recent_visitors": 10000  # Replace this with real data if available
    }
    
    return render_template("index.html", title="Alesul Gresit", resources=resources, stats=stats, sources=sources)

@main.route("/help", methods=["GET", "POST"])
def help_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        link = request.form.get("link")
        message = request.form.get("message")
        file = request.files.get("file")

        # Handle file upload
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            file_path = os.path.join(UPLOAD_FOLDER, filename)
        else:
            file_path = None  # No file uploaded or invalid file type

        # Insert into MongoDB Atlas
        help_collection.insert_one({
            "name": name,
            "email": email,
            "link": link,
            "message": message,
            "file_path": file_path,  # Store the uploaded file path
            "timestamp": datetime.utcnow()
        })

        # Redirect with success message
        return redirect(url_for("main.help_page", success=True))

    success = request.args.get("success")
    return render_template("help.html", title="Cum poți ajuta?", success=success)

@main.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    results = []

    # Load resources from the JSON file
    with open("data/resources.json") as file:
        resources = json.load(file)

    # Filter resources based on query
    for resource in resources:
        if query in resource["title"].lower() or query in resource["description"].lower() or query in " ".join(resource["tags"]).lower():
            results.append(resource)

    return render_template("search.html", title="Caută Resurse", query=query, results=results)

@main.route("/resources")
def resources():
    # Load resources from the JSON file
    with open("data/resources.json") as file:
        resources = json.load(file)
    return render_template("resources.html", title="Resurse", resources=resources)

@main.route("/about")
def about():
    return render_template("about.html", title="Despre Proiect")

@main.route("/glossary")
def glossary():
    terms = {
        "Fascism": {
            "definition": "Doctrină politică și ideologie totalitară care promovează naționalismul extremist, autoritarismul și suprimarea opoziției politice.",
            "link": "https://dexonline.ro/definitie/Fascism"
        },
        "Legionarism": {
            "definition": "Mișcare politică, ideologică și religioasă de extremă dreapta din România, asociată cu Garda de Fier.",
            "link": "https://dexonline.ro/definitie/Legionarism"
        },
        "Rusofil": {
            "definition": "Persoană sau atitudine care manifestă simpatie pentru Rusia sau cultura rusă.",
            "link": "https://dexonline.ro/definitie/Rusofil"
        },
        "NATO": {
            "definition": "Organizația Tratatului Atlanticului de Nord, o alianță militară formată din state membre pentru apărarea colectivă.",
            "link": "https://dexonline.ro/definitie/NATO"
        },
        "UE": {
            "definition": "Uniunea Europeană, o uniune politico-economică formată din 27 de state membre din Europa.",
            "link": "https://dexonline.ro/definitie/UE"
        },
        "Suveran": {
            "definition": "Care deține puterea supremă într-un stat; independent.",
            "link": "https://dexonline.ro/definitie/Suveran"
        },
        "Antisemit": {
            "definition": "Persoană sau atitudine care manifestă ostilitate față de evrei.",
            "link": "https://dexonline.ro/definitie/Antisemit"
        },
        "Diaspora": {
            "definition": "Comunitățile de oameni care trăiesc în afara țării lor de origine.",
            "link": "https://dexonline.ro/definitie/Diaspora"
        },
        "Masonerie": {
            "definition": "Organizație fraternă asociată cu simbolismul masonic, adesea înconjurată de mister și controversă.",
            "link": "https://dexonline.ro/definitie/Masonerie"
        },
        "Pedologie": {
            "definition": "Știința care studiază formarea, compoziția și proprietățile solurilor.",
            "link": "https://dexonline.ro/definitie/Pedologie"
        },
        "H2O": {
            "definition": "Formula chimică a apei, compus format din doi atomi de hidrogen și un atom de oxigen.",
            "link": "https://dexonline.ro/definitie/H2O"
        },
        "Cezariană": {
            "definition": "Procedură chirurgicală prin care se extrage fătul din uter printr-o incizie în abdomen.",
            "link": "https://dexonline.ro/definitie/Cezariană"
        },
        "Populism": {
            "definition": "Politică bazată pe apeluri emoționale către mase, adesea însoțită de promisiuni simpliste pentru probleme complexe.",
            "link": "https://dexonline.ro/definitie/Populism"
        },
        "Extremism": {
            "definition": "Atitudine politică, religioasă sau ideologică caracterizată prin opinii radicale și refuzul compromisului.",
            "link": "https://dexonline.ro/definitie/Extremism"
        },
        "Propagandă": {
            "definition": "Activitate sistematică de răspândire a ideilor, informațiilor sau doctrinei pentru a influența opinia publică.",
            "link": "https://dexonline.ro/definitie/Propaganda"
        },
        "Autocrație": {
            "definition": "Formă de guvernare în care puterea este concentrată în mâinile unei singure persoane.",
            "link": "https://dexonline.ro/definitie/Autocratie"
        },
        "Xenofobie": {
            "definition": "Aversiune sau frică față de străini sau față de ceea ce este perceput ca fiind diferit cultural.",
            "link": "https://dexonline.ro/definitie/Xenofobie"
        },
        "Naționalism": {
            "definition": "Ideologie care promovează interesele și identitatea națională, adesea în opoziție cu alte grupuri etnice sau națiuni.",
            "link": "https://dexonline.ro/definitie/Nationalism"
        },
        "Război hibrid": {
            "definition": "Strategie militară care combină metode convenționale și neconvenționale, inclusiv propagandă și atacuri cibernetice.",
            "link": "https://dexonline.ro/definitie/Razboi"
        },
        "Corupție": {
            "definition": "Utilizarea abuzivă a puterii publice în interes personal.",
            "link": "https://dexonline.ro/definitie/Coruptie"
        },
        "Inflație": {
            "definition": "Creștere generală a prețurilor bunurilor și serviciilor într-o economie.",
            "link": "https://dexonline.ro/definitie/Inflatie"
        },
        "Fake news": {
            "definition": "Informații false sau înșelătoare prezentate ca fiind știri reale.",
            "link": "https://dexonline.ro/definitie/Fake news"
        }
    }
    return render_template("glossary.html", title="Glosar", terms=terms)

@main.route("/voices", methods=["GET", "POST"])
def voices():
    if request.method == "POST":
        # Collect form data and save to MongoDB
        name = request.form.get("name")
        email = request.form.get("email")
        title = request.form.get("title")
        content = request.form.get("content")
        file = request.files.get("file")

        # Handle file upload
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = filename
        else:
            image_url = None

        # Insert into MongoDB
        db["voices"].insert_one({
            "name": name,
            "email": email,
            "title": title,
            "content": content,
            "image_url": image_url,
            "timestamp": datetime.utcnow()
        })

        # Redirect with a success message
        return redirect(url_for("main.voices", success=True))

    # Check for success parameter in GET request
    success = request.args.get("success")
    articles = list(db["voices"].find().sort("timestamp", -1))
    return render_template("voices.html", title="Vocea Ta", articles=articles, success=success)

@main.route("/voices/<article_id>")
def article_detail(article_id):
    try:
        article = db["voices"].find_one({"_id": ObjectId(article_id)})
        if not article:
            return "Articolul nu a fost găsit.", 404
    except Exception as e:
        return f"Eroare: {str(e)}", 400
    return render_template("article_detail.html", title=article["title"], article=article)


@main.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)