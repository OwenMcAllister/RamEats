import React, { useState } from 'react';
import './index.scss';

const OnBoardMF = () => {
    const [gender, setGender] = useState('');
    const [submitted, setSubmitted] = useState(false);

    const handleGenderSelection = (selectedGender) => {
        setGender(selectedGender);
    };

    const handleSubmit = async () => {
        if (!gender) {
            console.error('Gender has not been selected');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/api/onboard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    step: 'gender',
                    gender: gender,
                }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log('Gender data sent successfully:', data);

            if (data.redirect){
                window.location.href = data.redirect;
            }
            
            setSubmitted(true); // Set submitted state to true after successful submission
        } catch (error) {
            console.error('Error sending gender data:', error.message);
            // Handle error, e.g., display error message to user
        }
    };

    return (
        <>
            <p>Biological Sex</p>
            <div>
                <button className='gender' type="button" onClick={() => handleGenderSelection('Male')}>Male</button>
                <button className='gender' type="button" onClick={() => handleGenderSelection('Female')}>Female</button>
            </div>
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

export default OnBoardMF;
