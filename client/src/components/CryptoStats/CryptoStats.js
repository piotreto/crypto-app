import {useState, useEffect} from 'react';
import axios from 'axios';

export default function CryptoStats(){

    const [stats, setStats] = useState([]);

    useEffect(async () => {
    
        const URL = 'http://localhost:4200/info/daily_crypto_statistics/';
        const JWT = getJWT();

        

        const response = await axios.post(URL, JWT);

        setStats(response.data.stats);
        console.log(response.data.stats);

    }, []);

    const getJWT = () =>{
        const jwt = JSON.parse(localStorage.getItem('jwt'));
        return {"JWT": jwt};
    }

    return (
        <div className="CryptoStats">
            <h2>Last 24h</h2>
            {stats.map((stat,i) =>{
                return(
                <div key={i}>
                    {stat.percentage < 0 &&
                    <div>
                        <h1 style={{color: 'red'}}>
                            {stat.cryptoID}
                        </h1>
                        <p style={{color: 'red'}}>{stat.percentage}%</p>
                    </div>}

                    {stat.percentage >= 0 &&
                    <div>
                        <h1 style={{color: 'green'}}>
                            {stat.cryptoID}
                        </h1>
                        <p style={{color: 'green'}}>{stat.percentage}%</p>
                    </div>}

                </div>
                )
            })}
        </div>
    )
}