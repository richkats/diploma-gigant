import React, {Component, useEffect, useState} from 'react';
import '../add.css'
import {Form, FormControl} from "react-bootstrap";
import { useParams } from 'react-router-dom';
import {useCookies} from "react-cookie";
import "../description.css"


const BACKEND_URL = "http://10.13.13.25:8000";
function Screen() {
    const [advertisement, setAdvertisement] = useState({requirements: [], genres: []});
    const [cookies, setCookie] = useCookies(['ad_id', 'type']);
    const [isLoading, setIsLoading] = useState(true);
    const ad_id = cookies.ad_id;
    function responseJSON(json){
        setAdvertisement(json)
        console.log(json)
    }

    useEffect(() => {
        fetch(BACKEND_URL + "/rendered_" + cookies.type + "/?ad_id=" + ad_id)
            .then((res) => res.json())
            .then((json) => responseJSON(json));
    }, []);
    if(advertisement["genres"].length && isLoading){
        setIsLoading(false)
    }
    function getNormalDate()
    {
        const date = new Date(advertisement["date"]);
        const dateFormat = date.getDate()+
            "/"+(date.getMonth()+1)+
            "/"+date.getFullYear();
        return dateFormat;
    }
    function City(props) {
        return <div className={"text_description_medium"}>{cookies.type === "venue_ad" ? "Адрес: " : "Город: "}{props.name}</div>;
    }
    function Band(props) {
        return <div className={"band_description"}>{props.name}</div>;
    }
    function Dates(props) {
        return (
            <div className={"text_description_medium"}>
                Свободные даты:
                <div className={"text_description_regular"}>{props.name}</div>
            </div>
        );
    }
    function Genre(props) {
        return <p className={"genre_background"}>{props.name}</p>;
    }
    function Contacts(props) {
        return <div className={"text_description_medium"}>Контакты: {props.name}</div>;
    }
    function Equipment(props) {
        return <div className={"text_description_medium"}>Оборудование: {props.name}</div>;
    }
    function Photo(props) {
        return <img className={"photo_description"} src={props.photo} alt={""}/>;
    }
    function Descr(props) {
        return <div className={"text_description_medium"}>Описание: {props.name}</div>;
    }

    return (
    <div>
        <div className={"title_description"}>
            <p className={"title_text"}>Объявление {cookies.type === "venue_ad" ? "площадки" : "исполнителя"}</p>
        </div>
        {isLoading ? (
            <div className="load"/>
        ) : (<>
        <div className={"background_description"}>
            <Band name ={advertisement["name"]}/>
            <hr style={{width:"95%", margin: 'auto'}}/>
            <div className="wrapper_description">
                <Photo photo={advertisement["photo"]}/>
                <div className={"block_description"}>
                    <City name = {advertisement["city"]}/>
                    <Dates name = {getNormalDate(advertisement["date"])}/>
                    <div className={"text_description_medium"}>
                        Требования:
                    {advertisement["requirements"].map((item) => (
                        <div key={item.name}>
                            {item.name}: {item.value}
                        </div>
                    ))}
                    </div>
                    <Contacts name={advertisement["contacts"]}/>
                    <div className={"genre_text_description"}>
                        {advertisement["genres"].map((item) => (
                            <Genre key={item} name={item} />
                        ))}
                    </div>
                </div>
                <div className={"block_description_text"}>
                    <Descr name={advertisement["description"]}/>
                </div>
                <div className={"block_description_text"}>
                    <Equipment name={advertisement["equipment"]}/>
                    <div className={cookies.type === "venue_ad" ? "text_description_medium" : "background_hidden"}>Наличие звукооператора: {advertisement["have_lightguy"] ? "есть" : "нет"}</div>
                    <div className={cookies.type === "venue_ad" ? "text_description_medium" : "background_hidden"}>Наличие светооператора: {advertisement["have_lightguy"] ? "есть" : "нет"}</div>
                </div>
            </div>
        </div>
            </>
        )}
    </div>
    );
};
class Description extends Component {
    render() {
        return (
            <Screen/>
        );
    }
}

export default Description;
