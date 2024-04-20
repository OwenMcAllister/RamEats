import React, { useState } from 'react';
import './index.scss';
import logo from '../../assets/RamEatsLogo.svg';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        try {
            const response = await fetch('http://127.0.0.1:5000/api/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email, // Assuming username is the email for login
                    password: password,
                    action: 'login' // Specify the action as 'login'
                }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();

            if (data.redirect){
                window.location.href = data.redirect;
            }

        } catch (error) {
            console.error('Error during login:', error.message);
            // Handle error, e.g., display error message to user
        }
    };

    return (
        <>
            <div className='login-page'>
                <ul>
                    <img src={logo} alt='Logo' height={'50px'}/> 
                    <h1>RamEats</h1> 
                    <form onSubmit={handleSubmit}>
                        <label htmlFor='email'>Email</label> 
                        <input type='email' name='email' id='email' required value={email} onChange={(e) => setEmail(e.target.value)} /> 
                        <label htmlFor='password'>Password</label> 
                        <input type='password' name='password' id='password' required value={password} onChange={(e) => setPassword(e.target.value)} /> 
                        <button className='login' type='submit'>Login</button>
                        <a className='newPass'>Forgot password?</a>
                    </form>
                </ul>

                <p>Don't have an account? <a className='signUp'>Sign Up</a></p>
            </div>
        </>
    );
};

export default Login;
