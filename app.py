from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the saved model components
try:
    pivot_tab = pickle.load(open('pivot_table.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
    books_df = pickle.load(open('books_dataframe.pkl', 'rb'))
except FileNotFoundError as e:
    print(f"Error loading model components: {e}")
    pivot_tab = None
    similarity_scores = None
    books_df = None

def recommend_books(book_name, pivot_table, similarity_matrix, books_data, top_n=5):
    if pivot_table is None or similarity_matrix is None or books_data is None:
        return "Error: Model components not loaded."

    if book_name not in pivot_table.index:
        return f"Book '{book_name}' not found in our catalog."

    try:
        index = np.where(pivot_table.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_matrix[index])),
                                   key=lambda x: x[1], reverse=True)[1:top_n+1]

        recommendations = []
        for i in similar_items:
            book_title = pivot_table.index[i[0]]
            temp_df = books_data[books_data['Book-Title'] == book_title]
            if not temp_df.empty:
                book_info = {
                    'title': temp_df['Book-Title'].iloc[0],
                    'author': temp_df['Book-Author'].iloc[0],
                    'image_url': temp_df['Image-URL-M'].iloc[0]
                }
                recommendations.append(book_info)
        return recommendations

    except Exception as e:
        return f"Error generating recommendations: {e}"

@app.route('/recommend', methods=['POST'])
def get_recommendations_api():
    data = request.get_json()
    if not data or 'book_name' not in data:
        return jsonify({'error': 'Please provide a book_name in the request body.'}), 400

    book_name = data['book_name']
    recommendations = recommend_books(book_name, pivot_tab, similarity_scores, books_df)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)