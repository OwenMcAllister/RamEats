import React, { useState } from 'react';
import './index.scss';

const OnBoardGoal = () => {
    const [fitgoal, setGoal] = useState('');
    const [submitted, setSubmitted] = useState(false);

    const handleGoalSelection = (selectedGoal) => {
        setGoal(selectedGoal);
    };

    const handleSubmit = async () => {
        if (!fitgoal) {
            console.error('Goal has not been selected');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/api/onboard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    step: 'fitnessGoal',
                    goal: fitgoal,
                }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log('Goal data sent successfully:', data);

            if (data.redirect){
                window.location.href = data.redirect;
            }
            
            setSubmitted(true); // Set submitted state to true after successful submission
        } catch (error) {
            console.error('Error sending goal data:', error.message);
            // Handle error, e.g., display error message to user
        }
    };

    return (
        <>
            <p>Biological Sex</p>
            <button className='fitgoal' type="button" onClick={() => handleGoalSelection('gain')}>Gain Weight</button>
            <button className='fitgoal' type="button" onClick={() => handleGoalSelection('lose')}>Lose Weight</button>
            <button className='fitgoal' type="button" onClick={() => handleGoalSelection('maintain')}>Maintain Weight</button>
            {!submitted && (
                <button className='next' type="button" onClick={handleSubmit}>Next</button>
            )}
            {submitted && (
                <p>Submitted successfully!</p>
                // You can replace this with any UI indicating successful submission
            )}
        </>
    );
}

export default OnBoardGoal;
