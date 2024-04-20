import React, { useState } from 'react';
import './index.scss';

const OnBoardTimeline = () => {
    const [days, setDays] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('http://127.0.0.1:5000/api/onboard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    step: 'timeline',
                    timeline: days,
                }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log('Timeline data sent successfully:', data);
            // Redirect or perform other actions upon successful data submission
        } catch (error) {
            console.error('Error sending timeline data:', error.message);
            // Handle error, e.g., display error message to user
        }
    };

    return (
        <>
            <p>How long do you have to complete this goal?</p>
            <form onSubmit={handleSubmit}>
                <label htmlFor='days'>Days</label> 
                <input 
                    type='number' 
                    name='days' 
                    id='days' 
                    value={days} 
                    onChange={(e) => setDays(e.target.value)} 
                    required 
                />
                <button className='next' type='submit'>Next</button>
            </form>
        </>
    );
}

export default OnBoardTimeline;
