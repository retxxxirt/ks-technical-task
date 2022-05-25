from datetime import date
from decimal import Decimal
from typing import Any

from flask import Flask, jsonify
from flask.json import JSONEncoder as BaseJSONEncoder
from flask_cors import CORS
from sqlmodel import Session, SQLModel

from app.database import engine, DatabaseOrder


class JSONEncoder(BaseJSONEncoder):
    """JSOEncoder for date and Decimal"""

    def default(self, value: Any) -> Any:
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, Decimal):
            return float(value)
        return super().default(value)


# create database models if not exists
SQLModel.metadata.create_all(engine)

app = Flask("backend")
app.json_encoder = JSONEncoder

# allow all cors for app
CORS(app)


@app.route("/give-me-everything-you-know/")
def get_all_orders():
    """Return all orders sorted by table_id inside json object"""

    with Session(engine) as session:
        query = session.query(DatabaseOrder).order_by(DatabaseOrder.table_id)
        return jsonify(results=[o.dict() for o in query])
