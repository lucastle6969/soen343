function removeItem(button){
    let table = document.getElementById("physical-item-table");
    let row = button.parentNode.parentNode;
    let index = row.rowIndex;
    if(row.dataset.physicalcopyid){
        modifyDeletedItems(row.dataset.physicalcopyid);
    } else {
        modifyNewItemCount(-1);
    }
    table.deleteRow(index);
}

function addItem(){
    let table = document.getElementById("physical-item-table");
    let row = table.insertRow(-1);
    let status = row.insertCell(0);
    status.innerHTML = "Available"
    row.insertCell(1); // Return date - none is needed for newly created items
    let button = row.insertCell(2);
    button.innerHTML = "<button type=\"button\" class=\"btn btn-secondary\" onclick=\"removeItem(this)\">Remove</button>";
    modifyNewItemCount(1);
}

function modifyNewItemCount(amount){
    let addCounter = document.getElementById("physicalAdd");
    let value = parseInt(addCounter.value);
    value += amount;
    addCounter.value = value
}

function modifyDeletedItems(id){
    let deletedGroup = document.getElementById("physicalDelete");
    let input = document.createElement("input");
    input.type = "hidden";
    input.name = "physical_items_removed";
    input.value = id
    deletedGroup.appendChild(input);
}


