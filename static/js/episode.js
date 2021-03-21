import {fetchApiPost,  fetchApiDelete, fetchApiPatch} from "./data_manager.js";
// this code edits or delete chosen episode from /show/<show_id>/<season>
// it binds code to edit or delete button on list episodes


const showEditEpisodeRow = (e) => {
    let episodeNr = e.target.id
    let trEpisodeNr = document.getElementById(`tr${episodeNr}`)
    trEpisodeNr.hidden = false;
    console.log(episodeNr);
}

const hideEditEpisodeRow = (e) => {
    const charsNumberOfCANCELinID = 7; // Cancel. = 7 chars
    let episodeNr = (e.target.id).slice(charsNumberOfCANCELinID);
    let trEpisodeNr = document.getElementById(`tr${episodeNr}`)
    trEpisodeNr.hidden = true;
    console.log(e, e.target.id, episodeNr);
}

//////////////////////////////////////////////
const deleteEpisode = (e) => {
    if (confirm('Are you sure you want to delete this thing from the database?')) {
        // delete this thing
            console.log(e.target.id);
            let episodeNr = e.target.id;
            let bodyJSONrequest = { show_id: showId, season_nr: seasonNr, episode_nr: episodeNr }
            fetchApiDelete('/episode', deleteEpisodeCallback, bodyJSONrequest );
            console.log('Thing was deleted from the database.');
    } else {
      // Do nothing!
      console.log('Thing was not deleted from the database.');
    }
}

const deleteEpisodeCallback = (response) => {
    if(response.status === "success"){
        console.log("OK. Changing episode title success");
        location.reload();
    }else{
        console.log("Error with changing episode title");
    }
}
const changeEpisode = (e) => {
    const charsNumberOfOKinID = 3; // Ok. = 3 chars
    let episodeNr = (e.target.id).slice(charsNumberOfOKinID);
    let newEpisodeTitle = (document.getElementById(`inputEpisodeTitle.${episodeNr}`)).value;
    let bodyJSONrequest = {new_title:newEpisodeTitle,show_id: showId, season_nr: seasonNr, episode_nr: episodeNr}
    fetchApiPatch('/episode', changeEpisodeCallback, bodyJSONrequest );
}

const changeEpisodeCallback = (response) => {
    if(response.status === "success"){
        console.log("OK. Changing episode title success");
        location.reload();
    }else{
        console.log("Error with changing episode title");
    }
}

////// adding new episode
const trNewEpisode = document.getElementById('trNewEpisode');

const showAddEpisodeButtonRow = (e) => { trNewEpisode.hidden = false; }
const hideAddEpisodeButtonRow = (e) => { trNewEpisode.hidden = true;}

// add new episod button
const addEpisodeButton = document.getElementById('addEpisodeButton');
addEpisodeButton.addEventListener('click', showAddEpisodeButtonRow);

// cancel adding new episode button
const cancelNewEpisodeButton = document.getElementById('Cancel.newEpisode')
cancelNewEpisodeButton.addEventListener('click', hideAddEpisodeButtonRow);


const okSendNewEpisodeDataCallback = (response) => {
    if(response.status === "success"){
        console.log("OK. Adding new episode success");
        location.reload();
    }else{
        console.log("Error with Adding new episode");
    }
}

const okSendNewEpisodeData = () => {
    let newEpisodeTitle = (document.getElementById('inputEpisodeTitle.newEpisodeTitle')).value;
    let newEpisodeNr =  (document.getElementById('inputEpisodeNumber.newEpisodeNr')).value;
    let bodyJSONrequest = {title:newEpisodeTitle,show_id: showId, season_nr: seasonNr, episode_nr: newEpisodeNr}
    fetchApiPost('/episode', okSendNewEpisodeDataCallback, bodyJSONrequest)
}

// ok adding new episode button
const okNewEpisodeButton = document.getElementById('Ok.newEpisode')
okNewEpisodeButton.addEventListener('click', okSendNewEpisodeData);



//////////////////////////////////////////////

// show_id and season_nr
const showId = document.getElementById("show_id").textContent;
const seasonNr = document.getElementById("season_nr").textContent;

/* buttons and their events */
//edit buttons
const editEpisodeButtons = document.getElementsByClassName("editEpisodeButton");
const editEpisodeButtonsArray = Array.from(editEpisodeButtons); // because editEpisodeButtons is NodeList
//Array.prototype.forEach.call(editEpisodeButtons,button => button.addEventListener('click',showEditEpisodeRow))
editEpisodeButtonsArray.forEach(button => button.addEventListener('click',showEditEpisodeRow));

//delete buttons
const deleteEpisodeButtons = document.getElementsByClassName("deleteEpisodeButton");
const deleteEpisodeButtonsArray = Array.from(deleteEpisodeButtons);
deleteEpisodeButtonsArray.forEach(button => button.addEventListener('click', deleteEpisode));


// cancel buttons
const cancelButtons = document.getElementsByClassName("cancel-button");
const cancelButtonsArray = Array.from(cancelButtons);
cancelButtonsArray.forEach(button => button.addEventListener('click', hideEditEpisodeRow));

// ok buttons
const okButtons = document.getElementsByClassName("ok-button");
const okButtonsArray = Array.from(okButtons);
okButtonsArray.forEach(button => {button.addEventListener('click', changeEpisode)});



