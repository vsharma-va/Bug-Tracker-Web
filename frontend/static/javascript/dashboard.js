import { Helper } from "./helper/allHelpers.js";
import { Charts } from "./charts.js";

let DOUGHNUT_STAT_CHART;

let allCardFilterCombos = document.getElementsByName("filters");
Array.from(allCardFilterCombos).forEach((element) => {
    element.addEventListener("change", cardFilterComboChanged);
});

let allViewAllBtns = document.querySelectorAll('[class^="view-all,"]');
Array.from(allViewAllBtns).forEach((element) => {
    element.addEventListener("click", projectSpecificBtnClicked);
});

let allStatsFilterCombos = document.getElementsByClassName(
    "filter-info-at-a-glance"
);
Array.from(allStatsFilterCombos).forEach((element) => {
    element.addEventListener("change", statsFilterComboChanged);
});

let allRoleBtns = document.querySelectorAll('[class^="role,"]');
console.log(allRoleBtns);
Array.from(allRoleBtns).forEach((element) => {
    element.addEventListener("click", projectSpecificBtnClicked);
});

document
    .getElementById("invite")
    .addEventListener("click", headerButtonClicked);
document
    .getElementById("add-user-id")
    .addEventListener("click", addUserIdToPopup);
let allRemoveXInPopup;
let invitePopupBackground = document
    .getElementById("invite-popup-background")
    .addEventListener("click", outsideContainerClicked);
document
    .getElementById("generate-link")
    .addEventListener("click", generateLinkClicked);

document.getElementById("join").addEventListener("click", headerButtonClicked);
document
    .getElementById("join-popup-background")
    .addEventListener("click", outsideContainerClicked);
document
    .getElementById("join-confirm-btn")
    .addEventListener("click", joinPopupConfirmClicked);

document
    .getElementById("create")
    .addEventListener("click", headerButtonClicked);
document
    .getElementById("create-popup-background")
    .addEventListener("click", outsideContainerClicked);
document
    .getElementById("confirm-create")
    .addEventListener("click", createPopupConfirmClicked);

function cardFilterComboChanged(event) {
    let idCombo = event.target.id;
    let comboValue = event.target.value;
    let idComboArray = idCombo.split(",");

    let allFilters = [];
    let index = -1;
    let counter = 0;
    allCardFilterCombos.forEach((e) => {
        if (e.id === idCombo) {
            allFilters.push(comboValue);
            index = counter;
        } else {
            allFilters.push(e.value);
        }
        ++counter;
    });

    let projectName = idComboArray[idComboArray.length - 1];

    // sent to (dashboard.py dash()) every time a combo box is changed
    let xml = new XMLHttpRequest();
    let dataToSend = JSON.stringify({
        type: `${allFilters}`,
        project_name: `${projectName}`,
        filter_index: `${index}`,
    });

    // when state changes to ready the user is redirected to (dashboard.py filtered())

    let onReadyFunc = () => {
        if (xml.readyState == XMLHttpRequest.DONE) {
            if (xml.status == 200) {
                let cardDict = JSON.parse(xml.responseText);
                let insertAt = document.getElementById(
                    `card-container,${projectName}`
                );
                let totalValue = "";
                Array.from(cardDict[projectName]).forEach((element) => {
                    totalValue += element;
                });
                insertAt.innerHTML = totalValue;
            } else {
                console.log(`http errror -> ${xml.status}`);
            }
        } else {
            console.log(`error -> ${xml.readyState}`);
        }
    };
    Helper.httpRequest(
        xml,
        "POST",
        `/authorised/dash/filter/${allFilters}`,
        onReadyFunc,
        dataToSend
    );
}

function projectSpecificBtnClicked(event) {
    let classNameElement = event.target.className;
    let idOfElement = event.target.id;
    let projectName = classNameElement
        .split(",")[1]
        .replaceAll('"', "")
        .replaceAll("'", "")
        .trim();
    let newUrl = "";
    if (idOfElement === "view-all-btn") {
        newUrl = window.location.href + `/main/${projectName}`;
    } else if (idOfElement === "role-btn") {
        newUrl = window.location.href + `/roles/${projectName}`;
    }
    window.location.href = newUrl;
}

window.onload = () => {
    /* 
        whenever the dashboard.html loads comboLoaded() is called which gets the value of combos
        from (dasboard.py (filter_type_fetch()))
    */
    cardFilterComboLoaded();
    currentProjectStatistics("None", false);
};

function cardFilterComboLoaded() {
    let xml = new XMLHttpRequest();

    var onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            // refer to (dashboard.py (filter_type_fetch()) for return type details)
            let unclean = xml.responseText;
            let filterAndProject = unclean.split(":");
            let filter = filterAndProject[0]
                .replaceAll('"', "")
                .replaceAll("'", "")
                .replace("[", "")
                .replace("]", "")
                .split(",");
            let projectName = filterAndProject[1].replaceAll('"', "").trim();
            let allCombos = document.getElementsByName("filters");
            console.log(filter);
            if (filter[0].length != 0) {
                for (let i = 0; i < allCombos.length; ++i) {
                    allCombos[i].value = filter[i].trim();
                }
            }
        }
    };
    Helper.httpRequest(
        xml,
        "GET",
        "/authorised/filtered/type/fetch",
        onReadyFunc,
        null
    );
}

function statsFilterComboChanged(event) {
    let changedComboValue = event.target.value;
    currentProjectStatistics(changedComboValue, true);
}

function currentProjectStatistics(projectName, destroyOld) {
    let insertAt = document
        .getElementById("current-project-statistics")
        .getContext("2d");
    let paragraph = document.getElementById("empty-text");
    let artist = new Charts(insertAt);
    let xml = new XMLHttpRequest();
    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            let returnValue = JSON.parse(xml.responseText);
            console.log(returnValue);
            if (destroyOld === true) {
                artist.destroyChart(DOUGHNUT_STAT_CHART);
            }
            if (Object.keys(returnValue).length === 0) {
                paragraph.innerHTML = "No Data To Display";
            } else if (returnValue["status"] === "none") {
                paragraph.innerHTML =
                    "Please select a project from the filter above";
            } else {
                paragraph.innerHTML = "";
                DOUGHNUT_STAT_CHART = artist.drawDoughnutChart(
                    Object.values(returnValue),
                    Object.keys(returnValue),
                    true
                );
            }
        }
    };
    Helper.httpRequest(
        xml,
        "GET",
        `/authorised/dash/charts/gcps/${projectName}`,
        onReadyFunc,
        null
    );
}

function headerButtonClicked(event) {
    let background = document.getElementById(
        `${event.target.id}-popup-background`
    );
    background.style.display = "grid";
}

function outsideContainerClicked(event) {
    if (
        event.target.id == "invite-popup-background" ||
        event.target.id == "join-popup-background" ||
        event.target.id == "create-popup-background"
    ) {
        event.target.style.display = "none";
    }
}

function joinPopupConfirmClicked() {
    let userInput = document.getElementById("join-link");
    let xml = new XMLHttpRequest();
    let dataToSend = JSON.stringify({
        join_link: `${userInput.value}`,
    });
    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            let returnValue = JSON.parse(xml.responseText);
            console.log(returnValue);
            if (returnValue["status"] == "error") {
                let insertAt = document.getElementById("error-flash");
                insertAt.innerHTML = returnValue["html"];
            } else if (returnValue["status"] == "success") {
                let insertAt = document.getElementById("error-flash");
                insertAt.innerHTML = returnValue["html"];
            }
        }
    };
    Helper.httpRequest(
        xml,
        "POST",
        window.location.href + "/joinWithInvite",
        onReadyFunc,
        dataToSend
    );
}

function addUserIdToPopup() {
    let userInput = prompt("Enter the id of user", -1);
    let insertAt = document.getElementById("user-id");
    let toInsert = `<div class='user-id-tag'><p class='user-id-number'>${userInput}</p><button class='remove-user-id'>X</div>`;
    insertAt.innerHTML += toInsert;
    allRemoveXInPopup = document.getElementsByClassName("remove-user-id");
    Array.from(allRemoveXInPopup).forEach((element) => {
        element.addEventListener("click", xRemoveUserIdClickedInInvitePopup);
    });
}

function xRemoveUserIdClickedInInvitePopup(event) {
    event.target.parentNode.remove();
}

function generateLinkClicked() {
    let allIds = document.getElementsByClassName("user-id-number");
    let projectName = document.getElementById("project-selector").value;
    console.log(projectName);
    let allIdsArray = [];
    for (let i = 0; i < allIds.length; ++i) {
        allIdsArray.push(allIds.item(i).innerText);
    }
    let xml = new XMLHttpRequest();
    let dataToSend = JSON.stringify({
        user_ids: `${allIdsArray}`,
        project_name: `${projectName}`,
    });
    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            document.getElementById("generated-link").innerHTML =
                xml.responseText;
        }
    };
    Helper.httpRequest(
        xml,
        "POST",
        window.location.href + "/generateInvite",
        onReadyFunc,
        dataToSend
    );
}

function createPopupConfirmClicked() {
    let projectName = document.getElementById("project-name").value;
    let xml = new XMLHttpRequest();
    let dataToSend = JSON.stringify({
        project_name: projectName,
    });
    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            let insertAt = document.getElementById("error-flash");
            let response = JSON.parse(xml.responseText);
            if (response["status"] === "ok") {
                insertAt.innerHTML = response["html"];
            } else {
                insertAt.innerHTML = response["html"];
            }
        }
    };
    Helper.httpRequest(
        xml,
        "POST",
        window.location.href + "/createNewProject",
        onReadyFunc,
        dataToSend
    );
}

setInterval(() => {
    let xml = new XMLHttpRequest();
    let allCombos = document.getElementsByName("filters");
    let allFilters = [];
    allCombos.forEach((e) => {
        allFilters.push(e.value);
    });
    let dataToSend = JSON.stringify({
        type: `${allFilters}`,
    });

    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            let cardHtml = JSON.parse(xml.responseText);
            let allProjects = document.getElementsByClassName("project-name");
            Array.from(allProjects).forEach((element) => {
                let insertAt = document.getElementById(
                    `card-container,${element.innerText}`
                );
                let totalValue = "";
                Array.from(cardHtml[element.innerText]).forEach((value) => {
                    totalValue += value;
                });
                insertAt.innerHTML = totalValue;
            });
        }
    };
    Helper.httpRequest(
        xml,
        "POST",
        "/authorised/dash/update",
        onReadyFunc,
        dataToSend
    );
}, 40000);

setInterval(() => {
    let whereToDisplay = document.getElementById("date-time");
    let dateTime = new Date();
    whereToDisplay.textContent = dateTime;
}, 1000);
