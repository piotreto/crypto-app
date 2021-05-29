import './Transaction.css';
import {useState, useEffect, useCallback} from 'react';
import axios from 'axios';
import TradeHistory from '../TradeHistory/TradeHistory';


export default function Transaction(props){

    const [buy, setBuy] = useState(0);
    const [sell, setSell] = useState(0);
    const [cryptoList, setCryptoList] = useState([]);
    const [buyChoice, setBuyChoice] = useState('bitcoin');
    const [sellChoice, setSellChoice] = useState('bitcoin');

    const handleBuy = async (e) =>{
        e.preventDefault();
        const jwt = getJWT();

        const number = parseFloat(buy);
        const value = replaceDot(buy);
        const URL = 'http://127.0.0.1:4200/transaction/buy/' + buyChoice + '/' + value + '/';
        try{
            const response = await axios.post(URL, jwt);
            alert("You bought " + buyChoice + " for " + number + "$");
            props.refreshHandler();
        }catch(err){
            alert(err.response.data.error);
        }
    }

    const handleSell = async (e) =>{
        e.preventDefault();
        const jwt = getJWT();

        const number = parseFloat(sell);
        const value = replaceDot(sell);
        const URL = 'http://127.0.0.1:4200/transaction/sell/' + sellChoice + '/' + value + '/';
        try{
            const response = await axios.post(URL, jwt);
            alert("You sold " + number + " of " + sellChoice);
            props.refreshHandler(); 
        }catch(err){
            alert(err.response.data.error);
        }
    }

    const getJWT = () =>{
        const jwt = JSON.parse(localStorage.getItem('jwt'));
        return {"JWT": jwt};
    }

    const replaceDot = (number) =>{
        if(! isNaN(parseFloat(number))){
            return ('' + parseFloat(number)).replace('.', 'a');
        }else{
            return -1;
        }
    }

    useEffect(async () =>{
        try{
            const cryptoListURL = 'http://localhost:4200/exchange/list';
            const result = await axios.get(cryptoListURL);

            setCryptoList(result.data.cryptoList);

        }catch(err){
            console.log(err)
        }
    }, []);

    return(
        <div className="Transaction">
            <div className="buy">
                <form>
                    <label>Buy</label>
                    <select name="cryptoChoice" onChange={(e) =>{
                        setBuyChoice(e.target.value);
                    }}>
                        {cryptoList.map((cryptoName, index) => {
                            return <option value={cryptoName} key={index}>{cryptoName.toUpperCase()}</option>
                        })}
                    </select><br></br>
                    Buy {buyChoice} for 
                    <input type="text" value={buy} onChange={(e) => setBuy(e.target.value)}></input>$
                    <button value="buy" onClick={(e) => handleBuy(e)}>BUY</button>
                </form>
            </div>   

            <div className="sell">
                <form>
                    <label>Sell</label>
                    <select name="cryptoChoice" onChange={(e) =>{
                        setSellChoice(e.target.value);
                    }}>
                        {cryptoList.map((cryptoName, index) => {
                            return <option value={cryptoName} key={index}>{cryptoName.toUpperCase()}</option>
                        })}
                    </select><br></br>
                    Sell
                    <input type="text" value={sell} onChange={(e) => setSell(e.target.value)}></input> {sellChoice} for $
                    <button value="sell" onClick={(e) => handleSell(e)}>SELL</button>
                </form>
            </div>
        </div>
    )
}