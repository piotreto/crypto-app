import react ,{useState} from 'react';
import { Form, Button } from 'react-bootstrap';
import './Login.css';
import axios from 'axios';
import {useHistory} from 'react-router-dom';


export default function Login(){

    let history = useHistory();

    const [formEmail, setFormEmail] = useState('');
    const [formPassword, setFormPassword] = useState('');


    async function handleSubmit(e){
        e.preventDefault();

        const form = e.currentTarget;

        if(form.checkValidity() === false){
            alert('Enter valid values');
            return;
        }

        const toSend ={
            email: formEmail,
            password: formPassword
        };

        //Let the backed verify if the values are valid
        try{
            const URL = 'http://localhost:4200/auth/login/';

            const response = await axios.post(URL, toSend);

            setFormEmail('');
            setFormPassword('');

            console.log(response.data);
            alert('Logged successfully!');

            localStorage.setItem('user', JSON.stringify(response.data.email));
            localStorage.setItem('jwt', JSON.stringify(response.data.JWT));

        
            history.push('/');
            window.location.reload();
            
        }catch(err){
            alert(err.response.data.error);
            return;
        }

    }


    return (
        <div className="Login">
            <Form className="myForm" onSubmit={handleSubmit}>

                <Form.Group controlId="formEmail">
                    <Form.Label className="myLabel">Email</Form.Label>
                    <Form.Control type="email" value={formEmail} onChange={(e) => setFormEmail(e.target.value)} required/>
                </Form.Group>

                <Form.Group controlId="formPassword">
                    <Form.Label className="myLabel">Password</Form.Label>
                    <Form.Control type="password" value={formPassword} onChange={(e) => setFormPassword(e.target.value)} required/>
                </Form.Group>

                <Button className="submitButton" variant="primary" type="submit">
                    Log In
                </Button>

            </Form>
        </div>
    )
}