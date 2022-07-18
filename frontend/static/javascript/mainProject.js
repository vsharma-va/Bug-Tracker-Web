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
    }).disableSelection();

    inProgress = $("#in-progress").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
        start: updateOriginalOrders,
    }).disableSelection();

    toBeTested = $("#to-be-tested").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
        start: updateOriginalOrders,
    }).disableSelection();

    clos = $("#closed").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
        start: updateOriginalOrders,
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
    // you can find out about all the properties by printing ui.item to the console
    let allChildren = ui.item['0'].children;
    // console.log(allChildren);
    // console.log(event.target.id);
    // console.log(allChildren.tag.textContent);
    // console.log(allChildren.tag.style.cssText.split(":")[1].replaceAll(";", "").trim());

    console.log(columnName);
    let sorted = $(`#${columnName}`).sortable("serialize");
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

    console.log(`${originalOrder} -> ${eventType}`);
    console.log(`${sorted} -> ${eventType}`);

    // post request. Used to update the database.
    let xml = new XMLHttpRequest();
    xml.open("POST", window.location.href + `/on/${eventType}`, true);
    xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    // new_order and original_order are the results of sortable("serialize")
    let dataToSend = JSON.stringify({
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
    xml.send(dataToSend);
    /*
        plans to fix drag and drop wrt database
        return some value from flask function when the database is updated
        Then update the page by using ajax so that html ids are correct and wrong elements are not added or deleted
    */
    // updatePage is used to update the ids of the divs so that wrong elements are not removed or added
    xml.onreadystatechange = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            if (xml.responseText === "receive") {
                updatePage();
            }
        }
    }

}

function updatePage() {
    let xml = new XMLHttpRequest();
    xml.open("GET", `${window.location.href}/update`, true);
    xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xml.onreadystatechange = () => {
        if (xml.readyState == 4 && xml.status == 200) {
            // cardHtml is a dictionary sent from flask {'column_name': datainlist}
            let cardHtml = JSON.parse(xml.responseText);
            let allColumns = document.getElementsByClassName("sortable ui-sortable");
            Array.from(allColumns).forEach((element) => {
                let totalValue = "";
                cardHtml[element.id].forEach((value) => {
                    totalValue += value;
                });
                element.innerHTML = totalValue;
            });
        }
    }

    xml.send(null);
}

function cardClicked() {
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
