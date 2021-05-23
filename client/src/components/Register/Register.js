
import react ,{useState} from 'react';
import { Form, Button } from 'react-bootstrap';
import './Register.css';
import axios from 'axios';
import {useHistory} from 'react-router-dom';


export default function Register(){
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

        const toSend = {
            email: formEmail,
            password: formPassword 
        };
        
        //Let the backend validate if the values are valid
        try{
            const URL = 'http://localhost:4200/auth/register/';

            const response = await axios.post(URL, toSend);
            setFormEmail('');
            setFormPassword('');

            alert('Registration successful, you can now log in!');

            history.push('/login');
        }catch(err){
            alert(err.response.data.error);
            return;
        };

        

    }


    return(
        <div className="Register">
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
                    Sign Up
                </Button>
            </Form>
        </div>
    )
}