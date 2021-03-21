import {fetchApiGet} from "./data_manager.js";
// {## new route to one show#}

const getActorsFromApiButton = document.getElementById("getActorsFromApiButton");
const actorsCharactersTableBody = document.getElementById("actorsCharactersTableBody");
const actorsCharacterTable = document.getElementById("actorsCharacterTable");

const showId = document.getElementById("show_id").innerText;
const seasonId = document.getElementById("season_id").innerText;
const episodeId = document.getElementById("episode_id").innerText;


const createActorRow = (actor) => {
    
    let newActorRow = document.createElement("tr");
    let newActorRowActorName = document.createElement("td");
    newActorRowActorName.innerText = actor.name;
    let newActorRowCharacterName = document.createElement("td");
    newActorRowCharacterName.innerText = actor.character_name;
    newActorRow.appendChild(newActorRowActorName);
    newActorRow.appendChild(newActorRowCharacterName);
    actorsCharactersTableBody.appendChild(newActorRow);
}


const putActorsOnPage = (actors) => {
    actorsCharactersTableBody.innerHTML = '';
    actors.forEach(actor => createActorRow(actor))
}

const showActorsFromShow = () => {
    actorsCharacterTable.hidden = false;
    fetchApiGet(`/actors/${showId}`, putActorsOnPage);
}

getActorsFromApiButton.addEventListener('click', showActorsFromShow);
