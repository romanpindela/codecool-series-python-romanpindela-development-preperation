import {fetchApiPost,  fetchApiDelete, fetchApiPatch} from "./data_manager.js";

const searchButton = document.getElementById('searchButton');
const searchInput = document.getElementById('searchInput');


const searchForShowTitleCallback = (response) => {
        console.log(response);
}

const searchForShowTittle = () => {

    let bodyJSONrequest = {'search': searchInput.value }
    fetchApiPost('/search',  searchForShowTitleCallback, bodyJSONrequest );
}

searchButton.addEventListener('click', searchForShowTittle);
