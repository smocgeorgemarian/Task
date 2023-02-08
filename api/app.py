from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
db = SQLAlchemy(app)

DESIRED_KEYS = ["hash", "family"]


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(200), nullable=False)
    family = db.Column(db.String(200), nullable=False)
    __table_args__ = (UniqueConstraint('hash', name='_hash_'),)

    def __repr__(self):
        return f'<File with hash {self.hash} from family {self.family}>'


def validate_json(json_data: dict) -> bool:
    return all(key in json_data for key in DESIRED_KEYS)


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


@app.route('/hashes/<string:hash_value>', methods=['GET'])
def get_family_by_hash(hash_value: str):
    sample = Sample.query.filter_by(hash=hash_value).first()
    if sample is None:
        return f"Sample with hash {hash_value} could not be found", 404
    return sample.family, 200


@app.route('/families/<string:family>', methods=['GET'])
def get_hashes_by_family(family: str):
    hashes = list(map(lambda s: s.hash, Sample.query.filter_by(family=family)))
    return hashes, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
