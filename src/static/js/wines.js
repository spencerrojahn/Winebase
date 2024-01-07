
async function sendWinesListPostRequest(sortColumnId, sortOrder, filters, offset, limit) {
    const wines_list_api_url = "/api/wines/list"
    const request_body = {
        sort: {
            value: sortColumnId,
            order: sortOrder
        },
        filters: filters,
        offset: offset,
        limit: limit        
    }

    // Returning the fetch call directly, it already returns a Promise
    try {
        const response = await fetch(wines_list_api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request_body)
        })
        // Check if the response status is okay
        if (!response.ok) {
            throw new Error('Network response was not ok')
        }
        return await response.json()
    } catch (error) {
        console.error('Error fetching wines data:', error)
        // Throw the error again to propagate it
        throw error
    }
}

async function sendWinesAddPostRequest(request_body) {
    const wines_add_api_url = "/api/wines/add"

    // Returning the fetch call directly, it already returns a Promise
    try {
        const response = await fetch(wines_add_api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request_body)
        })
        // Check if the response status is okay
        if (!response.ok) {
            throw new Error('Network response was not ok')
        }
        return await response.json()
    } catch (error) {
        console.error('Error fetching wines data:', error)
        // Throw the error again to propagate it
        throw error
    }
}




async function populateWinesTable(sortColumnId, sortOrder, filters, offset, limit) {
    // Generate the URL for the internal route with the user parameter
    try {
        const data = await sendWinesListPostRequest(sortColumnId, sortOrder, filters, offset, limit)
        console.log(data)
            
        // Create HTML elements to display the result
        var table_body = document.getElementById('wines-table-body')
        table_body.innerHTML = ''
    
        // Iterate through the list of lists and create rows
        data.forEach(list => {
            // Create a new row
    
            var row = table_body.insertRow()
            
            // Set background collor if drank
            if (list[list.length -1] === true) {
                row.style.backgroundColor = '#eeeeee'
                
            }
    
            // Iterate through the items in the list and create cells
            list.forEach((item, index) => {
                
                // first index is the WineEntry id
                if (index > 0) {
                    var cell = row.insertCell()
                    // set last row to be in the middle and use check mark
                    if (index === list.length - 1) {
                        cell.id += 'drank-header'
                        if (item === true) {
                            cell.textContent = '\u2713'
                        } 
                    } else {
                        // else set the item normally
                        cell.textContent = item
                    }
                }
                
            })
            
            // Create a new anchor element
            var link = document.createElement('a')
            link.className = "wine-detail-row-link"
    
            // The id contains the WineEntry.id from this given row entry (so that it can be used later
            // on for fetching the details for this given WineEntry)
            link.id = 'wine-detail-row-link_' + list[0]
            
            // Set the href attribute to your desired URL
            link.href = '#'
            // Set any other necessary attributes or styles for the link
            link.textContent = 'Details' // Set the link text
    
            // Create a cell for the link and append the link to it
            var linkCell = row.insertCell()
            linkCell.style.textAlign = 'center'
            linkCell.appendChild(link)
    
        })
    } catch (error) {
        console.error('Error in populateWinesTable:', error)


    }
    
}


async function sortingClick(columnHeaderlink, sortingSpan)  {

    // 1 = unclicked
    // 2 = ascending
    // 3 = descending
    var currentState
    if (columnHeaderlink.style.color === 'black') {
        currentState = 1
    } else {
        if (sortingSpan.textContent === '\u2191') {
            currentState = 2
        } else {
            currentState = 3
        }
    }

    // Iterate through the elements and set the style
    var elementsWithClass = document.querySelectorAll('a.column-header')
    elementsWithClass.forEach(function(element) {
        element.style.color = 'black'
    })

    var sortingSymbols = document.querySelectorAll('span.sorting-symbol')
    sortingSymbols.forEach(function(symbol) {
        symbol.textContent = '-'
    })

    switch (currentState) {
        case 1:
            // move to state 2 ascending
            sortingSpan.textContent = '\u2191'
            columnHeaderlink.style.color = '#797979'

            await populateWinesTable(columnHeaderlink.id, true, null, 0, 25)
            
            // send get request for ascending for this given column

            break
        case 2:
            // move to state 3 descending
            sortingSpan.textContent = '\u2193'
            columnHeaderlink.style.color = '#797979'

            await populateWinesTable(columnHeaderlink.id, false, null, 0, 25)

            // send get request for desc on this given column

            break
        case 3:
            // move to state 1 unclicked
            sortingSpan.textContent = '\u2191'
            columnHeaderlink.style.color = '#797979'

            await populateWinesTable(columnHeaderlink.id, true, null, 0, 25)

            break
        default:
            break
    }

}


function handleAddWine() {
    
    // document.getElementById('entry-date-location-input').value = getToday()

    const popupOverlay = document.getElementById('popupOverlay')
    popupOverlay.style.display = 'flex'
}

function closeAddWinePopup() {
    const popupOverlay = document.getElementById('popupOverlay')
    popupOverlay.style.display = 'none'
}




async function onPageLoad() {
    
    // Get the table header element
    var tableHead = document.querySelector('#wines-table-head')

    // Define an array of column names (including names with spaces)
    var columnNames = ['Cellar', 'Bin Location', 'Owner', 'Vintage', 'Varietal(s)', 
                        'Wine Name', 'Winery Name', 'Winery Location',
                        'Vineyard Location', 'Entry Date', 'Drink Date', 'Drank', "Details"]

    // Create th elements and append them to the table header
    columnNames.forEach(function(columnName) {
        var th = document.createElement('th')

        // Replace spaces with dashes in the column name for the id attribute
        var columnNameId = columnName.toLowerCase().replace(/\s+/g, '-').replace(/[()]/g,'')

        // Create link element
        var link = document.createElement('a')
        link.style.color = 'black'
        link.id = columnNameId + '-column-sort'
        link.className = 'column-header'

        // Create span elements
        var spanColumnName = document.createElement('span')
        spanColumnName.textContent = columnName

        var sortingSpan = document.createElement('span')
        sortingSpan.id = columnNameId + '-sort-symbol'
        sortingSpan.className = 'sorting-symbol'
        sortingSpan.textContent = '-'
        

        // // Initial sorting when created
        if (columnName === 'Drink Date') {
            link.style.color = '#797979'
            sortingSpan.textContent = '\u2191'
        }

        // Append span elements to link
        link.appendChild(spanColumnName)

        if (columnName !== 'Details') {
            link.appendChild(sortingSpan)

            // Add onclick function to the link
            link.onclick = function() {
                sortingClick(link, sortingSpan)
            }

        }
        

        // Append link to th
        th.appendChild(link)

        // Append th to table header
        tableHead.appendChild(th)
    })

    // SEND INTITIAL with 'Drink Date' sorting

    // Call the function to make the internal API request on page load
    await populateWinesTable('drink-date-column-sort', true, null, 0, 25)
    // sendWinesGetRequest(null, null, null, 0, 25)
}


// function getToday() {
//     const today = new Date()
//     const year = today.getFullYear()
//     const month = String(today.getMonth() + 1).padStart(2, '0')
//     const day = String(today.getDate()).padStart(2, '0')
//     return `${year}-${month}-${day}`
// }

// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('entry-date-location-input').value = getToday()
// })


function hideNewOwnerInputFields() {

    document.getElementById('add-wine-submit').disabled = true
    
    document.getElementById('owner-input').classList.add('invalid-input')
    document.getElementById('vintage-input').classList.add('invalid-input')
    document.getElementById('varietals-input').classList.add('invalid-input')
    document.getElementById('winery-name-input').classList.add('invalid-input')
    document.getElementById('entry-date-location-input').classList.add('invalid-input')
    

    document.getElementById('wine-name-input').classList.remove('invalid-input')
    document.getElementById('winery-location-input').classList.remove('invalid-input')
    document.getElementById('vineyard-location-input').classList.remove('invalid-input')
    document.getElementById('acquisition-info-input').classList.remove('invalid-input')
    document.getElementById('personal-notes-input').classList.remove('invalid-input')
    document.getElementById('expert-rater-name-input').classList.remove('invalid-input')
    document.getElementById('expert-rating-input').classList.remove('invalid-input')
    document.getElementById('personal-rating-input').classList.remove('invalid-input')


    var conditionalElements = document.querySelectorAll('.add-wine-details-form-group.new-owner')
    // Hide the conditional element
    conditionalElements.forEach(function (element) {
        element.style.display = 'none'
    })
}

document.addEventListener('DOMContentLoaded', function () {
    var selectElement = document.getElementById('owner-input')
    // Get the conditional element
    // Add event listener to the select element
    selectElement.addEventListener('input', function () {
        // Check if Option 2 is selected

        var conditionalElements = document.querySelectorAll('.add-wine-details-form-group.new-owner')
        
        if (selectElement.value === 'new-owner') {
            // Show the conditional element
            conditionalElements.forEach(function (element) {
                element.style.display = 'flex'
            })
        } else {
            // Hide the conditional element
            conditionalElements.forEach(function (element) {
                element.style.display = 'none'
            })
        }
    })
})


window.addEventListener('resize', function () {
    var minWidth = 1000


    // Check if the window width is less than the minimum
    if (window.innerWidth < minWidth) {
        // Enforce the minimum width 
        var wineDeta = document.querySelectorAll('.add-wine-details-form-group, .add-wine-details-form-control, .add-wine-info-form-control')

        wineDeta.forEach(function (element) {
            element.style.fontSize = '10px'
        })

        var newOwner = document.querySelectorAll('.new-owner')

        newOwner.forEach(function (element) {
            element.style.fontSize = '9px'
        })
    } else {
        var wineDeta = document.querySelectorAll('.add-wine-details-form-group, .add-wine-details-form-control, .add-wine-info-form-control')

        wineDeta.forEach(function (element) {
            element.style.fontSize = '14px'
        })

        var newOwner = document.querySelectorAll('.new-owner')

        newOwner.forEach(function (element) {
            element.style.fontSize = '11px'
        })
    }
    
})



// ADD WINE FORM VALIDATIONS

// document.getElementById('bin-location-input').addEventListener('blue', function() {
//     var inputValue = this.value

// })


function isValidCellarLocation() {
    var cellarInputValue = document.getElementById('cellar-input').value
    var binLocationInputValue = document.getElementById('bin-location-input').value.trim()
    if (cellarInputValue !== '') {
        // If cellar is not blank, then if bin location is blank --> invalid
        if (binLocationInputValue === '') {
            document.getElementById('bin-location-input').classList.add('invalid-input')
            return false
        } else {
            document.getElementById('cellar-input').classList.remove('invalid-input')

            // If cellar is not blank, then if bin location is NOT blank --> valid
            var pattern = /^[A-Z]\d-[FB]$/

            if (pattern.test(binLocationInputValue)) {
                document.getElementById('bin-location-input').classList.remove('invalid-input')

                // need to do lookup here for availability:

            } else {
                document.getElementById('bin-location-input').classList.add('invalid-input')
                return false
            }   

            return true

            // need to do cellar lookup here to see if location is fine


        }
        
    } else {
        if (binLocationInputValue !== '') {
            // If cellar is blank, then if bin location is NOT blank --> invalid

            var pattern = /^[A-Z]\d-[FB]$/

            if (pattern.test(binLocationInputValue)) {
                document.getElementById('bin-location-input').classList.remove('invalid-input')
                document.getElementById('cellar-input').classList.add('invalid-input')

                // need to do lookup here for availability:

            } else {
                document.getElementById('bin-location-input').classList.add('invalid-input')
                document.getElementById('cellar-input').classList.remove('invalid-input')
                return false
            }  
            return false
        } else {
            document.getElementById('bin-location-input').classList.remove('invalid-input')
            document.getElementById('cellar-input').classList.remove('invalid-input')
        }
        // If cellar is blank, then if bin location is blank --> valid
    }
    return true
}

function isOwnerValid() {
    var ownerInput = document.getElementById('owner-input')

    var newOwnerName = document.getElementById('new-owner-name-input')
    var newOwnerInitials = document.getElementById('new-owner-initials-input')
    var newOwnerColor = document.getElementById('new-owner-color-input')

    if (ownerInput.value !== '') {
        ownerInput.classList.remove('invalid-input')

        if (ownerInput.value === 'new-owner') {
            
            valid = true
            if (newOwnerName.value !== '' && newOwnerName.value.length <= 40) {
                newOwnerName.classList.remove('invalid-input')
            } else {
                newOwnerName.classList.add('invalid-input')
                valid = false
            }

            if (newOwnerInitials.value !== '' 
                && newOwnerInitials.value.length <= 4
                && /^[A-Z]+$/.test(newOwnerInitials.value)) {
                newOwnerInitials.classList.remove('invalid-input')
            } else {
                newOwnerInitials.classList.add('invalid-input')
                valid = false
            }

            if (newOwnerColor.value !== '') {
                newOwnerColor.classList.remove('invalid-input')
            } else {
                newOwnerColor.classList.add('invalid-input')
                valid = false
            }

            return valid

        } else {
            return true
        }
    } else {
        ownerInput.classList.add('invalid-input')
        return false
    }
}

function isValidVintage() {
    var vintageInput = document.getElementById('vintage-input')

    if (vintageInput.value !== ''
        && /^(19\d{2}|20\d{2})$/.test(vintageInput.value)
        && parseInt(vintageInput.value, 10) <= new Date().getFullYear()
        ) {
        vintageInput.classList.remove('invalid-input')
        return true
    } else {
        vintageInput.classList.add('invalid-input')
        return false
    }
}

function isValidVarietals() {
    var varietalsInput = document.getElementById('varietals-input')
    if (varietalsInput.value != '' && varietalsInput.value.length <= 255) {
        varietalsInput.classList.remove('invalid-input')
        return true
    } else {
        varietalsInput.classList.add('invalid-input')
        return false
    }
}


function isValidWineryName() {
    var wineryNameInput = document.getElementById('winery-name-input')
    if (wineryNameInput.value != '' && wineryNameInput.value.length <= 255) {
        wineryNameInput.classList.remove('invalid-input')
        return true
    } else {
        wineryNameInput.classList.add('invalid-input')
        return false
    }

}

function isValidEntryDate() {
    var entryDateInput = document.getElementById('entry-date-location-input')
    if (entryDateInput.value != '') {
        // Convert the input string to a Date object
        var entryDate = new Date(entryDateInput.value)
            
        // Get the current date
        var currentDate = new Date()
        currentDate.setHours(0, 0, 0, 0)

        if (entryDate <= currentDate) {
            entryDateInput.classList.remove('invalid-input')
            return true
        } else {
            entryDateInput.classList.add('invalid-input')
            return false
        }

    } else {
        entryDateInput.classList.add('invalid-input')
        return false
    }
}

function isValidDrinkDate() {
    var drinkDateInput = document.getElementById('drink-date-location-input')
    var drankInput = document.getElementById('drank-input')

    var drinkDate = new Date(drinkDateInput.value)

    // Get the current date
    var currentDate = new Date()
    currentDate.setHours(0, 0, 0, 0)

    if (drankInput.value === 'NO') {
        if (drinkDate <= currentDate) {
            drinkDateInput.classList.add('invalid-input')
            return false
        }
    } else {
        // drank is yes
        if (drinkDate > currentDate) {
            drinkDateInput.classList.add('invalid-input')
            return true
        } 
    }
    
    drinkDateInput.classList.remove('invalid-input')
    return true
}

function validateOptionalTextField(input, inputMaxLength) {
    if (input.value !== '' && input.value.length > inputMaxLength) {
        input.classList.add('invalid-input')
        return false
    }

    input.classList.remove('invalid-input')
    return true
}

function optionalTextFieldsValidation() {
    var list = [
        [document.getElementById('wine-name-input'), 150],
        [document.getElementById('winery-location-input'), 500],
        [document.getElementById('vineyard-location-input'), 500],
        [document.getElementById('acquisition-info-input'), 1000],
        [document.getElementById('personal-notes-input'), 1000]
    ]

    list.forEach(item => {
        if (!validateOptionalTextField(item[0], item[1])) {
            return false
        }
    })
    return true
}      

function validateExpertRating() {
    var expertRaterNameInput = document.getElementById('expert-rater-name-input')
    var expertRatingInput = document.getElementById('expert-rating-input')

    if (expertRaterNameInput.value === '') {
        if (expertRatingInput.value === '') {
            expertRaterNameInput.classList.remove('invalid-input')
            expertRatingInput.classList.remove('invalid-input')
            return true
        } else {
            // Rating is present but no name
            if (expertRatingInput.value > 101 || expertRatingInput.value < 50) {
                expertRaterNameInput.classList.remove('invalid-input')
                expertRatingInput.classList.add('invalid-input')
                return false
            } else {
                expertRaterNameInput.classList.add('invalid-input')
                expertRatingInput.classList.remove('invalid-input')
                return false
            }
        }
    } else if (expertRaterNameInput.value.length > 150) {
        expertRaterNameInput.classList.add('invalid-input')
        expertRatingInput.classList.remove('invalid-input')
        return false
    } else {
        if (expertRatingInput.value !== '' && expertRatingInput.value <= 100 && expertRatingInput.value >= 50) {
            expertRaterNameInput.classList.remove('invalid-input')
            expertRatingInput.classList.remove('invalid-input')
            return true
            
        } else {
            expertRaterNameInput.classList.remove('invalid-input')
            expertRatingInput.classList.add('invalid-input')
            return false
        }
    }
    
}

function validatePersonalRating() {
    var personalRatingInput = document.getElementById('personal-rating-input')

    if (personalRatingInput.value !== '' && (personalRatingInput.value > 5 || personalRatingInput.value < 1)) {
        personalRatingInput.classList.add('invalid-input')
        return false
    } 
    personalRatingInput.classList.remove('invalid-input')
    return true
}


document.addEventListener('DOMContentLoaded', function () {

    // Set the button to disabled by default
    document.getElementById('add-wine-submit').disabled = true 


    // Add an event listener for input changes
    document.getElementById('form-add-wine').addEventListener('input', function () {
        // Validate each input field based on your criteria

        // Validate bin location
        var validCellarLocation = isValidCellarLocation()
        var validOwner = isOwnerValid()
        var validVintage = isValidVintage()
        var validVarietals = isValidVarietals()
        var validWineryName = isValidWineryName()
        var validEntryDate = isValidEntryDate()
        var validDrinkDate = isValidDrinkDate()
        var validExperRating = validateExpertRating()
        var validPersonalRating = validatePersonalRating()
        var validOptionalTextFields = optionalTextFieldsValidation()

        // // Enable or disable the submit button based on validation results
        document.getElementById('add-wine-submit').disabled = !(validCellarLocation && validOwner 
                                                                && validVintage && validVarietals 
                                                                && validWineryName && validOptionalTextFields
                                                                && validEntryDate && validDrinkDate 
                                                                && validExperRating && validPersonalRating)
    })

})

document.addEventListener('DOMContentLoaded', function () {
    
    document.getElementById('form-add-wine').addEventListener('submit', async function (submitEvent) {
        
        submitEvent.preventDefault()
        
        // Get form data
        // const formData = new FormData(submitEvent.target)
        // const cellar = formData.get('cellar-input').options[]

        // Make API request
        
        // const cellar = document.getElementById('cellar-input').value

        try {
            const request_body = { 
                cellar: document.getElementById('cellar-input').value,
                binLocation: document.getElementById('bin-location-input').value,
                owner: document.getElementById('owner-input').value,
                newOwnerName: document.getElementById('new-owner-name-input').value,
                newOwnerInitials: document.getElementById('new-owner-initials-input').value,
                newOwnerColor: document.getElementById('new-owner-color-input').value,
                vintage: document.getElementById('vintage-input').value,
                varietals: document.getElementById('varietals-input').value,
                wineName: document.getElementById('wine-name-input').value,
                wineryName: document.getElementById('winery-name-input').value,
                wineryLocation: document.getElementById('winery-location-input').value,
                vineyardLocation: document.getElementById('vineyard-location-input').value,
                entryDate: document.getElementById('entry-date-location-input').value,
                drank: document.getElementById('drank-input').value,
                drinkDate: document.getElementById('drink-date-location-input').value,
                aquisitionInfo: document.getElementById('acquisition-info-input').value,
                personalNotes: document.getElementById('personal-notes-input').value,
                purchasePrice: document.getElementById('purchase-price-input').value.replace('$', ''),
                expertRaterName: document.getElementById('expert-rater-name-input').value,
                expertRating: document.getElementById('expert-rating-input').value,
                personalRating: document.getElementById('personal-rating-input').value
            }
    
            const data = await sendWinesAddPostRequest(request_body)

            console.log('API Response:', data)

            const popupOverlay = document.getElementById('popupOverlay')
            popupOverlay.style.display = 'none'

            // Check if the response is valid or if we get an error for the cellar location
            // not being available
            hideNewOwnerInputFields()

            document.getElementById('form-add-wine').reset()

            // Update the table after adding a new wine
            await populateWinesTable('drink-date-column-sort', true, null, 0, 25)
        } catch (error) {
            console.error('Error in adding wine to database:', error)
        }
    })
})


document.addEventListener('DOMContentLoaded', function () {
    const purchasePriceInput = document.getElementById('purchase-price-input');

    // Add an input event listener to format the input dynamically
    purchasePriceInput.addEventListener('input', function () {
        // Remove non-numeric characters from the input value
        let inputValue = purchasePriceInput.value.replace(/[^0-9]/g, '');

        // Add leading zeros if needed
        inputValue = inputValue.padStart(3, '0');
        let length = inputValue.length
        if (length === 4 && inputValue[0] === '0') {
            inputValue = inputValue.substring(1)
        }

        if (inputValue === '000') {
            purchasePriceInput.value = '';
        } else {
            // Format the value as a currency (assuming USD)
            const formattedValue = '$' + inputValue.slice(0, -2) + '.' + inputValue.slice(-2);

            // Update the input value
            purchasePriceInput.value = formattedValue;
        }
        
    });

    // Add a keypress event listener to prevent non-numeric input
    purchasePriceInput.addEventListener('keypress', function (event) {
        const key = event.key;
        // Allow numeric keys, backspace, and decimal point
        if (!/^\d$/.test(key) && key !== 'Backspace' && key !== '.') {
            event.preventDefault();
        }
    });

});




// Attach the onPageLoad function to the window.onload event
window.onload = onPageLoad