## ML Project: Book Recommendation System on a Static Dataset

This repository contains the code for a book recommendation system built using machine learning techniques. The system is designed to take a book title as input and return a list of recommended books based on patterns learned from a static dataset.

### Overview

This project demonstrates a basic implementation of a book recommendation system without relying on a live database for book additions or real-time updates. The model is trained on a specific dataset (originally sourced from [Kaggle Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?select=Ratings.csv)) and provides recommendations based on the learned relationships between books.

The repository includes:

- **`app.py`:** A Flask application that exposes an API endpoint (`/recommend`) to receive a book title and return recommendations.
- **`recommendation_model.pkl`:** (Placeholder - this file would contain your serialized, trained recommendation model.)
- **`Books.csv`:** (Placeholder - this file would contain the book metadata from the dataset.)
- **`Ratings.csv`:** (Placeholder - this file would contain the user ratings data from the dataset.)
- **`requirements.txt`:** A list of Python libraries required to run the Flask application.
- **`website/`:** A directory containing a simple HTML, CSS, and JavaScript front-end to interact with the recommendation API.
  - `website/index.html`: The main webpage with an input field for book titles and a display area for recommendations.
  - `website/style.css`: Basic styling for the webpage.
  - `website/script.js`: JavaScript code to send requests to the API and display the results.
- **`README.md`:** This file, providing an overview of the project and instructions for setup and usage.

### Setup

1.  **Clone the repository:**

    ```bash
    git clone [repository_url]
    cd [repository_name]
    ```

2.  **Install the required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **(Ensure your trained model and data are present):**
    Make sure you have your trained recommendation model saved as `recommendation_model.pkl` and the dataset files (`Books.csv`, `Ratings.csv`) in the root directory of the repository (or adjust the file paths in `app.py` accordingly).

4.  **Navigate to the `website` directory (optional):**
    ```bash
    cd website
    ```

### Running the Application

**Running the Flask API (Backend):**

1.  Open a terminal in the root directory of the repository.
2.  Run the Flask application:
    ```bash
    python app.py
    ```
    This will start the Flask development server (usually on `http://127.0.0.1:5000/`).

**Running the Simple Website (Frontend):**

1.  Navigate to the `website` directory in your file explorer.
2.  Open the `index.html` file in your web browser.

**Using the Recommendation System:**

1.  Ensure the Flask API is running in your terminal.
2.  In your web browser, in the "Book Recommendation" webpage, enter the title of a book you'd like recommendations for in the input field.
3.  Click the "Get Recommendations" button.
4.  The recommended books will be displayed below.

**Alternatively, you can directly interact with the API using tools like `curl` or Postman:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"book_name": "Animal Farm"}' [http://127.0.0.1:5000/recommend](http://127.0.0.1:5000/recommend)
```
