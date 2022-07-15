$(document).ready(function () {
    $("#open").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        revert: 0.001,
    }).disableSelection();
    
    $("#in-progress").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        revert: 0.001,
    }).disableSelection();

    $("#to-be-tested").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        revert: 0.001,
    }).disableSelection();

    $("#closed").sortable({
        connectWith: ".sortable",
        containment: ".columns",
        cursor: "move",
        revert: 0.001,
    }).disableSelection();
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
function onReceive(event, ui){
    ui.item
}