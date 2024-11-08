from flask import Flask, request, jsonify

file = input("Input File Path: ")
with open(file, "r") as f:
    data = f.read()
tags = {"cs":"A7", "ece":"AA", "eee":"A3", "eni":"A8", "mech":"A4", "civil":"A2", "phy":"B5", "chemical":"A1", "chem":"B2", "math":"B4", "bio":"B1", "pharma":"A5", "manu":"AB", "genstudies":"D2"}


app = Flask(__name__)
@app.route("/")
def home():
    
    print(request.args)
    format = request.args.get("format")
    branch = request.args.get("branch")
    year = request.args.get("year")
    if format:
        return "<pre>"+data+"</pre>", 200
    
    elif branch:
        if branch in tags:
            course = tags[branch]
            ids = data.split("\n")
            json = {"ids": []}
            for id in ids:
                if course in id:
                    json["ids"].append(id)
            return jsonify(json), 200
        else:
            return jsonify({"error": "branch not found"}), 400
    
    elif year:
        ids = data.split("\n")
        json = {"ids":[]}
        for id in ids:
            if id.startswith(year):
                json["ids"].append(id)
        return jsonify(json), 200
    
    else:
        ids = data.split("\n")
        json = {"id": ids}
        return jsonify(json), 200

@app.route("/<id>")
def info(id):
    ids = data.split("\n")
    for bitsid in ids:
        if bitsid[-5:-1] == id:
            break
    else:
        return jsonify({"error": "ID not found"}), 400
    json = {"id":{"uid":id}}

    year = bitsid[:4]
    json["id"]["year"] = 2025 - int(year)
    
    campustag = {"P": "pilani", "G": "goa", "H":"hyderabad", "D": "dubai"}
    campus = campustag[bitsid[-1]]
    json["id"]["campus"] = campus
    
    json["id"]["email"] = "f"+year+bitsid[-5:-1]+"@"+campus+".bits-pilani.ac.in"

    branch = list(tags.keys())[list(tags.values()).index(bitsid[4:6])]
    json["id"]["branch"] = branch
    return jsonify(json), 200


if __name__ == "__main__":
    app.run(debug=True)
