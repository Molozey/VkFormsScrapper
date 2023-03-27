import React from 'react';
import './App.css';
import LendingPage from "./components/LendingPage";
import CardQA from "./components/CardQA";
import ComplexUsers from "./components/ComplexUsers";
import ShowSeveralCards from "./components/ShowSeveralCards";
function App() {
  return (
    <div className="App">
        <h1>Nigger</h1>
        <h1 color={"red"}>Dynamic User</h1>
        <h4>EMPTY</h4>
        <ComplexUsers number_of_users={1}/>
        <ShowSeveralCards number_of_forms={10}/>
        {/*<CardQA num={1} question={"trst"} answer={"test_abs"}></CardQA>*/}
        {/*<LendingPage></LendingPage>*/}
    </div>
  );
}

export default App;
