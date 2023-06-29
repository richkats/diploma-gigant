import React, {Component, useState, useEffect, useRef} from 'react';
import Header from "../components/Header";
import "../ads.css"
import { For } from 'react-loops'
import { Link } from 'react-router-dom';
import {Route, Router, Routes} from "react-router";
import Description from "./Description";
import {useCookies} from "react-cookie";
import {type} from "@testing-library/user-event/dist/type";


const BACKEND_URL = "http://10.13.13.25:8000";
function City(props) {
    return <p className={"text_name"}>{props.name}</p>;
}
function Band(props) {
    return <div className={"band_name"}>{props.name}</div>;
}
function Dates(props) {
    return <p>{props.name}</p>;
}
function Genre(props) {
    return <p className={"genre_background"}>{props.name}</p>;
}
function Photo(props) {
    return <img className={"photo"} src={props.photo}/>;
}
function Ad(props){
    function getNormalDate()
    {
        const date = new Date(props.date);
        const dateFormat = date.getDate()+
            "/"+(date.getMonth()+1)+
            "/"+date.getFullYear();
        return dateFormat;
    }

    return(
        <>
            {/*<div className={"band_name"} style={{textAlign: "center", alignSelf: "center", paddingTop: "10px", paddingLeft: "0"}}>{props.type==='venue_ad' ? 'Площадка' : 'Исполнитель'}</div>*/}
        <div className={"wrapper_ad_1"}>
            <div className={"wrapper_column_text"}>
                <Band name={props.name} />
                <City name={props.city} />
                <div className={"text_name"}>{props.requirements[0].name}: {props.requirements[0].value}</div>
                <div className={"text_name"}>
                    Свободные даты:
                    <Dates name={getNormalDate()}/>
                </div>
            </div>
            <Photo photo={props.photo}/>
        </div>
        <div className={"genre_text"}>
            {props.genres.map((item) => (
                <Genre key={item} name={item} />
            ))}
        </div>
        </>
    )
}

function Window(){
    const [advertisements, setAdvertisements] = useState([]);
    const [cookies, setCookie] = useCookies(['ad_id', 'type'])
    const [isLoading, setIsLoading] = useState(true)
    const [isEntered, setIsEntered] = useState([]);
    // const [isEnteredVenue, setIsEnteredVenue] = useState(false)
    // const [isEnteredArtist, setIsEnteredArtist] = useState(false)
    const [isClickedVenue, setIsClickedVenue] = useState(false)
    const [isClickedArtist, setIsClickedArtist] = useState(false)
    const [isEnteredFilter, setIsEnteredFilter] = useState(false);
    const [isClickedFilter, setIsClickedFilter] = useState(false);
    const isFirstRender = useRef(true);
    const [genresFilter, setGenresFilter] = useState([]);
    const [isEnteredText, setIsEnteredText] = useState([]);
    const [clickedGenres, setClickedGenres] = useState([]);
    const handleMouseEnter = (index) => {
        const updatedIsEntered = [...isEntered];
        updatedIsEntered[index] = true;
        setIsEntered(updatedIsEntered);
    };
    const handleMouseLeave = (index) => {
        const updatedIsEntered = [...isEntered];
        updatedIsEntered[index] = false;
        setIsEntered(updatedIsEntered);
    };
    const handleMouseEnterText = (index) => {
        const updatedIsEnteredText = [...isEnteredText]
        updatedIsEnteredText[index] = true
        setIsEnteredText(updatedIsEnteredText)
    }
    const handleClickGenre = (text) => {
        if (clickedGenres.includes(text)) {
            const updatedValues = clickedGenres.filter((value) => value !== text);
            setClickedGenres(updatedValues);
        } else {
            const updatedValues = [...clickedGenres, text.toLocaleString()];
            setClickedGenres(updatedValues);
        }
    };
    const handleMouseLeaveText = (index) => {
        const updatedIsEnteredText = [...isEnteredText]
        updatedIsEnteredText[index] = false
        setIsEnteredText(updatedIsEnteredText)
    }

    const handleMouseEnterFilter = () => {
        setIsEnteredFilter(true)
    }
    const handleMouseLeaveFilter = () => {
        setIsEnteredFilter(false)
    }
    const handleMouseDownFilter = () => {
      setIsClickedFilter(!isClickedFilter)
    }

    function responseJSON(json){
        setAdvertisements(json)
        console.log(json)
    }
    function responseJSONGenres(json){
        setGenresFilter(json)
        console.log(json)
    }
    useEffect(() => {
        if (isFirstRender.current) {
            isFirstRender.current = false;
            fetch(BACKEND_URL + "/all_ads/")
                .then((res) => res.json())
                .then((json) => responseJSON(json))
            fetch(BACKEND_URL + "/genres/")
                .then((res) => res.json())
                .then((json) => responseJSONGenres(json))
        }}, []);
    if(advertisements.length && genresFilter.length && isLoading){
        setIsLoading(false)
    }
    function openAd(ad_id, type)
    {
        setCookie('type', type, {path: '/'});
        setCookie('ad_id', ad_id, { path: '/' });
        window.location.replace("/Description");
    }

    return (
        <div>
            <div style={{backgroundColor: "white"}}>
                <div className={"filter container"}>
                    <div className={isClickedFilter ? "filter_box_clicked text_description_regular" : (isEnteredFilter ? "filter_box_entered text_description_regular" : "filter_box text_description_regular") } onMouseEnter={handleMouseEnterFilter} onMouseLeave={handleMouseLeaveFilter} onClick={handleMouseDownFilter}>
                        <svg id="Group_35" data-name="Group 35" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 66.58 57.184">
                            <path id="Path_16" data-name="Path 16" d="M-170.816-274.868q7.167,0,14.334,0c1.011,0,2.023.02,3.032-.024.527-.023,1.044.071,1.571.034.56-.04,1.125-.009,1.688-.009h5.025c.667,0,.647-.008.877-.624a8.861,8.861,0,0,1,7.527-6.133,9,9,0,0,1,9.806,6.368.461.461,0,0,0,.519.393c1.524-.011,3.048.006,4.572-.011.387,0,.536.109.529.512q-.031,1.771,0,3.542c.007.409-.151.512-.532.508-1.455-.016-2.911.009-4.366-.014a.683.683,0,0,0-.79.553,9.08,9.08,0,0,1-8.732,6.294,9.07,9.07,0,0,1-8.531-6.292.687.687,0,0,0-.785-.557q-20.966.016-41.932.009a3.9,3.9,0,0,0-.412,0c-.349.037-.48-.083-.473-.459.024-1.235.019-2.471,0-3.707,0-.309.076-.394.39-.393Q-179.158-274.861-170.816-274.868Zm39.725,2.284a4.573,4.573,0,0,0-4.529-4.585,4.615,4.615,0,0,0-4.608,4.551,4.578,4.578,0,0,0,4.533,4.589A4.563,4.563,0,0,0-131.091-272.583Z" transform="translate(187.916 301.197)"/>
                            <path id="Path_17" data-name="Path 17" d="M-136.028-34.24c-4.64,0-9.281.006-13.921-.008a.636.636,0,0,0-.723.517,8.825,8.825,0,0,1-6.667,6.088,8.747,8.747,0,0,1-8.4-2.412,8.587,8.587,0,0,1-2.277-3.753.533.533,0,0,0-.615-.437q-6.013.013-12.026.005c-2.292,0-4.585-.007-6.877.006-.363,0-.5-.083-.494-.48.023-1.235.014-2.471-.012-3.706-.008-.364.192-.366.44-.366h9.761c3.031,0,6.062-.006,9.093.009a.67.67,0,0,0,.764-.53,8.843,8.843,0,0,1,7.366-6.208,8.7,8.7,0,0,1,7.288,2.177,8.784,8.784,0,0,1,2.684,4.156c.113.367.343.4.653.4q3.913-.007,7.825,0h19.852c.927,0,.831-.042.832.812q0,1.524,0,3.048c0,.686,0,.686-.667.686Zm-23.343,2.291a4.58,4.58,0,0,0,4.619-4.534,4.613,4.613,0,0,0-4.525-4.6,4.589,4.589,0,0,0-4.635,4.484A4.57,4.57,0,0,0-159.371-31.949Z" transform="translate(188.054 84.575)"/>
                            <path id="Path_18" data-name="Path 18" d="M-141.742-506.927h-17.875c-.59,0-1.181.019-1.77-.006a.515.515,0,0,0-.583.439,9.022,9.022,0,0,1-3.236,4.6,8.926,8.926,0,0,1-4.538,1.782,8.741,8.741,0,0,1-4.73-.795,8.915,8.915,0,0,1-4.838-5.485.667.667,0,0,0-.777-.548c-2.553.019-5.107,0-7.661.02-.388,0-.442-.117-.438-.462q.022-1.914-.021-3.829c-.007-.31.17-.219.313-.219,2.595,0,5.19-.011,7.784.013a.706.706,0,0,0,.808-.573,8.9,8.9,0,0,1,7.664-6.237,8.479,8.479,0,0,1,5.544,1.167,8.936,8.936,0,0,1,4.078,5.07.716.716,0,0,0,.825.572q19.358-.018,38.716-.009a3.175,3.175,0,0,0,.37,0c.362-.042.48.113.475.471q-.024,1.812,0,3.624c0,.328-.1.414-.426.413q-6.692-.017-13.384-.009Zm-24.341-2.226a4.636,4.636,0,0,0-4.61-4.613,4.584,4.584,0,0,0-4.522,4.6,4.559,4.559,0,0,0,4.57,4.583A4.62,4.62,0,0,0-166.083-509.153Z" transform="translate(188.209 518.3)"/>
                        </svg>
                        Фильтры
                    </div>
                    {isLoading ? (<></>
                    ): <div className={isClickedFilter ? 'popup' : "popup_hidden"}>{genresFilter.map((item, index) => (
                        <div key={index} className={isEnteredText[index] || clickedGenres.includes(item["name"]) ? 'text_description_regular_bold' : 'text_description_regular_genre'} onMouseEnter={() => handleMouseEnterText(index)} onMouseLeave={() => handleMouseLeaveText(index)} onClick={() => handleClickGenre(item["name"])}>
                            {item["name"]}
                        </div>
                    ))}</div>}
                </div>
            </div>

            {isLoading ? (
                    <div className={"loading"}>
                <div className="load"/>
                    </div>
            ) : (<>
            <div className={"parent-container"}>
                <div className={"title"}>
                    <p className={"title_text"}>Объявления исполнителей</p>
                </div>
                <div className={"wrapper"}>
                    {advertisements.map((item, index) => (
                        <div
                            key={item["ad_id"]}
                            className={item["type"] === "artist_ad" && (clickedGenres.every((element) => item['genres'].includes(element)) || clickedGenres.length === 0) ? (isEntered[index] ? "background_hover" : "background") : "background_hidden"}
                            onMouseEnter={() => handleMouseEnter(index)}
                            onMouseLeave={() => handleMouseLeave(index)}
                            onClick={() => openAd(item["ad_id"], item["type"])}
                        >{item["type"] === "artist_ad" &&
                            <Ad
                                className={"item"}
                                ad_id={item["ad_id"]}
                                photo={item["photo"]}
                                name={item["name"]}
                                genres={item["genres"]}
                                city={item["city"]}
                                date={item["date"]}
                                requirements={item["requirements"]}
                                type={item["type"]}
                            />}
                        </div>
                    ))}
                </div>
            </div>
                <div className={"title"}>
                    <p className={"title_text"}>Объявления площадок</p>
                </div>
                    <div className={"wrapper"}>
                        {advertisements.map((item, index) => (
                            <div
                                key={item["ad_id"]}
                                className={item["type"] === "venue_ad" && (clickedGenres.every((element) => item['genres'].includes(element)) || clickedGenres.length === 0) ? (isEntered[index] ? "background_hover" : "background") : "background_hidden"}
                                onMouseEnter={() => handleMouseEnter(index)}
                                onMouseLeave={() => handleMouseLeave(index)}
                                onClick={() => openAd(item["ad_id"], item["type"])}
                            >
                                {item["type"] === "venue_ad" &&
                                <Ad
                                    className={"item"}
                                    ad_id={item["ad_id"]}
                                    photo={item["photo"]}
                                    name={item["name"]}
                                    genres={item["genres"]}
                                    city={item["city"]}
                                    date={item["date"]}
                                    requirements={item["requirements"]}
                                    type={item["type"]}
                                />}
                            </div>
                            ))}
                    </div>
                </>
            )}
        </div>
    );
}

class Ads extends Component {

    render() {
        return (
            <Window />
        )
    }
}

export default Ads;
