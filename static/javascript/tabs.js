
document.addEventListener("DOMContentLoaded", function() {
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');

    // Function to activate a tab
    function activateTab(tabName) {
        // Remove active state from all links and hide all contents
        tabLinks.forEach(link => link.classList.remove('border-blue-600'));
        tabContents.forEach(content => content.style.display = "none");

        // Activate the clicked tab and show the corresponding content
        const activeLink = document.querySelector(`[data-tab="${tabName}"]`);
        const activeContent = document.querySelector(`.tab-content[data-tab="${tabName}"]`);

        if (activeLink) {
            activeLink.classList.add('border-blue-600');
        }
        if (activeContent) {
            activeContent.style.display = "block";
        }
    }

    // Set HOTEL as the default tab on page load
    activateTab('ferry');

    // Add event listener to each tab link
    tabLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const tabName = this.getAttribute('data-tab');
            activateTab(tabName);
        });
    });
});


// date range
document.addEventListener('DOMContentLoaded', function () {
    const dateRangeInput = document.getElementById('dateRange');
    const durationInput = document.getElementById('duration');

    flatpickr(dateRangeInput, {
        mode: "range",
        minDate: 'today', // Set minimum date to today
        dateFormat: "d-m-Y", // Set date format to day-month-year
        onChange: function(selectedDates) {
            if (selectedDates.length === 2) {
                const [startDate, endDate] = selectedDates;
                const duration = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));

                // Format dates to d-m-Y
                const formattedStartDate = startDate.toLocaleDateString('en-GB');
                const formattedEndDate = endDate.toLocaleDateString('en-GB');
                
                // Update the dateRange input with selected dates and duration
                dateRangeInput.value = `${formattedStartDate} to ${formattedEndDate}`;
                
                // Update the duration input with the number of days
                durationInput.value = `${duration} days`;
            } else {
                dateRangeInput.value = '';
                durationInput.value = '0 days';
            }
        }
    });
});


   // Show or hide the dropdown
function toggleDropdown() {
    const dropdown = document.getElementById('roomDropdown');
    dropdown.classList.toggle('hidden');
}

// Update the counts for rooms, adults, and children
function updateCount(type, change) {
    const roomInput = document.getElementById('roomCount');
    const adultInput = document.getElementById('adultCount');
    const childInput = document.getElementById('childCount');
    
    let roomCount = parseInt(roomInput.value);
    let adultCount = parseInt(adultInput.value);
    let childCount = parseInt(childInput.value);

    if (type === 'room') {
        roomCount = Math.max(1, roomCount + change); // Minimum of 1 room
        roomInput.value = roomCount;
    } else if (type === 'adult') {
        adultCount = Math.max(1, adultCount + change); // Minimum of 1 adult
        adultInput.value = adultCount;
    } else if (type === 'child') {
        childCount = Math.max(0, childCount + change); // Minimum of 0 children
        childInput.value = childCount;
        updateChildAgeDropdowns(childCount);
    }
}

// Function to dynamically add or remove child age dropdowns
function updateChildAgeDropdowns(count) {
    const container = document.getElementById('childAgeContainer');
    container.innerHTML = ''; // Clear existing dropdowns

    // Create a flex container to hold all the child age dropdowns side by side
    const flexContainer = document.createElement('div');
    flexContainer.classList.add('flex', 'flex-wrap', 'gap-4');

    for (let i = 1; i <= count; i++) {
        // Create a new dropdown for each child
        const childDropdown = document.createElement('div');
        childDropdown.classList.add('mb-1', 'flex-grow'); // Flex-grow ensures dropdowns are responsive

        childDropdown.innerHTML = `
            <label for="childAge${i}" class="block text-gray-800 font-semibold mb-2">Child ${i} Age</label>
            <select id="childAge${i}" name="childAge${i}" class="w-full p-3 border-2 custom-border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none">
                <option value="" disabled selected>Age</option>
                ${Array.from({ length: 18 }, (_, j) => `<option value="${j}">${j}</option>`).join('')}
            </select>`;
        
        // Append the new dropdown to the flex container
        flexContainer.appendChild(childDropdown);
    }

    // Append the flex container to the main container
    container.appendChild(flexContainer);
}

// Function to handle the Done button click
function doneSelection() {
    const roomCount = document.getElementById('roomCount').value;
    const adultCount = document.getElementById('adultCount').value;
    const childCount = document.getElementById('childCount').value;

    // Update the input field with the selected values
    document.getElementById('roomDetails').value = `${roomCount} Room, ${adultCount} Adult${adultCount > 1 ? 's' : ''}, ${childCount} Children`;

    // Hide the dropdown
    document.getElementById('roomDropdown').classList.add('hidden');
}




document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('hotel');
    const suggestionList = document.getElementById('suggestions');

    input.addEventListener('input', function () {
        const query = this.value;
        if (query.length < 3) {
            suggestionList.classList.add('hidden');
            return; // Start search after 3 characters
        }

        fetch(`/autocomplete/?query=${query}`)
            .then(response => response.json())
            .then(data => {
                const suggestions = data.predictions || [];
                suggestionList.innerHTML = '';

                if (suggestions.length > 0) {
                    suggestions.forEach(suggestion => {
                        const li = document.createElement('li');
                        li.textContent = suggestion.description;
                        li.addEventListener('click', function () {
                            input.value = this.textContent;
                            suggestionList.classList.add('hidden');
                        });
                        suggestionList.appendChild(li);
                    });
                    suggestionList.classList.remove('hidden');
                } else {
                    suggestionList.classList.add('hidden');
                }
            })
            .catch(error => console.error('Error fetching autocomplete data:', error));
    });

    document.addEventListener('click', function(event) {
        if (!input.contains(event.target) && !suggestionList.contains(event.target)) {
            suggestionList.classList.add('hidden');
        }
    });
});