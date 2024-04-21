import React, { useState } from 'react';
import './index.scss';

const OnBoardAge = () => {
    const [age, setWeight] = useState('');

    const handleNextClick = async (event) => {
        event.preventDefault(); // Prevent form submission and page reload

        try {
            const response = await fetch('http://127.0.0.1:5000/api/onboard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    step: 'age',
                    age: age,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to send height data.');
            }

            
            const data = await response.json();

            if (data.redirect){
                window.location.href = data.redirect;
            }
            
            console.log('Height data sent successfully.');
        } catch (error) {
            console.error('Error sending height data:', error.message);
            // Handle error
        }
    };

    return (
        <>
            <p>Age</p>
            <label htmlFor='age'>years.</label> 
            <input 
                type='number' 
                name='age' 
                id='age'
                value={age} 
                onChange={(e) => setWeight(e.target.value)} 
                required 
            />
            <button className='next' onClick={handleNextClick}>Next</button>
        </>
    );
}

export default OnBoardAge;
