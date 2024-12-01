
---

# Restaurant Finder

This project is a Flask-based web application that allows users to add, update, search, and delete restaurant entries stored in an Elasticsearch database. The application uses HTML for the front-end and Python for the back-end.

---

## Prerequisites

1. **Python**: Ensure Python (3.8 or later) is installed on your system.
   - [Download Python](https://www.python.org/downloads/)
2. **Elasticsearch**: Install and run Elasticsearch (v8.x recommended).
   - [Download Elasticsearch](https://www.elastic.co/downloads/elasticsearch)
3. **Flask**: Python microframework for the back-end.
4. **cURL**: Command-line tool for HTTP requests.
5. **Git**: To clone the repository.

---

## Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Vaishnavichunchu/RestaurantApp.git
   cd RestaurantApp
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Download and set up Elasticsearch:
   - Start Elasticsearch by navigating to the `bin` directory and running:
     ```bash
     ./elasticsearch.bat  # Windows
     ./bin/elasticsearch  # Linux/MacOS
     ```
   - Ensure Elasticsearch is running on `http://localhost:9200`.

4. Update the Elasticsearch credentials in `extra.py`:
   - Replace the username and password in the following line:
     ```python
     es = Elasticsearch(
         [{'host': 'localhost', 'port': 9200, 'scheme': 'https'}],
         http_auth=('elastic', 'your_password'),
         verify_certs=False
     )
     ```

5. Run the Flask application:
   ```bash
   python extra.py
   ```

---

## How to Use

1. **Initialize the Index**:
   - Open your terminal and execute:
     ```bash
     curl.exe -X GET "http://localhost:5000/initialize"
     ```
   - This initializes the Elasticsearch index and loads data from `restaurant.json`.

2. **Access the Web Application**:
   - Open your browser and navigate to:
     ```
     http://localhost:5000
     ```

3. **Perform CRUD Operations**:
   - **Add/Update**: Enter restaurant details and click "Submit".
   - **Search**: Use the search bar to find restaurants by name, address, city, or type of food.
   - **Delete**: Click the "Delete" button next to a restaurant entry to remove it from the database.

4. **Verify Elasticsearch Data**:
   - To verify indexed data in Elasticsearch:
     ```bash
     curl.exe -X GET "http://localhost:9200/restaurants/_search?pretty" -H "Content-Type: application/json" -d "{\"query\": {\"match_all\": {}}}"
     ```

5. **Reset the Index**:
   - To delete all data and reinitialize:
     ```bash
     curl.exe -X DELETE "http://localhost:9200/restaurants" -u elastic:your_password
     curl.exe -X GET "http://localhost:5000/initialize"
     ```

---

## Commands Used

### Start the Flask Application
```bash
python extra.py
```

### Initialize Data
```bash
curl.exe -X GET "http://localhost:5000/initialize"
```

### Search Data
```bash
curl.exe -X GET "http://localhost:9200/restaurants/_search?pretty" -H "Content-Type: application/json" -d "{\"query\": {\"match_all\": {}}}"
```

### Delete Data
```bash
curl.exe -X DELETE "http://localhost:9200/restaurants" -u elastic:your_password
```

---

## Troubleshooting

- **Elasticsearch connection issues**:
  Ensure Elasticsearch is running and accessible at `http://localhost:9200`.

- **Data not appearing in the search**:
  Check if the data is properly initialized using the `/initialize` endpoint.

- **Permission errors on Windows**:
  Run the terminal as Administrator.

---
Notes
Ensure the HTML and JSON file paths in extra.py match their actual locations on your system.
Always restart Elasticsearch if you encounter connection issues.
For changes in the dataset, update the JSON file and reinitialize using the /initialize endpoint.
