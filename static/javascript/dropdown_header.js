// static/js/dropdown.js

document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('menu-button');
    const dropdownMenu = document.getElementById('dropdown-menu');

    // Toggle dropdown visibility
    menuButton.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownMenu.classList.toggle('hidden');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
        if (!dropdownMenu.classList.contains('hidden')) {
            dropdownMenu.classList.add('hidden');
        }
    });

    // Close dropdown when clicking on any dropdown item
    dropdownMenu.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownMenu.classList.add('hidden');
    });
});