'use strict';
function Reviews() {
  const [reviews, setReviews] = React.useState([]);

  // Modify the current state by setting the new data to
  // the response from the backend
  const recipeId = document.getElementById('recipe-id').innerHTML
  React.useEffect(()=>{
    fetch(`http://localhost:5001/reviews/${recipeId}`,{
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json())
    .then(response => setReviews(response))
    .catch(error => console.log(error))

  },[])

  return (
    <div className="container pl-0 mt-20">
      <div className="row">
      <h5 className="color-brown">Reviews</h5>
      {reviews.map(rev => <div key="rev" className="card m-20 font-18 p-10 m-10">
                            <p className="underline-style">{rev.user_name}</p>
                            <p>Rating: {rev.rating}/5</p>
                            <p>Review: {rev.review}</p>
                          </div>)}
      </div>
    </div>
  );
}

ReactDOM.render(<Reviews />, document.getElementById('test-reviews'));
