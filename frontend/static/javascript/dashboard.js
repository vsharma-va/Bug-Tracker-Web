function comboChanged(element) {
    let idCombo = element.id;
    let comboValue = element.value;
    let idComboArray = idCombo.split(",");

    let allCombos = document.getElementsByName("filters")
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
    var xml = new XMLHttpRequest();
    xml.open("POST", "/authorised/dash", true);
    xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    let dataToSend = JSON.stringify({
        "type": `${allFilters}`,
        "project_name": `${idComboArray[idComboArray.length - 1]}`,
        "filter_index": `${index}`
    });
    xml.send(dataToSend)

    // when state changes to ready the user is redirected to (dashboard.py filtered())
    xml.onreadystatechange = () => {
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
    };
};

window.onload = () => {
    /* 
        whenever the dashboard.html loads comboLoaded() is called which gets the value of combos
        from (dasboard.py (filter_type_fetch()))
    */
    comboLoaded();
}

function comboLoaded() {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            // refer to (dashboard.py (filter_type_fetch()) for return type details)
            let unclean = xml.responseText;
            let filterAndProject = unclean.split(":");
            let filter = filterAndProject[0].replaceAll("\"", "").replaceAll("\'", "").replace("[", "").replace("]", "").split(",");
            let projectName = filterAndProject[1].replaceAll("\"", "").trim();
            console.log(filter);
            console.log(projectName);
            let allCombos = document.getElementsByName("filters");
            if (filter.length != 0) {
                for (let i = 0; i < allCombos.length; ++i) {
                    console.log(filter[i].trim());
                    allCombos[i].value = filter[i].trim();
                }
            }
        }
    }
    xml.open("GET", "/authorised/filtered/type/fetch", true);
    xml.send(null);
}

function viewAllClicked(element) {
    let classNameElement = element.className;
    let projectName = classNameElement.split(",")[1].replaceAll("\"", "").replaceAll("\'", "").trim()
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
    var xml = new XMLHttpRequest();
    let allCombos = document.getElementsByName("filters")
    let allFilters = [];
    allCombos.forEach((e) => {
        allFilters.push(e.value)
    })

    var xml = new XMLHttpRequest();
    xml.open("POST", "/authorised/dash/update", true)
    xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    let dataToSend = JSON.stringify({
        "type": `${allFilters}`,
    });

    xml.onreadystatechange = () => {
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
    xml.send(dataToSend)
}, 40000)