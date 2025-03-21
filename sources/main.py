from flask import Flask, render_template, request
from PIL import Image
from scrapInfos import scrapInfos
# import test
from test import final_res

app = Flask(__name__)

EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("index.html")

@app.route('/art', methods=['POST'])
def uploadImageAndRenderResult():
    if 'image' not in request.files:
        return render_template('error.html', error='Aucune image trouvée dans la requête')
    file = request.files['image']

    if file and allowed_file(file.filename):
        image = Image.open(file)
        new_size = (256, 256)  
        image = image.resize(new_size, Image.LANCZOS)
        
        url = final_res(image, int(request.form.get('threshold')))

        try:
            return render_template("oeuvre.html", scrap=scrapInfos(url))
        except:
            return render_template('error.html', error='Aucune correspondance trouvée.')
    else:
        return render_template('error.html', error='Fichier non autorisé ou invalide')

if __name__ == "__main__":
    app.run(debug=True)