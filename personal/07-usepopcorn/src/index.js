import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
// import StarRating from './Starrating';

// function Test() {
//   const [movieRating, setMovieRating] = useState(0);
//   return <div>
//     <StarRating maxRating={10} color='blue' onSetRating={setMovieRating} />
//     <p>This movie was rated {movieRating} stars</p>
//   </div>
// }

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
    {/* <StarRating maxRating="abcd" size={20} messages={["Terrible", "Bad", "Ok", "Good", "Amazing"]} />
    <StarRating maxRating={10} />
    <StarRating size={24} color='red' className="test" defaultRating={3} />
    <Test /> */}
  </React.StrictMode>
);
