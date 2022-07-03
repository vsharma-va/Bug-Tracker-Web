function comboChanged(element) {
    let idCombo = element.id;
    let comboValue = element.value;
    let idComboArray = idCombo.split(",");
    var xml = new XMLHttpRequest();
    xml.open("POST", "/authorised/dash", true);
    xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    let dataToSend = JSON.stringify({
        "type": `${comboValue}`,
        "project_name": `${idComboArray[idComboArray.length - 1]}`
    });
    xml.send(dataToSend)

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
    comboLoaded();
}

function comboLoaded() {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = () => {
        if(xml.readyState == 4 && xml.status == 200){
            let unclean = xml.responseText;
            let cleanFilterName = unclean.split(",")[0].replace("[", "").replaceAll("\'", "").trim();
            let cleanProjectName = unclean.split(",")[1].replace("]", "").replaceAll("\'", "").trim();
            console.log(cleanFilterName);
            console.log(cleanProjectName);
            console.log(`fitlers,${cleanProjectName}`)
            let combo = document.getElementById(`filters,${cleanProjectName}`)
            combo.value = cleanFilterName;
        }
    }
    xml.open("GET", "type/fetch", true);
    xml.send(null);
}
