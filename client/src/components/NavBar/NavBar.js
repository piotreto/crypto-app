import {Link, useHistory} from 'react-router-dom';
import react, {useState, useEffect} from 'react';
import './NavBar.css';
import Button from 'react-bootstrap/Button';


export default function NavBar(){
    let history = useHistory();


    const [user, setUser] = useState(null);

    function logout(){
        if(!user) return;
        console.log('loggin out');
        localStorage.setItem('user', null);
        localStorage.setItem('jwt', null);

        alert('Successfully logged out!');
        
        history.push('/');
        window.location.reload();
    }

    useEffect(() =>{
        let isMounted = true;
        
        if(isMounted){
            const userData = localStorage.getItem('user');
            console.log(userData);
            setUser(JSON.parse(userData));
            
        }

        return () => {isMounted = false};
    }, []);

    return(
        <div className="NavBar">
            <Link to='/'>
                <button className="HomeButton">Home</button>
            </Link>

            {!user &&
            <Link to='/login'>
                <button className="LoginButton">Login</button>
            </Link>}

            {!user &&
            <Link to='/register'>
                <button className="LoginButton">Register</button>
            </Link>}

            {user &&
            <Button variant="secondary" onClick={logout}>Log out</Button>}

            {user &&
            <Link to='/wallet'>
                <button className="LoginButton">Wallet</button>
            </Link>}

            {user &&
            <Link to='/trade_history'>
                <button className="LoginButton">Trade History</button>
            </Link>}


        </div>
    );
}
