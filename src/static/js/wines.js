

function sendWinesGetRequest(sortColumnId, sortOrder, filters, offset, limit) {
    // Generate the URL for the internal route with the user parameter
    var wines_api_url = "/apis/wines";

    var request_body = {
        sort: {
            value: sortColumnId,
            order: sortOrder
        },
        filters: filters,
        offset: offset,
        limit: limit        
    };


    // Use the Fetch API to make the internal GET request
    fetch(wines_api_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request_body)
    })
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
        console.log(data)
        
        // Create HTML elements to display the result
        var table_body = document.getElementById('wines-table-body');
        table_body.innerHTML = '';

        // Iterate through the list of lists and create rows
        data.forEach(list => {
            // Create a new row
            var row = table_body.insertRow();
            
            // Set background collor if drank
            if (list[list.length -1] === true) {
                row.style.backgroundColor = '#eeeeee';
                
            }

            // Iterate through the items in the list and create cells
            list.forEach((item, index) => {
                var cell = row.insertCell();
                
                // set last row to be in the middle and use check mark
                if (index === list.length - 1) {
                    cell.id += 'drank-header';
                    if (item === true) {
                        cell.textContent = '\u2713';
                    } 
                } else {
                    // else set the item normally
                    cell.textContent = item;
                }
            });
        });

    })
    .catch(error => {
        // Handle errors
        console.error('Error:', error);

    });
}


function sortingClick(columnHeaderlink, sortingSpan)  {

    // 1 = unclicked
    // 2 = ascending
    // 3 = descending
    var currentState;
    if (link.style.color === 'black') {
        currentState = 1;
    } else {
        if (sortingSpan.textContent === '\u2191') {
            currentState = 2;
        } else {
            currentState = 3;
        }
    }

    // Iterate through the elements and set the style
    var elementsWithClass = document.querySelectorAll('a.column-header');
    elementsWithClass.forEach(function(element) {
        element.style.color = 'black';
    });

    var sortingSymbols = document.querySelectorAll('span.sorting-symbol');
    sortingSymbols.forEach(function(symbol) {
        symbol.textContent = '-';
    });

    switch (currentState) {
        case 1:
            // move to state 2 ascending
            sortingSpan.textContent = '\u2191';
            columnHeaderlink.style.color = '#797979';

            sendWinesGetRequest(link.id, true, null, 0, 25);
            
            // send get request for ascending for this given column

            break;
        case 2:
            // move to state 3 descending
            sortingSpan.textContent = '\u2193';
            columnHeaderlink.style.color = '#797979';

            sendWinesGetRequest(link.id, false, null, 0, 25);

            // send get request for desc on this given column

            break;
        case 3:
            // move to state 1 unclicked
            sortingSpan.textContent = '\u2191';
            columnHeaderlink.style.color = '#797979';

            sendWinesGetRequest(columnHeaderlink.id, true, null, 0, 25);

            break;
        default:
            break;
    }

}


function onPageLoad() {
    
    // Get the table header element
    var tableHead = document.querySelector('#wines-table-head');

    // Define an array of column names (including names with spaces)
    var columnNames = ['Cellar', 'Bin Location', 'Owner', 'Vintage', 'Varietals', 
                        'Wine Name', 'Winery Name', 'Winery Location',
                        'Vineyard Location', 'Entry Date', 'Drink Date', 'Drank'];

    // Create th elements and append them to the table header
    columnNames.forEach(function(columnName) {
        var th = document.createElement('th');

        // Replace spaces with dashes in the column name for the id attribute
        var columnNameId = columnName.toLowerCase().replace(/\s+/g, '-');

        // Create link element
        var link = document.createElement('a');
        link.style.color = 'black';
        link.id = columnNameId + '-column-sort';
        link.className = 'column-header';

        // Create span elements
        var spanColumnName = document.createElement('span');
        spanColumnName.textContent = columnName;

        var sortingSpan = document.createElement('span');
        sortingSpan.id = columnNameId + '-sort-symbol'
        sortingSpan.className = 'sorting-symbol';
        sortingSpan.textContent = '-';

        // // Initial sorting when created
        if (columnName === 'Drink Date') {
            link.style.color = '#797979';
            sortingSpan.textContent = '\u2191';
        }

        // Append span elements to link
        link.appendChild(spanColumnName);
        link.appendChild(sortingSpan);

        // Add onclick function to the link
        link.onclick = function() {
            sortingClick(link, sortingSpan)
        }

        // Append link to th
        th.appendChild(link);

        // Append th to table header
        tableHead.appendChild(th);
    });

    // SEND INTITIAL with 'Drink Date' sorting

    // Call the function to make the internal API request on page load
    sendWinesGetRequest('drink-date-column-sort', true, null, 0, 25);
    // sendWinesGetRequest(null, null, null, 0, 25);
}



// Attach the onPageLoad function to the window.onload event
window.onload = onPageLoad;