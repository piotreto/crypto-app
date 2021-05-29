import './TradeHistory.css';
import {useState, useEffect } from 'react';
import axios from 'axios';


export default function TradeHistory(){

    const [history, setHistory] = useState([]);

    useEffect(async () => {

        const URL = 'http://localhost:4200/info/trade_history/';
        const JWT = getJWT();

        try{
            const response = await axios.post(URL, JWT);

            console.log(response.data.trades);
            setHistory(response.data.trades);
        }catch(err){
            alert(err);
            return;
        }

    }, []);

    const getJWT = () =>{
        const jwt = JSON.parse(localStorage.getItem('jwt'));
        return {"JWT": jwt};
    }

    return(
        <div className="TradeHistory">
            {history.map((trade, i) => {
                return(
                    <div key={i} className="trade">
                        {trade.type == "BUY" && <div key={i}>
                            <h1 style={{color: 'green'}}>{trade.type} {trade.cryptoID}</h1>
                            <p>{trade.amount * trade.currentPrice}$ ➔ {trade.amount}{trade.cryptoID}</p>
                        </div>}

                        {trade.type == "SELL" &&<div key={i}>
                            <h1 style={{color: 'red'}}>{trade.type} {trade.cryptoID}</h1>
                            <p>{trade.amount}{trade.cryptoID} ➔ {trade.amount * trade.currentPrice}$</p>
                        </div>}
                    </div>
                )
            })}
        </div>
    )
}