import {fetchApiPost} from "./data_manager.js";

const inputEmail = document.getElementById('inputEmail');
const inputPassword = document.getElementById('inputPassword');
const formInfo = document.getElementById('formInfo');

// hide login/register forms when click outside forms
const bodyPage = document.getElementById('body');
document.addEventListener('dblclick', showLoginRegisterForms);

function showLoginRegisterForms(e){
    console.log(e);
    console.log(e.target.id);
    if (['bt_register', 'bt_login'].includes(e.target.id)){
        console.log('\'bt_register\', \'bt_login\'');
        inputEmail.type = "text";
        inputPassword.type = "password";
        formInfo.hidden = false;
    }else{
        inputEmail.type = "hidden";
        inputPassword.type = "hidden";
        formInfo.hidden = true;
}}

// register ////////////////////////////
const registerButton = document.getElementById('bt_register');
registerButton.addEventListener('click',registerFunction);

function registerFunction(e){
    e.preventDefault();
    if(inputEmail.type === "hidden"){
        showLoginRegisterForms(e);
    }else{
        sendFormDataToRegisterUser();
    }
}

function sendFormDataToRegisterUser(){
    let userFormData = { username: inputEmail.value, password: inputPassword.value}
    console.log("sendig form data to register user.. ", userFormData)
    fetchApiPost('/register', registrationStatus, userFormData)
}

function registrationStatus(response){
    if(response.status === "success"){
        console.log("OK. Registration success");
    }else{
        console.log("Error with Registration: Probably wrong login");
    }
}

// login //////////////////////////
const loginButton = document.getElementById('bt_login');
loginButton.addEventListener('click', loginFunction);

function loginFunction(e){
    e.preventDefault();
    if(inputEmail.type === "hidden"){
        showLoginRegisterForms(e);
    }else{
        sendFormDataToLoginUser();
    }
}

function sendFormDataToLoginUser(){
    let userFormData = { username: inputEmail.value, password: inputPassword.value}
    console.log("sending form data to login user...", userFormData)
    fetchApiPost('/login', loginStatus, userFormData)
}

function loginStatus(response){
    if(response.status === "success"){
        console.log("OK. Login success");
    }else{
        console.log("Error with Login: Probably wrong login");
    }
}