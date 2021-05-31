import React, {useEffect, useState, useRef, createRef} from 'react';
import axios from 'axios';
import Line from 'react-chartjs-2';
import Slider from '@material-ui/core/Slider';
import './Chart.css';



function Chart(props){

    const [cryptoData, setCryptoData] = useState({});
    const [daysRange, setDaysRange] = useState(10);

    useEffect( async () => {
        let isMounted = true;
        console.log("moj coin " + props.cryptoID);
        const cryptoInfoUrl = 'http://localhost:4200/exchange/' + props.cryptoID.toLowerCase() + '/usd/' + daysRange;

        try{
            let result = await axios.get(cryptoInfoUrl);
            result = result.data;
            console.log(result);
            if(isMounted){
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
            }

        }catch(error){
            if(isMounted){
                setCryptoData({});
            }
            alert(error);
        }

        return () => {isMounted = false};
    }, [props, daysRange]);


    const updateChart = () => {
        
    }

    return(
        <div className="Chart">
            <Line type='line' data={cryptoData}/>
            <div className="mySlider">
                <p>Choose days range</p>
                <Slider 
                className="mySlider"
                value={daysRange} 
                onChange={(e, value) => setDaysRange(value)} 
                aria-labelledby="continuous-slider"
                valueLabelDisplay="auto"
                min={1}
                max={10}
                marks/>
            </div>
        </div>
    )
}

export default Chart;