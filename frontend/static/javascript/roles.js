import { Helper } from "./helper/allHelpers.js";

let allRoleSelectors = document.getElementsByClassName("user_roles");
Array.from(allRoleSelectors).forEach((element) => {
    element.addEventListener("change", roleSelectorValueChanged);
});

let saveChangesButton = document.getElementById("save-changes-button");
saveChangesButton.addEventListener("click", saveChangesButtonClicked);

window.onload = () => {
    loadButtonWRTRoles();
    saveChangesButton.disabled = true;
    for(let i = 0; i < allRoleSelectors.length; ++i){
        for(let z=0; z < allRoleSelectors[i].length; ++z){
            if(allRoleSelectors[i][z].defaultSelected === true){
                console.log(allRoleSelectors[i][z].defaultSelected);
                allRoleSelectors[i].value = allRoleSelectors[i][z].value;
            }
        }
    }
}

function roleSelectorValueChanged(){
    saveChangesButton.disabled = false;
}

function saveChangesButtonClicked(){
    let userNameValueObject = {};
    let xml = new XMLHttpRequest();
    Array.from(allRoleSelectors).forEach((element) =>{
        userNameValueObject[element.id.split("__")[1].trim()] = element.value;
    });
    let dataToSend = JSON.stringify(userNameValueObject);
    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200){
            let returnValue = JSON.parse(xml.responseText);
            if(returnValue["status"] == "success"){
                let insertAt = document.getElementById("error-flash");
                insertAt.innerHTML = returnValue["html"]
                saveChangesButton.disabled = true;
            }
        }
    }
    Helper.httpRequest(xml, "POST", window.location.href + "/updateUserRoles", onReadyFunc, dataToSend);
}

function loadButtonWRTRoles(){
    let currentRoleDefinition;
    let xml = new XMLHttpRequest();
    let urlList = window.location.href.split('/')
    let projectName = urlList[urlList.length - 1];
    let dataToSend = JSON.stringify({
        "project_name": `${projectName}`,
    });
    let onReadyFunc = () => {
        if(xml.readyState == 4 && xml.status == 200){
            currentRoleDefinition = JSON.parse(xml.responseText);
            if (currentRoleDefinition['role_name'] === 'admin'){
                saveChangesButton.disabled = true;
            } else{
                let insertAt = document.getElementById("save-btn-container");
                insertAt.innerHTML = "PERMISSION DENIED";
            }
        }
    }

    Helper.httpRequest(xml, "POST", `/authorised/dash/main/${projectName}/getUserRoleDefinition`, onReadyFunc, dataToSend);
}
