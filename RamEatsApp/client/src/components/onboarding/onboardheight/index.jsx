import React, { useState } from 'react';
import './index.scss';

const OnBoardHeight = () => {
    const [feet, setFeet] = useState('');
    const [inches, setInches] = useState('');

    const handleNextClick = async (event) => {
        event.preventDefault(); // Prevent form submission and page reload

        try {
            const response = await fetch('http://127.0.0.1:5000/api/onboard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    step: 'height',
                    feet: feet,
                    inches: inches
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
            <div className='onboard-height'>
                <p>Height</p>
                <label htmlFor='feet'>Ft.</label> 
                <input 
                    type='number' 
                    name='feet' 
                    id='feet' 
                    required 
                    value={feet} 
                    onChange={(e) => setFeet(e.target.value)}
                />
                <label htmlFor='inches'>In.</label> 
                <input 
                    type='number' 
                    name='inches' 
                    id='inches' 
                    required 
                    value={inches} 
                    onChange={(e) => setInches(e.target.value)}
                />
                <button className='next' onClick={handleNextClick}>Next</button>
            </div>
        </>
    );
}

export default OnBoardHeight;
