var selectedColumn = 'damage';
var selectedRoles = ['Assassin', 'Guardian', 'Hunter', 'Mage', 'Warrior'];
var selectedMode = '435';
var allTables = {};
var godNames;
var godRoles;
var players;
var modes = {426: "Conquest", 435: "Arena", 448: "Joust", 445: "Assault", 10195: "Under 30 Arena",
    451: "Conquest Ranked", 10193: "Under 30 Conquest", 10197: "Under 30 Joust", 450: "Joust Ranked",
    10189: "Slash", 440: "Duel Ranked"};
var checkboxes;
var roleSelectButton;
function load(gods, roles, tables, tableHeaders) {
    godNames = gods;
    godRoles = roles;
    allTables = tables;
    players = tableHeaders;
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
    var role = event.composedPath()[0].id;
    if (selectedRoles.includes(role)) {
        selectedRoles.splice(selectedRoles.indexOf(role), 1);
    } else {
        selectedRoles.push(role);
    }
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
    generateTable();
}
function generateTable() {
    console.clear();
    if (selectedRoles.length == 0) {
        document.getElementById("role-select-button").style.color = '#dd0000';
    } else {
        document.getElementById("role-select-button").style.color = '#c9d1d9';
    }
    document.getElementById("mode-select-button").innerHTML = modes[selectedMode];
    document.getElementById("column-select-button").innerHTML = selectedColumn.replace(/^\w/, (c) => c.toUpperCase());
    tds = document.getElementsByClassName("data-column");
    trs = document.getElementsByClassName("data-row");
    values = allTables[selectedMode][selectedColumn].flat();
    reigns = {}
    players.forEach(player => reigns[player] = 0);
    for (let i = 0; i < tds.length; i++) {
        var row = Math.floor(i/3);
        if (!selectedRoles.includes(godRoles[godNames[row]])) {
            trs[row].style.display = "none";
        } else {
            trs[row].style.display = "table-row";
            if (i % 3 == 2) {
                biggest = i;
    //            console.log(players[i%3-1]);
                if (tds[i-1].innerHTML > tds[i].innerHTML) {
                    biggest = i-1;
                    if (tds[i-2].innerHTML > tds[i-1].innerHTML) {
                        biggest = i-2;
                    }
                } else if (tds[i-2].innerHTML > tds[i].innerHTML) {
                    biggest = i-2;
                }
                if (tds[biggest].innerHTML != 0) {
                    for (j = 0; j < players.length; j++) {
                        if (i - biggest == j) {
                            name = players[(players.length - 1 - j)];
                            reigns[name] = reigns[name] + 1;
                        }
                    }
                    tds[biggest].style.fontWeight = "bold";
                    tds[biggest].style.letterSpacing = "0.5px";
                }
            }
        }
        tds[i].innerHTML = values[i];
        tds[i].style.textDecoration = "none";
    }
    players.forEach(player => {
       document.getElementById(player + "-reigns").innerHTML = reigns[player];
    });
    console.log(reigns);
}