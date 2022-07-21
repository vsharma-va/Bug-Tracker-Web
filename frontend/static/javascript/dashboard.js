import { Helper } from "./helper/allHelpers.js";

let allCombos = document.getElementsByName("filters");
Array.from(allCombos).forEach((element) => {
    element.addEventListener("change", comboChanged);
})

let allViewAllBtns = document.querySelectorAll('[class^="view-all,"]');
Array.from(allViewAllBtns).forEach((element) => {
    element.addEventListener("click", viewAllClicked);
})

function comboChanged(event) {
    let idCombo = event.target.id;
    let comboValue = event.target.value;
    let idComboArray = idCombo.split(",");

    let allFilters = [];
    let index = -1;
    let counter = 0;
    allCombos.forEach((e) => {
        if (e.id === idCombo) {
            allFilters.push(comboValue);
            index = counter;
        } else {
            allFilters.push(e.value);
        }
        ++counter
    })
    // sent to (dashboard.py dash()) every time a combo box is changed
    let xml = new XMLHttpRequest();
    let dataToSend = JSON.stringify({
        "type": `${allFilters}`,
        "project_name": `${idComboArray[idComboArray.length - 1]}`,
        "filter_index": `${index}`
    });

    // when state changes to ready the user is redirected to (dashboard.py filtered())

    let onReadyFunc = () => {
        if (xml.readyState == XMLHttpRequest.DONE) {
            if (xml.status == 200) {
                alert(xml.responseText);
                let urlAndFilter = xml.responseText;
                window.location.href = urlAndFilter.replace("?", "/");
            } else {
                console.log(`http errror -> ${xml.status}`)
            }
        } else {
            console.log(`error -> ${xml.readyState}`)
        }
    }
    Helper.httpRequest(xml, "POST", "/authorised/dash", onReadyFunc, dataToSend);
};

function viewAllClicked(event) {
    let classNameElement = event.target.className;
    let projectName = classNameElement.split(",")[1].replaceAll("\"", "").replaceAll("\'", "").trim();
    let newUrl = window.location.href + `/main/${projectName}`;
    window.location.href = newUrl;
}

window.onload = () => {
    /* 
        whenever the dashboard.html loads comboLoaded() is called which gets the value of combos
        from (dasboard.py (filter_type_fetch()))
    */
    comboLoaded();
}

function comboLoaded() {
    let xml = new XMLHttpRequest();

    var onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            // refer to (dashboard.py (filter_type_fetch()) for return type details)
            let unclean = xml.responseText;
            let filterAndProject = unclean.split(":");
            let filter = filterAndProject[0].replaceAll("\"", "").replaceAll("\'", "").replace("[", "").replace("]", "").split(",");
            let projectName = filterAndProject[1].replaceAll("\"", "").trim();
            let allCombos = document.getElementsByName("filters");
            if (filter[0].length != 0) {
                for (let i = 0; i < allCombos.length; ++i) {
                    console.log(filter[i].trim());
                    allCombos[i].value = filter[i].trim();
                }
            }
        }
    }
    Helper.httpRequest(xml, "GET", "/authorised/filtered/type/fetch", onReadyFunc, null)
}



// function test() {
//     var xml = new XMLHttpRequest();
//     let allCombos = document.getElementsByName("filters")
//     let allFilters = [];
//     allCombos.forEach((e) => {
//         allFilters.push(e.value)
//     })

//     var xml = new XMLHttpRequest();
//     xml.open("POST", "/authorised/dash/update", true)
//     xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//     let dataToSend = JSON.stringify({
//         "type": `${allFilters}`,
//     });

//     xml.onreadystatechange = () => {
//         if (xml.readyState == 4 && xml.status == 200) {
//             let cardHtml = JSON.parse(xml.responseText);
//             let allProjects = document.getElementsByClassName("project-name")
//             Array.from(allProjects).forEach((element) => {
//                 console.log(cardHtml[element.innerText]);
//                 let insertAt = document.getElementById(`card-container,${element.innerText}`);
//                 let totalValue = "";
//                 Array.from(cardHtml[element.innerText]).forEach((value) => {
//                     totalValue += value
//                 });
//                 insertAt.innerHTML = totalValue;
//             });
//         }
//     }
//     xml.send(dataToSend)

// }

setInterval(() => {
    let xml = new XMLHttpRequest();
    let allCombos = document.getElementsByName("filters")
    let allFilters = [];
    allCombos.forEach((e) => {
        allFilters.push(e.value)
    })
    let dataToSend = JSON.stringify({
        "type": `${allFilters}`,
    });

    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            let cardHtml = JSON.parse(xml.responseText);
            let allProjects = document.getElementsByClassName("project-name")
            Array.from(allProjects).forEach((element) => {
                let insertAt = document.getElementById(`card-container,${element.innerText}`);
                let totalValue = "";
                Array.from(cardHtml[element.innerText]).forEach((value) => {
                    totalValue += value
                });
                insertAt.innerHTML = totalValue;
            });
        }
    }
    Helper.httpRequest(xml, "POST", "/authorised/dash/update", onReadyFunc, dataToSend);
}, 40000)