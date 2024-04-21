import React, { useState } from 'react';
import './index.scss';

const OnBoardCalories = () => {
    const [calories, setCalories] = useState('');

    const handleNextClick = async (event) => {
        event.preventDefault(); // Prevent form submission and page reload

        try {
            const response = await fetch('http://127.0.0.1:5000/api/onboard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    step: 'activityLevel',
                    activityLevel: calories,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to send activity data.');
            }

            
            const data = await response.json();

            if (data.redirect){
                window.location.href = data.redirect;
            }
            
            console.log('Activity data sent successfully.');
        } catch (error) {
            console.error('Error sending activity data:', error.message);
            // Handle error
        }
    };

    return (
        <>
            <p>Approximately how many calories do you burn per day?</p>
            <label htmlFor='Calories'>kcal.</label> 
            <input 
                type='number' 
                name='calories' 
                id='calories'
                value={calories} 
                onChange={(e) => setCalories(e.target.value)} 
                required 
            />
            <button className='next' onClick={handleNextClick}>Next</button>
        </>
    );
}

export default OnBoardCalories;
