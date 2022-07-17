let open;
let inProgress;
let toBeTested;
let closed;

let openOriginalOrder;
let inProgressOriginalOrder;
let toBeTestedOriginalOrder;
let closedOriginalOrder;

$(document).ready(function () {
    open = $("#open").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
    }).disableSelection();
    
    inProgress = $("#in-progress").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
    }).disableSelection();

    toBeTested = $("#to-be-tested").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
    }).disableSelection();

    closed = $("#closed").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        receive: onReceiveRemove,
        remove: onReceiveRemove,
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
function onReceiveRemove(event, ui){
    // you can find out about all the properties by printing ui.item to the console
    let allChildren = ui.item['0'].children;
    // console.log(allChildren);
    // console.log(event.target.id);
    // console.log(allChildren.tag.textContent);
    // console.log(allChildren.tag.style.cssText.split(":")[1].replaceAll(";", "").trim());

    let columnName = event.target.id.toString();
    console.log(columnName);
    let sorted = $(`#${columnName}`).sortable("serialize");
    let originalOrder;
    let eventType;
    
    switch (event.type){
        case "sortremove":
            eventType = "remove";
            break;
        case "sortreceive":
            eventType = "receive";
            break;
    }

    switch (columnName){
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
    console.log(originalOrder);
    console.log(sorted);

    let xml = new XMLHttpRequest();
    xml.open("POST", window.location.href + `/on/${eventType}`, true);
    xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
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
    updateOriginalOrders(columnName);
    xml.send(dataToSend);
    /*
        plans to fix drag and drop wrt database
        return some value from flask function when the database is updated
        Then update the page by using ajax so that html ids are correct and wrong elements are not added or deleted
    */
}

function cardClicked(){
    console.log("clicked");
}

function updateOriginalOrders(columnName){
    switch (columnName){
        case "open":
            openOriginalOrder = open.sortable("serialize");
            break;
        case "in-progress":
            inProgressOriginalOrder = inProgress.sortable("serialize");
            break;
        case "to-be-tested":
            toBeTestedOriginalOrder = toBeTested.sortable("serialize");
            break;
        case "closed":
            closedOriginalOrder = closed.sortable("serialize");
            break;
        default:
            openOriginalOrder = open.sortable("serialize");
            inProgressOriginalOrder = inProgress.sortable("serialize");
            toBeTestedOriginalOrder = toBeTested.sortable("serialize");
            closedOriginalOrder = closed.sortable("serialize");
    }
}