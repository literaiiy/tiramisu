// starting with all these varible sand rcrap
var guildTable = document.getElementById('guildTable')
var row = guildTable.insertRow(0);
var cella = row.insertCell(0);
var cellb = row.insertCell(1);
var cellc = row.insertCell(2);
var celld = row.insertCell(3);
var celle = row.insertCell(4);
var cellf = row.insertCell(5);

// requests


cella.innerHTML = '{{items[0]}}';
// broken one eeh
cellc.innerHTML = '{{items[1]["joined"]}}';
celld.innerHTML = '{{items[1]["guildRank"]}}';
celle.innerHTML = '{{items[1]["expPastWeek"]}}';
cellf.innerHTML = '{{items[1]["quests"]}}';