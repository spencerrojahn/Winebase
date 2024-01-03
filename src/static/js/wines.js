

function onPageLoadWineList(username) {
    // Generate the URL for the internal route with the user parameter
    var wines_api_url = "/apis/wines/" + username;

    // Use the Fetch API to make the internal GET request
    fetch(wines_api_url)
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            // Create HTML elements to display the result
            var table_body = document.getElementById('wines-table-body');
            console.log(data)

            // Iterate through the list of lists and create rows
            data.forEach(list => {
                // Create a new row
                var row = table_body.insertRow();

                // Iterate through the items in the list and create cells
                list.forEach(item => {
                    var cell = row.insertCell();
                    cell.textContent = item;
                });
            });

        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);

            // Display an error message
            var resultContainer = document.getElementById('wines-table-body');
        });
}


function onPageLoad() {
    // Get the user information from the data attribute of the link or any other source
    var username = document.getElementById('header-username').textContent;

    // Call the function to make the internal API request on page load
    onPageLoadWineList(username);
}



// Attach the onPageLoad function to the window.onload event
window.onload = onPageLoad;