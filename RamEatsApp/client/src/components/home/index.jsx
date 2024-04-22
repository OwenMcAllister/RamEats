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
    const [listItems, setListItems] = useState(<b>Loading</b>);

    // Using useEffect for single rendering
    useEffect(() => {
        // Using fetch to fetch the api from 
        // flask server it will be redirected to proxy
        fetch("http://127.0.0.1:5000/api/meal").then((res) =>
            res.json().then((data) => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
                // Setting a data from api
                setdata({
                    selected_items: data.selected_items,
                    total_calories: data.total_calories,
                    total_protein: data.total_protein,
                    total_carbs: data.total_carbs,
                    total_fats: data.total_fats,
                });
                setListItems(data.selected_items.map((item, index) => (
                    <li key={index}>
                    <p>
                        <b>{item[0]}:</b> {item[1]}
                    </p>
                    </li>
                )));
            })
        );
    }, []);

    // if (!loading) {
    //     const listItems = data.selected_items.map((item, index) => (
    //         <li key={index}>
    //         <p>
    //             <b>{item[0]}:</b> {item[1]}
    //         </p>
    //         </li>
    //     ));
    // }

    

    return (
        <>
            <div className='container home-page'>
                {/* Calling a data from setdata for showing */}
                <ul>{listItems}</ul>
                <p>Total Calories: {data.total_calories}</p>
                <p>Total Protein: {data.total_protein}g</p>
                <p>Total Carbs: {data.total_carbs}g</p>
                <p>Total Fats: {data.total_fats}g</p>
            </div>
        </>
    )
}

export default Home