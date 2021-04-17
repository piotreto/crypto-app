import React, {useEffect, useState, useRef, createRef} from 'react';
import axios from 'axios';
import Line from 'react-chartjs-2';


function Chart(props){

    const [cryptoData, setCryptoData] = useState({});

    useEffect( async () => {
        let isMounted = true;
        console.log("moj coin " + props.cryptoID);
        const cryptoInfoUrl = 'http://localhost:4200/exchange/' + props.cryptoID.toLowerCase() + '/usd/10';

        try{
            let result = await axios.get(cryptoInfoUrl);
            result = result.data;
            console.log(result);
            setCryptoData({
                labels: result.time,
                datasets: [
                    {
                        label: props.cryptoID,
                        data: result.prices,
                        borderColor: "#3e95cd"
                    }
                ]
            });

        }catch(error){
            if(isMounted){
                setCryptoData({});
            }
        }

        return () => {isMounted = false};
    }, [props]);


    const updateChart = () => {
        
    }

    return(
        <div className="Chart">
            <Line type='line' data={cryptoData}/>
            <p>{props.cryptoID}</p>
        </div>
    )
}

export default Chart;