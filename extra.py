import json
from flask import Flask, request, jsonify, send_from_directory
from elasticsearch import Elasticsearch, helpers
from flask import make_response
from flask import Flask, jsonify
import logging
from elasticsearch import Elasticsearch, ConnectionError, NotFoundError

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Initialize Elasticsearch client
es = Elasticsearch(
    [{'host': 'localhost', 'port': 9200, 'scheme': 'https'}],
    http_auth=('elastic', 'KFLadYQ1J+9fspwZd*_j'),
    verify_certs=False
)
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle uncaught exceptions"""
    return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(404)
def resource_not_found(e):
    response = make_response(jsonify(error=str(e)), 404)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/')
def index():
    return send_from_directory('C:/Users/vaish/OneDrive/Desktop', 'index.html')

@app.route('/initialize', methods=['GET'])
def initialize_index():
    """Index the JSON data into Elasticsearch."""
    try:
        # Read the JSON file
        with open('restaurant.json', 'r') as file:
            data = json.load(file)  # Parse JSON content
        index_data(data)  # Call the indexing function
        return jsonify({"status": "success", "message": "Data indexed successfully"})
    except json.JSONDecodeError as e:
        return jsonify({"status": "error", "message": f"JSON error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"}), 500


def index_data(data):
    """Bulk index data into Elasticsearch."""
    actions = [
        {
            "_index": "restaurants",
            "_id": item['_id'],
            "_source": {
                "name": item['name'],
                "address": item['address'],
                "city": item['city'],
                "type_of_food": item['type_of_food'],
            }
        }
        for item in data
    ]
    helpers.bulk(es, actions)
    es.indices.refresh(index="restaurants")

@app.route('/document/<id>', methods=['POST'])
def create_or_update_document(id):
    """Add or update a restaurant document."""
    try:
        data = request.json
        result = es.index(index="restaurants", id=id, body=data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

@app.route('/document/<id>', methods=['DELETE'])
def delete_document(id):
    """Delete a restaurant document."""
    try:
        es.delete(index="restaurants", id=id)
        return jsonify({"message": "Document deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete document", "details": str(e)}), 500

@app.route('/search', methods=['GET'])
def search():
    """Search for restaurants."""
    query = request.args.get('q', '')
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "address", "city", "type_of_food"]
            }
        }
    }
    try:
        result = es.search(index="restaurants", body=body)
        # Include `_id` in the response
        return jsonify([{"_id": hit["_id"], **hit["_source"]} for hit in result['hits']['hits']])
    except Exception as e:
        return jsonify({"error": "Failed to search", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)