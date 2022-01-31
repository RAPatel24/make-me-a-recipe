'use strict';
const ReviewData = [
    {
      recipeId: 1,
      review: "some review",
      rating: 5
    },
    {
        recipeId: 2,
        review: "some review",
        rating: 5
      },
  ];
  function Review(props) {
    return (
      <div className="card">
        <h2>Review: {props.review}</h2>
        <p>Rating: {props.rating}  </p>
      </div>
    );
  }
  function ReviewContainer() {
    const reviewList = [];
  
    for (const value of ReviewData) {
      reviewList.push(
        <Review
          review={value.review}
          rating={value.rating}
          key={value.recipeId}
        />
      );
    }
  
    return <React.Fragment>{reviewList}</React.Fragment>;
  }
ReactDOM.render(<ReviewContainer />, document.querySelector('#review'));
