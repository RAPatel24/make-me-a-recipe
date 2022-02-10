'use strict';
function ReviewCount() {
  const [reviewcount, setReviewCount] = React.useState([]);

  // Modify the current state by setting the new data to
  // the response from the backend
  const recipeId = document.getElementById('recipe-id').innerHTML
  React.useEffect(()=>{
    fetch(`http://localhost:5001/reviewcount/${recipeId}`,{
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json())
    .then(response => setReviewCount(response))
    .catch(error => console.log(error))

  },[])

  return (
    <a href="#test-reviews" className="color-cadetblue"> {reviewcount} reviews</a>
  );
}

ReactDOM.render(<ReviewCount />, document.getElementById('review-count'));