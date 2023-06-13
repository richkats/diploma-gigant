import React, { useState } from 'react';
import '../App.css'
import '../add.css'
import {Button, Form, FormControl, ToastContainer} from "react-bootstrap";
import photo from '../components/photo_logo.svg'
import "react-modern-calendar-datepicker/lib/DatePicker.css";
import { Calendar } from "react-modern-calendar-datepicker";
import DatePicker from "react-modern-calendar-datepicker";
import {render} from "@testing-library/react";
import {ImageUploader} from './handleImageUpload.js'
const currentDate = new Date();
const defaultValue = {
    year: currentDate.getFullYear(),
    month: currentDate.getMonth()+1,
    day: currentDate.getDate(),
};


function Add() {
    const [selectedDay, setSelectedDay] = useState(defaultValue);
    const [groupName, setGroupName] = useState("");
    const [selectedCity, setSelectedCity] = useState("");
    const [requirements, setRequirements] = useState([{ name: "", value: "" }]);
    const [contacts, setContacts] = useState("");
    const [genres, setGenres] = useState([""]);
    const [description, setDescription] = useState("");
    const [equipment, setEquipment] = useState("");
    const [preview, setPreview] = useState(photo);
    const [checked, setChecked] = useState(false);
    const [needSound, setNeedSound] = useState(false);
    const [needLight, setNeedLight] = useState(false);
    const handleLightChange = () => {
        setNeedLight(!needLight)
    }
    const handleSoundChange = () => {
        setNeedSound(!needSound)
    }
    const handleChange = () => {
        setChecked(!checked);
    };
    const addGenre = () => {
        setGenres([...genres, ""]);
    };

    const addRequirement = () => {
        setRequirements([...requirements, { name: "", value: "" }]);
    };
    const handleRequirementChange = (index, field, value) => {
        const updatedRequirements = [...requirements];
        updatedRequirements[index][field] = value;
        setRequirements(updatedRequirements);
    };
    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onloadend = () => {
            setPreview(reader.result);
        };

        if (file) {
            reader.readAsDataURL(file);
        }

    };
    const removeRequirement = (index) => {
        if (index !== 0){
            const updatedRequirements = [...requirements]
            updatedRequirements.splice(index, 1)
            setRequirements(updatedRequirements)
        }
    }
    const removeGenre = (index) => {
        if (index !== 0){
            const updatedGenres = [...genres]
            updatedGenres.splice(index,1)
            setGenres(updatedGenres)
        }
    }
    const handleSubmit = (event) => {
        event.preventDefault();
        const date = new Date(selectedDay.year, selectedDay.month - 1, selectedDay.day + 1);
        const timestamp = date.getTime();
        let route = "/create_artist_ad/";
        console.log(checked)
        let formData = {
            name: groupName,
            city: selectedCity,
            free_dates: [timestamp],
            requirements: requirements.map((requirement) => ({
                name: requirement.name,
                value: requirement.value,
            })),
            contacts: contacts,
            genres: genres,
            description: description,
            equipment: equipment,
            photo: preview,
        };
        if (checked)
        {
            formData = {
                name: groupName,
                city: selectedCity,
                free_dates: [timestamp],
                requirements: requirements.map((requirement) => ({
                    name: requirement.name,
                    value: requirement.value,
                })),
                contacts: contacts,
                genres: genres,
                description: description,
                equipment: equipment,
                photo: preview,
                have_soundguy: needSound,
                have_lightguy: needLight
            };
            route = "/create_venue_ad/";
        }
        fetch('http://10.13.13.25:8000' + route,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            })
        alert("Объявление создано!")
        console.log(formData);
    };

    return (
        <div>
            <div className={"title_description"}>
                <p className={"title_text"}>Добавить объявление</p>
            </div>
            <div className={"background_description"}>
                <Form inline onSubmit={handleSubmit} className={"text_description_medium"}>
                    <div className={"title_wrapper"}>
                        <FormControl
                            type="text"
                            placeholder={checked ? "Название площадки" : "Название группы"}
                            className="form"
                            value={groupName}
                            onChange={(e) => setGroupName(e.target.value)}
                        />
                        <div className={"check_box"}>
                            <p className={"text_description_regular"}>Исполнитель </p>
                            <input className="tgl_1 tgl_1-flat" id="cb4" type="checkbox" checked={checked} onChange={handleChange}/>
                            <label className="tgl_1-btn" htmlFor="cb4"/>
                            <p className={"text_description_regular"}> Площадка</p>
                        </div>
                    </div>
                    <hr style={{ width: "95%", margin: "auto" }}/>
                    <div className="wrapper_add">
                        <div className={"block"} style={{height:"100%", display: "flex", flexDirection: "column", justifyContent: "center"}}>
                            <div className="mb-4 d-flex justify-content-center">
                            </div>
                            <div className="d-flex justify-content-center photo_add">
                                <div className="btn btn-primary btn-rounded" style={{backgroundColor:'gray', border:'0px'}}>
                                    <label className="form-label text-white m-1" htmlFor="customFile1">Прикрепить фотографии</label>
                                    <input type="file" className="form-control d-none" id="customFile1"/>
                                    <input type="file" accept="image/*" onChange={handleImageUpload} />
                                    {preview && <img src={preview} style={{ width: 200, height: 150,margin:10}} alt="Preview" />}
                                </div>
                            </div>
                        </div>
                        <div className={"block"}>
                            <FormControl
                                type="text"
                                placeholder={checked ? "Введите адрес" : "Введите город"}
                                className="blockform"
                                value={selectedCity}
                                onChange={(e) => setSelectedCity(e.target.value)}
                            />
                            <div className={"calendar"}>
                                <Calendar
                                    value={selectedDay}
                                    onChange={setSelectedDay}
                                    shouldHighlightWeekends
                                    colorPrimary="gray"
                                />
                            </div>
                            {requirements.map((requirement, index) => (
                                <div key={index} className="req_wrapper">
                                    <FormControl
                                        type="text"
                                        placeholder="Название"
                                        className="block_req"
                                        value={requirement.name}
                                        onChange={(e) => handleRequirementChange(index, "name", e.target.value)}
                                    />
                                    <FormControl
                                        type="text"
                                        placeholder="Значение"
                                        className="block_req"
                                        value={requirement.value}
                                        onChange={(e) => handleRequirementChange(index, "value", e.target.value)}
                                    />
                                    {index !== 0 && (<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="25px" height="25px" onClick={() => removeRequirement(index)}><path d="M 7.7070312 6.2929688 L 6.2929688 7.7070312 L 23.585938 25 L 6.2929688 42.292969 L 7.7070312 43.707031 L 25 26.414062 L 42.292969 43.707031 L 43.707031 42.292969 L 26.414062 25 L 43.707031 7.7070312 L 42.292969 6.2929688 L 25 23.585938 L 7.7070312 6.2929688 z"/></svg>
                                    )}</div>
                            ))}
                            <Button
                                type="button"
                                onClick={addRequirement}
                                style={{
                                    display: "block",
                                    margin: "auto",
                                    backgroundColor: "gray",
                                    border: "0px",
                                    marginTop: "10px",
                                    marginBottom: "10px",
                                }}
                            >
                                Добавить еще требование
                            </Button>
                            <FormControl
                                type="text"
                                placeholder="Укажите контакты"
                                className="blockform"
                                value={contacts}
                                onChange={(e) => setContacts(e.target.value)}
                            />
                            {genres.map((genre, index) => (
                                <div key={index} className={"genre_wrap"}>
                                    <FormControl
                                        type="text"
                                        placeholder="Название жанра"
                                        className="blockformgenre"
                                        value={genre}
                                        onChange={(e) => {
                                            const updatedGenres = [...genres];
                                            updatedGenres[index] = e.target.value;
                                            setGenres(updatedGenres);
                                        }}
                                    />
                                    {index !== 0 && (<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="25px" height="25px" onClick={() => removeGenre(index)}><path d="M 7.7070312 6.2929688 L 6.2929688 7.7070312 L 23.585938 25 L 6.2929688 42.292969 L 7.7070312 43.707031 L 25 26.414062 L 42.292969 43.707031 L 43.707031 42.292969 L 26.414062 25 L 43.707031 7.7070312 L 42.292969 6.2929688 L 25 23.585938 L 7.7070312 6.2929688 z"/></svg>
                                    )}
                                </div>
                            ))}

                            <Button
                                type="button"
                                onClick={addGenre}
                                style={{
                                    display: "block",
                                    margin: "auto",
                                    backgroundColor: "gray",
                                    border: "0px",
                                    marginTop: "10px",
                                    marginBottom: "10px",
                                }}
                            >
                                Добавить жанр
                            </Button>
                            <div className={checked ? "check_box_group" : "check_box_group_hidden"}>
                                <div>
                                    <input className="tgl tgl-flat" id="cb5" type="checkbox" checked={needSound} onChange={handleSoundChange}/>
                                    <label className="tgl-btn" htmlFor="cb5"/>
                                </div>
                                    <p className={"text_description_regular"}>Есть звукооператор</p>
                                <div>
                                    <input className="tgl tgl-flat" id="cb6" type="checkbox" checked={needLight} onChange={handleLightChange}/>
                                    <label className="tgl-btn" htmlFor="cb6"/>
                                </div>
                                    <p className={"text_description_regular"}>Есть светооператор</p>
                            </div>
                        </div>
                        <FormControl
                            as="textarea"
                            type="text"
                            placeholder="Введите описание"
                            className="textareaform"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                        />
                        <FormControl
                            as="textarea"
                            type="text"
                            placeholder="Ваше оборудование"
                            className="textareaform"
                            value={equipment}
                            onChange={(e) => setEquipment(e.target.value)}
                        />
                    </div>
                    <Button type="submit" style={{ display: "block", margin: "auto", backgroundColor: "gray", border: "0px" }}>
                        Отправить
                    </Button>
                </Form>
            </div>
        </div>
    );
}

export default Add;


