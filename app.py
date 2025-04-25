from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

# Load the saved model components
try:
    pivot_tab = pickle.load(open('pivot_table.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
    books_df = pickle.load(open('books_dataframe.pkl', 'rb'))  # Load the dataframe with ratings
except FileNotFoundError as e:
    print(f"Error loading model components: {e}")
    pivot_tab = None
    similarity_scores = None
    books_df = None

def recommend_books(book_name, pivot_table, similarity_matrix, books_data, top_n=5):
    if pivot_table is None or similarity_matrix is None or books_data is None:
        return {"error": "Model components not loaded."}

    if book_name in pivot_table.index:
        try:
            index = np.where(pivot_table.index == book_name)[0][0]
            similar_items = sorted(list(enumerate(similarity_matrix[index])),
                                       key=lambda x: x[1], reverse=True)[1:top_n+1]

            recommendations = []
            for i in similar_items:
                book_title = pivot_table.index[i[0]]
                # Directly use books_data which now contains the rating information
                temp_df = books_data[books_data['Book-Title'] == book_title]
                if not temp_df.empty:
                    book_info = {
                        'title': temp_df['Book-Title'].iloc[0],
                        'author': temp_df['Book-Author'].iloc[0],
                        'image_url': temp_df['Image-URL-M'].iloc[0],
                        'average_rating': float(temp_df['Average_Rating'].iloc[0]),  # Get average rating
                        'rating_count': int(temp_df['Rating_Count'].iloc[0])    # Get rating count
                    }
                    recommendations.append(book_info)
            return {"recommendations": recommendations}
        except Exception as e:
            return {"error": f"Error generating recommendations: {e}"}
    else:
        close_matches = get_close_matches(book_name, pivot_table.index, n=7, cutoff=0.1)
        if close_matches:
            suggestions = []
            for match in close_matches:
                temp_df = books_data[books_data['Book-Title'] == match]
                if not temp_df.empty:
                    suggestion_info = {
                        'title': temp_df['Book-Title'].iloc[0],
                        'author': temp_df['Book-Author'].iloc[0],
                        'image_url': temp_df['Image-URL-M'].iloc[0],
                        'average_rating': float(temp_df['Average_Rating'].iloc[0]), #Get average rating for suggestion
                        'rating_count': int(temp_df['Rating_Count'].iloc[0])   # Get rating count for suggestion
                    }
                    suggestions.append(suggestion_info)
            return {"suggestions": suggestions}
        else:
            return {"error": f"Book '{book_name}' not found in our catalog."}

@app.route('/recommend', methods=['POST'])
def get_recommendations_api():
    data = request.get_json()
    if not data or 'book_name' not in data:
        return jsonify({'error': 'Please provide a book_name in the request body.'}), 400

    book_name = data['book_name']
    result = recommend_books(book_name, pivot_tab, similarity_scores, books_df)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)