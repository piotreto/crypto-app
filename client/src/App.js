import './App.css';
import ChartWrapper from './components/ChartWrapper/ChartWrapper';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import NavBar from './components/NavBar/NavBar';
import Wallet from './components/Wallet/Wallet';
import TradeHistory from './components/TradeHistory/TradeHistory';

function App() {
  return (
    <div className="App">
      <Router>

        <NavBar/>

        <Switch>

          <Route path='/' exact={true}>
            <ChartWrapper/>
          </Route>

          <Route path='/login' exact={true}>
            <Login/>
          </Route>

          <Route path='/register' exact={true}>
            <Register/>
          </Route>

          <Route path='/wallet' exact={true}>
            <Wallet/>
          </Route>

          <Route path='/trade_history' exact={true}>
            <TradeHistory/>
          </Route>

        </Switch>
      </Router>
    </div>
  );
}
export default App;
