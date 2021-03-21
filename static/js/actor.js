import {fetchApiPost} from "./data_manager.js";

# editing actor's name
const actorsCharactersTable = document.getElementsByClassName("actor");
const shortenFirstNameButton = document.getElementById("shortenFirstNameButton");


const shortenFirstName = (actorTd) => {
    let actorFullName = actorTd.innerText;
    let actorFullNameArray = actorFullName.split(' ');
    let firstname = actorFullNameArray[0];
    let surname = actorFullNameArray[1];
    let shortenActorName = "".concat(firstname[0],'. ',surname)
    actorTd.innerText = shortenActorName;
}

const shortenFirstNames = () => {
    let actors = Array.from(actorsCharactersTable)
    actors.forEach(actor => shortenFirstName(actor));

}

shortenFirstNameButton.addEventListener("click", shortenFirstNames);


