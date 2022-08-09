var selectedColumn = 'damage';
var selectedRoles = ['Assassin', 'Guardian', 'Hunter', 'Mage', 'Warrior'];
var selectedMode = '435';
var allTables = {};
var godNames;
var godRoles;
var modes = {426: "Conquest", 435: "Arena", 448: "Joust", 445: "Assault", 10195: "Under 30 Arena",
    451: "Conquest Ranked", 10193: "Under 30 Conquest", 10197: "Under 30 Joust", 450: "Joust Ranked",
    10189: "Slash", 440: "Duel Ranked"};
var checkboxes;
var roleSelectButton;
function load(gods, roles, tables) {
    godNames = gods;
    godRoles = roles;
    allTables = tables;
    checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = true;
        checkbox.addEventListener('click', selectRole);
    });
    roleSelectButton = document.getElementById('role-select-button');
    roleSelectButton.addEventListener('click', selectAllRoles);
    generateTable();
}
function selectColumn(column) {
    selectedColumn = column;
    generateTable();
}
function selectMode(mode) {
    selectedMode = mode;
    generateTable();
}
function selectRole(event) {
//    selectedRoles = role;
    console.log(event);
    checkboxes.forEach(checkbox => {
        console.log(checkbox.checked);
    });
    generateTable();
}
function selectAllRoles() {
    if (selectedRoles.length == 5) {
        selectedRoles = [];
        checkboxes.forEach(checkbox => checkbox.checked = false);
    } else {
        selectedRoles = ['Assassin', 'Guardian', 'Hunter', 'Mage', 'Warrior'];
        checkboxes.forEach(checkbox => checkbox.checked = true);
    }
}
function generateTable() {
//    console.log(selectedRoles);
    document.getElementById("mode-select-button").innerHTML = modes[selectedMode];
    document.getElementById("column-select-button").innerHTML = selectedColumn.replace(/^\w/, (c) => c.toUpperCase());
    tds = document.getElementsByClassName("data-column");
    trs = document.getElementsByClassName("data-row");
    values = allTables[selectedMode][selectedColumn].flat();
    for (let i = 0; i < tds.length; i++) {
        var row = Math.floor(i/3);
        if (!selectedRoles.includes(godRoles[godNames[row]])) {
            trs[row].style.display = "none";
        } else {
            trs[row].style.display = "table-row";
        }
        tds[i].innerHTML = values[i];
        tds[i].style.textDecoration = "none";

        if (i % 3 == 2) {
            biggest = tds[i];
            if (tds[i-1].innerHTML > tds[i].innerHTML) {
                biggest = tds[i-1];
                if (tds[i-2].innerHTML > tds[i-1].innerHTML) {
                    biggest = tds[i-2];
                }
            } else if (tds[i-2].innerHTML > tds[i].innerHTML) {
                biggest = tds[i-2];
            }
            if (biggest.innerHTML != 0) {
                biggest.style.textDecoration = "underline";
            }
        }
    }
}