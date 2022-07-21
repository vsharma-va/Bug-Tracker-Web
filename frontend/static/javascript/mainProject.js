import { Helper } from "./helper/allHelpers.js";

// Global Variables
let opn;
let inProgress;
let toBeTested;
let clos;

let openOriginalOrder;
let inProgressOriginalOrder;
let toBeTestedOriginalOrder;
let closedOriginalOrder;

// defining all sortables
$(document).ready(function () {
    /*
        receive fires when the item is dropped into the sortable
        remove fires when the item is dropped into another sortable
        remove event takes place before receive
        start fires when the item is dragged
    */
    opn = $("#open").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
        start: updateOriginalOrders,
        cancel: ".column-name",
    }).disableSelection();

    inProgress = $("#in-progress").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
        start: updateOriginalOrders,
        cancel: ".column-name",
    }).disableSelection();

    toBeTested = $("#to-be-tested").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
        start: updateOriginalOrders,
        cancel: ".column-name",
    }).disableSelection();

    clos = $("#closed").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
        start: updateOriginalOrders,
        cancel: ".column-name",
    }).disableSelection();

    updateOriginalOrders();
});

/* 
    use receive event in jquery sortable
    get item. store values of the item in a json
    use serialize to get updated order
    send json to flask. do crud

    also use remove event in jquery sortable
    get item. get project id.
    send to flask. remove from projectData where project_id = json
*/
function onReceiveRemove(event, ui) {
    let columnName = event.target.id.toString();
    let sorted = $(`#${columnName}`).sortable("serialize");
    // console.log($(`#${columnName}`).sortable("toArray", {attribute: "data-id"}));
    let idInOrder = $(`#${columnName}`).sortable("toArray", {attribute: "data-id"});
    idInOrder.splice(0, 1);

    // you can find out about all the properties by printing ui.item to the console
    let allChildren = ui.item['0'].children;
    // console.log(ui.item['0'].dataset['id']);
    // console.log(event.target.id);
    // console.log(allChildren.tag.textContent);
    // console.log(allChildren.tag.style.cssText.split(":")[1].replaceAll(";", "").trim());

    let originalOrder;
    let eventType;

    switch (event.type) {
        case "sortremove":
            eventType = "remove";
            break;
        case "sortreceive":
            eventType = "receive";
            break;
    }

    switch (columnName) {
        case "open":
            originalOrder = openOriginalOrder;
            break;
        case "to-be-tested":
            originalOrder = toBeTestedOriginalOrder;
            break;
        case "in-progress":
            originalOrder = inProgressOriginalOrder;
            break;
        case "closed":
            originalOrder = closedOriginalOrder;
            break;
    }

    // post request. Used to update the database.
    let xml = new XMLHttpRequest();
    // new_order and original_order are the results of sortable("serialize")
    let dataToSend = JSON.stringify({
        "id": ui.item["0"].dataset["id"].toString(),
        "id_in_order": idInOrder.toString(),
        "tag": allChildren.tag.textContent,
        "tag_color": allChildren.tag.style.cssText.split(":")[1].replaceAll(";", "").trim(),
        "column": allChildren.column.textContent,
        "description": allChildren.description.textContent,
        "by": allChildren.by.textContent,
        "received_by": event.target.id,
        "new_order": sorted,
        "original_order": originalOrder,
        "event_type": eventType,
    });
    /*
        plans to fix drag and drop wrt database
        return some value from flask function when the database is updated
        Then update the page by using ajax so that html ids are correct and wrong elements are not added or deleted
    */
    // updatePage is used to update the ids of the divs so that wrong elements are not removed or added
    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            if (xml.responseText === "receive") {
                updatePage();
            }
        }
    }
    let url = window.location.href + `/on/${eventType}`
    Helper.httpRequest(xml, "POST", url, onReadyFunc, dataToSend);

}

function updatePage() {
    let xml = new XMLHttpRequest();

    let onReadyFunc = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            // cardHtml is a dictionary sent from flask {'column_name': datainlist}
            let cardHtml = JSON.parse(xml.responseText);
            let allColumns = document.getElementsByClassName("sortable ui-sortable");
            Array.from(allColumns).forEach((element) => {
                let totalValue = "";
                cardHtml[element.id].forEach((value) => {
                    totalValue += value;
                });
                totalValue = `<p class='column-name'>${element.id.toUpperCase().replaceAll("-", " ")}</p> \n` + totalValue;
                element.innerHTML = totalValue;
            });
        }
    }
    Helper.httpRequest(xml, "GET", `${window.location.href}/update`, onReadyFunc);
}

function updateOriginalOrders(columnName) {
    switch (columnName) {
        case "open":
            openOriginalOrder = opn.sortable("serialize");
            break;
        case "in-progress":
            inProgressOriginalOrder = inProgress.sortable("serialize");
            break;
        case "to-be-tested":
            toBeTestedOriginalOrder = toBeTested.sortable("serialize");
            break;
        case "closed":
            closedOriginalOrder = clos.sortable("serialize");
            break;
        default:
            openOriginalOrder = opn.sortable("serialize");
            inProgressOriginalOrder = inProgress.sortable("serialize");
            toBeTestedOriginalOrder = toBeTested.sortable("serialize");
            closedOriginalOrder = clos.sortable("serialize");
    }
}

setInterval(updatePage, 40000);

let allCards = document.getElementsByClassName("card");
Array.from(allCards).forEach((element) => {
    element.addEventListener("click", cardOnClick, false);
});


function cardOnClick(event){
    let clickedElement = event.target;
    let columnAndPosition = clickedElement.id.split("_");
    let xml = XMLHttpRequest()
    Helper.httpRequest(xml, "GET", window.location.href + "loadoverlay");
}