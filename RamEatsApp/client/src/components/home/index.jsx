import { useEffect, useState } from 'react';
import './index.scss'

const Home = () => {
    const [data, setdata] = useState({
        selected_items: "",
        total_calories: 0,
        total_protein: 0,
        total_carbs: 0,
        total_fats: 0,
    });

    // Using useEffect for single rendering
    useEffect(() => {
        // Using fetch to fetch the api from 
        // flask server it will be redirected to proxy
        fetch("http://127.0.0.1:5000/api/meal").then((res) =>
            res.json().then((data) => {
                // Setting a data from api
                setdata({
                    selected_items: data.selected_items,
                    total_calories: data.total_calories,
                    total_protein: data.total_protein,
                    total_fats: data.total_fats,
                });
            })
        );
    }, []);

    return (
        <>
            <div className='container home-page'>
                {/* Calling a data from setdata for showing */}
                <p>{data.selected_items}</p>
                <p>{data.total_calories}</p>
                <p>{data.total_protein}</p>
                <p>{data.total_fats}</p>
            </div>
        </>
    )
}

export default Home