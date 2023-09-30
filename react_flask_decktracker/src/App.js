import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import ReactDOM from "react-dom";


class App extends React.Component {
  constructor() {
    super();
    this.state = { data: [] };
  }

  async componentDidMount() {
    await new Promise( res => setTimeout(res, 10000) );
    const response = await fetch('http://localhost:5000/testing');
    const json = await response.json();
    console.log(json);
    this.setState({data: json.total_games});
  }

  render() {
    this.componentDidMount(); 
    return <h1>{this.state.data}</h1>;
  }

  // useEffect(() => {
  //   fetch('/api').then(res => res.json()).then(data => {
  //     setCurrentDb(data.toString());
  //   })
  // }, []);
}

export default App;

// ReactDOM.render(<App />, document.getElementById("app"));
