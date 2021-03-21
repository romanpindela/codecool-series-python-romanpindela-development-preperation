import {fetchApiPost} from "./data_manager.js";

const showActorCallback = (response) => {
    setTimeout(()=>{alert(response['name'])},3000);
}

const showActor = () => {
    fetchApiPost('/actorofaday', showActorCallback,{'test':'test'})
}

const actorOfADayButton = document.getElementById("actorOfADayButton");
actorOfADayButton.addEventListener('click', showActor);

