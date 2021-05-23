import {useState, useEffect, useCallback} from 'react';
import axios from 'axios';
import Transaction from '../Transaction/Transaction';


export default function Wallet(){

    const [walletData, setWalletData] = useState([]);
    const [email, setEmail] = useState('');
    const [tick, refreshState] = useState(0);

    const refreshHandler = useCallback(() => {
        refreshState(tick => tick + 1);
      }, [])

    useEffect(async () =>{
        const URL = 'http://localhost:4200/info/wallet_details/';
        const jwt = JSON.parse(localStorage.getItem('jwt'));
        
        try{
            const toSend = {"JWT": jwt};
            const response = await axios.post(URL, toSend);


            console.log(response.data.wallet_info);
            setWalletData(response.data);
        }catch(err){
            console.log(err);
            return;
        }
    }, [tick]);

    return(
        <div className="Wallet">
            {walletData.wallet_info !== undefined && <div>
                <p>{walletData.dollars} $</p>
                <div className="cryptoWrapper">
                    {walletData.wallet_info.map((crypto, i) =>{
                        return(
                            <div key={i}>
                                {crypto.cryptoID}: {crypto.amount}
                            </div>
                        )
                    })}
                </div>
            </div>}
            <Transaction refreshHandler = {refreshHandler}/>
        </div>
    );
}