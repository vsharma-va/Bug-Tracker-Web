let allRoleSelectors = document.getElementsByClassName("user_roles");
Array.from(allRoleSelectors).forEach((element) => {
    element.addEventListener("change", roleSelectorValueChanged);
});

let saveChangesButton = document.getElementById("save-changes-button");
saveChangesButton.addEventListener("click", saveChangesButtonClicked);

window.onload = () => {
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
        console.log(element.id);
        console.log(element.value);
        userNameValueObject[element.id.split("__")[1].trim()] = element.value;
    });
    let dataToSend = JSON.stringify(userNameValueObject);
    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200){
            console.log("ok");
        }
    }
}
