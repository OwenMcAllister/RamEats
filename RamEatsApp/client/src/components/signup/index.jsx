import React, { useState } from 'react';
import './index.scss';
import logo from '../../assets/RamEatsLogo.svg';

const Signup = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/api/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email, // Assuming username is the email for signup
                    password: password,
                    action: 'signup' // Specify the action as 'signup'
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
            console.error('Error during signup:', error.message);
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
                        <label htmlFor='name'>Name</label> <br/>
                        <input type='text' id='name' name='name' required minLength={1} maxLength={20} value={name} onChange={(e) => setName(e.target.value)} /> <br/>
                        <label htmlFor='email'>Email</label> <br/>
                        <input type='email' name='email' id='email' required value={email} onChange={(e) => setEmail(e.target.value)} /> <br/>
                        <label htmlFor='password'>Password</label> <br/>
                        <input type='password' name='password' id='password' required value={password} onChange={(e) => setPassword(e.target.value)} /> <br/>
                        <label htmlFor='confirm_password'>Re-Enter Password</label> <br/>
                        <input type='password' name='confirm_password' id='confirm_password' required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} /> <br/>
                        <button className='login' type='submit'>Sign Up</button>
                    </form>
                </ul>

                <p>Back to <a className='bottom-link' href='/login'>login</a></p>
            </div>
        </>
    );
};

export default Signup;
