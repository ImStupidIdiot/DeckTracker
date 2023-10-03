import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import ReactDOM from "react-dom";


class App extends React.Component {
  constructor() {
    super();
    this.state = { total_games: 0, total_wins: 0, uids: ['809458646', '859401792', '812310683', '878964522', '622963441', '860236862', '606415530', '624516438', '612358049', '649486104', '646346491', '626398278', '704822600', '819042492', '603200036'], mounted: false};
  }

  async componentDidMount() {
    if (!this.state.mounted) {
      console.log('start')
      this.setState({mounted: true}); 
      while(true) {
        for (let i = 0; i < this.state.uids.length; i++) {
          const response = await fetch('http://localhost:5000/testing/' + this.state.uids[i]);
          // for testing later: 646346491
          const json = await response.json();
          this.setState({total_games: json.total_games, total_wins: json.total_wins});
          for (var key in json) {
            if (key.includes('[')) {
              this.setState({[key]: [Math.round(json[key]['wins'] / json[key]['total_games'] * 100), json[key]['total_games']]});
            }
          }
          for (var key in json.opponents) {
            if (key.includes('[')) {
              this.setState({[key + 'opp']: [Math.round(json.opponents[key]['wins'] / json.opponents[key]['total_games'] * 100), json.opponents[key]['total_games']]});
            }
          }
        }
        var sleep = await new Promise(resolve => setTimeout(resolve, 30000));
      }
    }
  }

  // is_meta(str) {
  //   return str in meta_list;
  // }


  render() {
    var build = "";
    var buildList = [];
    for (var key in this.state) {
      if (key.includes('[')) {
        buildList.push([key, this.state[key][0], this.state[key][1]]);
      }
    }
    buildList = buildList.sort((tuple1, tuple2) => tuple2[2] - tuple1[2]);
    for (let i = 0; i < buildList.length; i++) {
        var tuple = buildList[i];
        build += tuple[0] + ': ' + tuple[1] + '% over ' + tuple[2] + ' games';
        build += '\n    '; 
    }
    return <pre><h1> Currently Tracking UIDS: {this.state.uids.toString()} <br/> Total Games: {this.state.total_games} <br/> Total Wins: {this.state.total_wins} <br/> Winrate: {this.state.total_wins / this.state.total_games * 100}% <br/> Winrate by Deck: <br/>    {build}
    </h1></pre>;
  }

  // useEffect(() => {
  //   fetch('/api').then(res => res.json()).then(data => {
  //     setCurrentDb(data.toString());
  //   })
  // }, []);
}

export default App;

// ReactDOM.render(<App />, document.getElementById("app"));
