import {fetchApiPost} from "./data_manager.js";

//# list all show seasons

//elements
const newSeasonTr = document.getElementById("newSeasonTr");
const showId = document.getElementById("show_id").innerText;
const inputNewEpisodeID = document.getElementById("inputNewEpisodeID");
const inputNewEpisodeSeasonNumber = document.getElementById("inputNewEpisodeSeasonNumber");
const inputNewEpisodeSeasonTitle = document.getElementById("inputNewEpisodeSeasonTitle");
const inputNewEpisodeSeasonOverview = document.getElementById("inputNewEpisodeSeasonOverview");

//buttons
const addSeasonButton = document.getElementById("addSeasonButton");
const OkNewEpisodeButton = document.getElementById("OkNewEpisodeButton");
const CancelNewEpisodeButton = document.getElementById("CancelNewEpisodeButton");

//events
const showNewSeasonTr = () => { newSeasonTr.hidden = false; }
const hideNewSeasonTr = () => { newSeasonTr.hidden = true; }

addSeasonButton.addEventListener('click', showNewSeasonTr);
CancelNewEpisodeButton.addEventListener('click', hideNewSeasonTr);

const addNewSeasonCallback = (reponse) => {
    console.log(response);
}


const addNewSeason = () => {
    let season_id = inputNewEpisodeID.value;
    let season_number = inputNewEpisodeSeasonNumber.value;
    let season_title = inputNewEpisodeSeasonTitle.value;
    let season_overview = inputNewEpisodeSeasonOverview.value;

    let bodyJSONrequest = {
        'season_id': season_id,
        'season_number': season_number,
        'season_title': season_title,
        'season_overview': season_overview };

    console.log(bodyJSONrequest)

    fetchApiPost(`/show/${showId}/season`, addNewSeasonCallback, bodyJSONrequest);

}

OkNewEpisodeButton.addEventListener('click', addNewSeason);