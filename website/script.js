function getRecommendations() {
  const bookName = document.getElementById("bookInput").value;
  const recommendationList = document.getElementById("recommendationList");
  recommendationList.innerHTML = "Loading recommendations...";

  fetch("http://127.0.0.1:5000/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ book_name: bookName }),
  })
    .then((response) => response.json())
    .then((data) => {
      recommendationList.innerHTML = "";
      if (
        data.recommendations &&
        Array.isArray(data.recommendations) &&
        data.recommendations.length > 0
      ) {
        const titleHeading = document.createElement("h3");
        titleHeading.textContent = `Recommendations for "${
          document.getElementById("bookInput").value
        }":`;
        recommendationList.appendChild(titleHeading);
        data.recommendations.forEach((book) => {
          const listItem = document.createElement("li");
          const image = document.createElement("img");
          image.src = book.image_url;
          image.alt = book.title + " cover";
          listItem.appendChild(image);

          const details = document.createElement("div");
          const title = document.createElement("h3");
          title.textContent = book.title;
          const author = document.createElement("p");
          author.textContent = "Author: " + book.author;
          const avgRating = document.createElement("p");
          avgRating.textContent =
            "Average rating: " + book.average_rating.toFixed(2); // Display 2 decimal places
          const ratingCount = document.createElement("p");
          ratingCount.textContent = "Number of reviews: " + book.rating_count;
          details.appendChild(title);
          details.appendChild(author);
          details.appendChild(avgRating);
          details.appendChild(ratingCount);
          listItem.appendChild(details);

          recommendationList.appendChild(listItem);
        });
      } else if (
        data.suggestions &&
        Array.isArray(data.suggestions) &&
        data.suggestions.length > 0
      ) {
        const suggestionHeading = document.createElement("h3");
        suggestionHeading.textContent = `Did you mean?`;
        recommendationList.appendChild(suggestionHeading);
        const suggestionsList = document.createElement("ul");
        data.suggestions.forEach((suggestion) => {
          const suggestionItem = document.createElement("li");
          const suggestionButton = document.createElement("button");
          suggestionButton.textContent = suggestion.title;
          suggestionButton.onclick = () => {
            document.getElementById("bookInput").value = suggestion.title;
            getRecommendations();
          };
          const suggestionDetails = document.createElement("div");
          suggestionDetails.textContent = `Author: ${
            suggestion.author
          }, Average rating: ${suggestion.average_rating.toFixed(
            2
          )}, Number of reviews: ${suggestion.rating_count}`;
          suggestionItem.appendChild(suggestionButton);
          suggestionItem.appendChild(suggestionDetails);
          suggestionsList.appendChild(suggestionItem);
        });
        recommendationList.appendChild(suggestionsList);
      } else if (data.error) {
        const listItem = document.createElement("li");
        listItem.textContent = `Error: ${data.error}`;
        recommendationList.appendChild(listItem);
      } else {
        const listItem = document.createElement("li");
        listItem.textContent = "No recommendations found.";
        recommendationList.appendChild(listItem);
      }
    })
    .catch((error) => {
      recommendationList.innerHTML = `Error fetching recommendations: ${error}`;
    });
}
