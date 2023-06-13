import React, {Component} from 'react';
import {Button, Container, Form, FormControl, Nav, Navbar} from "react-bootstrap";
import logo from './ant_logo.png'
import { Route, Routes} from "react-router-dom"

import Home from "../Pages/Home";
import Add from "../Pages/Add";
import Description from "../Pages/Description";
import Account from "../Pages/account";
import Ads from "../Pages/ads"


class Header extends Component {
    render() {
        return (
            <>
            <Navbar fixed={"top"} collapseOnSelect expand="md" className={"bg_light"} variant="light">
                <Container>
                    <Navbar.Brand href="/Ads">
                        <img
                            src = {logo}
                            height="60"
                            width="180"
                            className="d-inline-block align-top"
                            alt="Logo"
                            />
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="responsive-navbar-nav"/>
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav className="me-auto">
                            <Nav.Link href={'/Ads'}> Объявления </Nav.Link>
                            <Nav.Link href={'/Add'}> Добавить объявление </Nav.Link>
                            <Nav.Link href={'/Account'}> Личный кабинет </Nav.Link>

                        </Nav>
                        <Form inline>
                            <FormControl
                            type="text"
                            placeholder="Поиск"
                            className="mr-sm-2"
                            />
                        </Form>
                        <Button variant={"outline-info"}>Поиск</Button>

                    </Navbar.Collapse>
                </Container>
            </Navbar>

               <Routes>
                   <Route path="/Ads" element={<Ads />} />
                   <Route path="/Add" element={<Add/>} />
                   <Route path={"/Description"} element={<Description/>} />
                   <Route path={"/Account"} element={<Account/>} />
               </Routes>

    </>
        );
    }
}

export default Header;
