const specialCases = {
    "graphics": "Integrated Graphics",
    "smt": "SMT",
    "latency": "CAS Latency",
}

function onLoadDashboard(component) {
    window.location.href = '/products/' + component;
}

let compProduct;

function onLoadPartList(component) {
    fetchPartData(component).then((data) => {
        if (component === "memory") {
            data = data.map((item) => {
                return {
                    "name": item.name,
                    "Count / Size": item.count + " x " + item.size + "GB",
                    "latency": item.latency,
                    "speed": item.speed
                }
            })
        }
        compProduct = component;
        formatPartsTable(data);
    })
}

function formatPartsTable(data) {
    let tableString = "";
    const keys = Object.keys(data[0]);
    const filteredKeys = keys.filter(function(e) { return e !== "name"});
    const mappedKeys = filteredKeys.map(item => {
        return specialCases[item] ?? convertKeyRegex(item);
    });

    tableString = tableString + "<thead><tr><th class='name-column'>Name</th>";
    for (let i = 0; i < mappedKeys.length; i++) {
        tableString = tableString + "<th>" + mappedKeys[i] +"</th>";
    }
    tableString = tableString + "<th class='price-column'>Price</th><th class='add-column'></th></tr></thead><tbody>";
    for (let i = 0; i < 50; i++) {
        const filteredData = data[i];
        const name = filteredData.name;
        delete filteredData.name;
        tableString = tableString + "<tr id='selection__" + i + "'><td class='name-cell'>" + name + "</td>";
        // const price = data[i].price ? data[i].price : "-";
        // delete data[i].price;
        for (let prop of Object.values(filteredData)) {
            if (prop === 1 || prop === 0) {
                const value = prop === 1 ? "Yes" : "No";
                tableString = tableString + "<td>" + value + "</td>";
            } else {
                const value = prop ?? "-";
                tableString = tableString + "<td>" + value + "</td>";
            }

        }
        tableString = tableString + "<td class='price-cell'></td>";
        tableString = tableString + "<td><button class='btn btn--full' onclick='addPartToList("+i+")'>Add</button></td></tr>";
    }
    tableString = tableString + "</tbody>";
    $('#parts-list').html(tableString);
}

function addPartToList(i) {
    const value = $('#selection__' + i + '> .name-cell').html();
    localStorage.setItem(compProduct, value);
    window.location.href = '/parts-dashboard';
}

function removeSelection(key) {
    localStorage.removeItem(key.id);
    $(key).children('.td-selection').html("<button class='btn btn--full' onclick='onLoadDashboard(\""+key.id+"\")'>+ Select</button>");
    $(key).children('.td-remove').remove();
}

function convertKeyRegex(str) {
    var i, frags = str.split('_');
    for (i=0; i<frags.length; i++) {
        frags[i] = frags[i].charAt(0).toUpperCase() + frags[i].slice(1);
    }
    return frags.join(' ');
}

async function fetchPartData(component) {
    const url = "/components/" + component;
    return $.ajax({
        url: url,
        method: "GET",
        dataType: "json"
    });
}

function saveList() {
    const data = fetchData(null);
    if (data.component !== null) {
        $.ajax({
            url: "/save-list",
            method: "POST",
            dataType: "json",
            data: JSON.stringify(data)
        }).done(function(data) {
            console.log(data);
        })
    }
}

function updateList() {
    let id = $('#build-list').prop('selectedIndex');
    const data = fetchData(id);
    if (data.component !== null) {
        $.ajax({
            url: "/save-list",
            method: "POST",
            dataType: "json",
            data: JSON.stringify(data)
        }).done(function(data) {
            console.log(data);
        })
    }
}

function fetchData(id) {
    let data = {
        "component": {
        },
        "id": id
    }
    for (let i = 0; i < localStorage.length; i++) {
        if (localStorage.key(i)) {
            const key = localStorage.key(i);
            const value = localStorage.getItem(key);
            data["component"][key] = value;
        }
    }
    return data;
}
