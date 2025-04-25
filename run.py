from flask import Flask, render_template, request, jsonify
from main import llm_model
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial

app = Flask(__name__)

# Create a thread pool for concurrent processing
executor = ThreadPoolExecutor(max_workers=100)  # Adjust the number of workers

# Helper function to apply the LLM model to a ticket description
def analyze_ticket(ticket_description):
    return llm_model({"ticket_description": ticket_description})

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_single():
    data = request.get_json()
    ticket_description = data.get("ticket_description", "")
    response = llm_model({"ticket_description": ticket_description})
    return response

@app.route("/analyze_bulk", methods=["POST"])
def analyze_bulk():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    
    # Read the file as a DataFrame
    df = pd.read_excel(file)
    
    # Ensure there is a "description" column in the uploaded file
    if 'description' not in df.columns:
        return jsonify({"error": "File must contain a 'description' column"}), 400
    
    # Prepare the ticket descriptions for parallel processing
    descriptions = df['description'].tolist()
    ticket_numbers = df['number'].tolist()
    
    # Use ThreadPoolExecutor to process descriptions in parallel
    with executor as pool:
        results = list(pool.map(analyze_ticket, descriptions))
    
    # Prepare the results with corresponding ticket numbers
    priority_data = [{"S.No": num, "Description": desc, "Priority": priority} 
                     for num, desc, priority in zip(ticket_numbers, descriptions, results)]
    
    # Sort results by priority (high to low)
    priority_map = {"High": 3, "Mid": 2, "Low": 1}
    priority_data.sort(key=lambda x: priority_map.get(x["Priority"], 0), reverse=True)

    # Convert results to DataFrame
    result_df = pd.DataFrame(priority_data)

    # Convert DataFrame to an HTML table
    return result_df.to_html(index=False, classes="priority-table", header=True)

if __name__ == '__main__':
   app.run(debug=True)
