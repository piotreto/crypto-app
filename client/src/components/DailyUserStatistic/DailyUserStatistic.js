import './DailyUserStatistic.css';
import {useState, useEffect} from 'react';
import axios from 'axios';

export default function DailyUserStatistic(){

    const [dailyStatistics, setDailyStatistics] = useState({});

    useEffect(async () =>{
        const URL = 'http://localhost:4200/info/daily_statistics/';
        const jwt = JSON.parse(localStorage.getItem('jwt'));
        const toSend = {"JWT": jwt};
        try{
            const response = await axios.post(URL, toSend);
            setDailyStatistics(response.data);
        }catch(err){
            console.log(err);
        }
    }, [])


    return(
        <div className="DailyUserStatistic">
            <h1 className="title">Your daily statistics</h1>
            {dailyStatistics.percentage >= 0 && <div>
                <h2 style={{color: 'green'}}>Percentage: {dailyStatistics.percentage}</h2>
                <h2 style={{color: 'green'}}>Difference: {dailyStatistics.difference}</h2>
            </div>}
            {dailyStatistics.percentage < 0 && <div>
                <h2 style={{color: 'red'}}>Percentage: {dailyStatistics.percentage}</h2>
                <h2 style={{color: 'red'}}>Difference: {dailyStatistics.difference}</h2>
            </div>}
        
        </div>
    )
}