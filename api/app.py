from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

DESIRED_KEYS = ["hash", "family"]


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(200), nullable=False)
    family = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<File with hash {self.hash} from family {self.family}>'


def validate_json(json_data: dict) -> bool:
    return any(key in json_data for key in DESIRED_KEYS)


@app.route('/', methods=['POST'])
def add_sample():
    json_data = request.get_json(silent=True)
    if not validate_json(json_data=json_data):
        return "Bad request", 400

    new_sample = Sample(hash=json_data["hash"], family=json_data["family"])

    try:
        db.session.add(new_sample)
        db.session.commit()
        return "Sample added successfully", 201
    except Exception:
        return "Something went wrong", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
