const specialCases = {
    "graphics": "Integrated Graphics",
    "smt": "SMT",
    "latency": "CAS Latency",
}

function onLoadDashboard(component) {
    window.location.href = '/products/' + component;
}

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
        const name = data[i].name;
        delete data[i].name;
        tableString = tableString + "<tr><td class='name-cell'>" + name + "</td>";
        // const price = data[i].price ? data[i].price : "-";
        // delete data[i].price;
        for (let prop in data[i]) {
            const value = data[i][prop] ?? "-";
            tableString = tableString + "<td>" + value + "</td>";
        }
        tableString = tableString + "<td class='price-cell'></td>";
        tableString = tableString + "<td><button class='btn btn--full'>Add</button></td></tr>";
    }
    tableString = tableString + "</tbody>";
    $('#parts-list').html(tableString);

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
        dataType: "json",
        success: function (res) {
            return res;
        },
        error: function (err) {
            console.log(err);
        }
    });
}
