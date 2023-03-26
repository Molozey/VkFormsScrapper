import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import LendingPage from "./components/LendingPage";
import Card from "./components/CardQA";


ReactDOM.render(
    // <App />,
    // <LendingPage />,
    <Card num={2} question={'Question'} answer={'Answer'}/>,
  document.getElementById('root')
);
