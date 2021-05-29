import react, {useEffect, useState} from 'react';
import Chart from '../Chart/Chart';
import axios from 'axios';
import {Route, BrowserRouter as Router, Switch} from 'react-router-dom';
import CryptoStats from '../CryptoStats/CryptoStats';



function ChartWrapper(){

    const [cryptoList, setCryptoList] = useState([]);
    const [cryptoChoice, setCryptoChoice] = useState('bitcoin');


    useEffect(() =>{
        let isMounted = true;
        const cryptoListUrl = 'http://localhost:4200/exchange/list';


        axios.get(cryptoListUrl)
        .then(result => {
            if(isMounted){
                setCryptoList(result.data.cryptoList);
            }
        })
        .catch(error =>{
            if(isMounted) setCryptoList([]);
            console.log(error.message);
        });

        return () => {isMounted = false};
    }, []);

    
    


    return(
        <div className="ChartWrapper">
            <form>
                <label>Cryptos</label>
                <select name="cryptoChoice" onChange={(e) =>{
                    setCryptoChoice(e.target.value);
                }}>
                    {cryptoList.map((cryptoName, index) => {
                        return <option value={cryptoName} key={index}>{cryptoName.toUpperCase()}</option>
                    })}
                </select>
                <Chart cryptoID={cryptoChoice}/>
            </form>
        
            

        </div>
    )
}

export default ChartWrapper;