document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Function to format NRIC input with hyphens
    const nricInput = document.getElementById('nric');
    if (nricInput) {
        nricInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            let formattedValue = '';
            
            if (value.length > 0) {
                if (value.length <= 6) {
                    formattedValue = value;
                } else if (value.length <= 8) {
                    formattedValue = value.substring(0, 6) + '-' + value.substring(6);
                } else {
                    formattedValue = value.substring(0, 6) + '-' + value.substring(6, 8) + '-' + value.substring(8, 12);
                }
            }
            
            e.target.value = formattedValue;
        });
    }

    // Handle search form submission
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            // Remove empty parameters
            const inputs = searchForm.querySelectorAll('input, select');
            inputs.forEach(input => {
                if (input.value === '' && input.name !== 'search') {
                    input.name = '';
                }
            });
        });
    }

    // Table sorting functionality
    document.querySelectorAll('th[data-sort]').forEach(headerCell => {
        headerCell.addEventListener('click', () => {
            const table = headerCell.closest('table');
            const columnIndex = headerCell.cellIndex;
            const sortDirection = headerCell.classList.contains('sort-asc') ? 'desc' : 'asc';
            
            // Remove sort classes from all headers
            table.querySelectorAll('th').forEach(th => {
                th.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Add sort class to current header
            headerCell.classList.add(`sort-${sortDirection}`);
            
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            // Sort rows
            rows.sort((rowA, rowB) => {
                const cellA = rowA.cells[columnIndex].textContent.trim();
                const cellB = rowB.cells[columnIndex].textContent.trim();
                
                // Handle date sorting if cells contain dates
                if (cellA.match(/^\d{2} [A-Za-z]{3} \d{4}$/) && cellB.match(/^\d{2} [A-Za-z]{3} \d{4}$/)) {
                    const dateA = new Date(cellA);
                    const dateB = new Date(cellB);
                    return sortDirection === 'asc' ? dateA - dateB : dateB - dateA;
                }
                
                return sortDirection === 'asc' 
                    ? cellA.localeCompare(cellB) 
                    : cellB.localeCompare(cellA);
            });
            
            // Reorder rows in the DOM
            rows.forEach(row => {
                tbody.appendChild(row);
            });
        });
    });

    // Add status color indicators
    document.querySelectorAll('.status-indicator').forEach(indicator => {
        const status = indicator.textContent.trim();
        switch(status) {
            case 'Approved':
                indicator.classList.add('text-success');
                break;
            case 'Rejected':
                indicator.classList.add('text-danger');
                break;
            case 'Processing':
                indicator.classList.add('text-warning');
                break;
        }
    });
});

// Function to filter applications table
function filterTable() {
    const searchInput = document.getElementById('search-input');
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    const statusFilter = document.getElementById('status-filter');
    const selectedStatus = statusFilter ? statusFilter.value : '';
    const typeFilter = document.getElementById('type-filter');
    const selectedType = typeFilter ? typeFilter.value : '';
    
    const table = document.getElementById('applications-table');
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const name = row.querySelector('[data-field="name"]').textContent.toLowerCase();
        const nric = row.querySelector('[data-field="nric"]').textContent.toLowerCase();
        const phone = row.querySelector('[data-field="phone"]').textContent.toLowerCase();
        const status = row.querySelector('[data-field="status"]').textContent.trim();
        const type = row.querySelector('[data-field="type"]').textContent.trim();
        
        const matchesSearch = searchTerm === '' || 
            name.includes(searchTerm) || 
            nric.includes(searchTerm) || 
            phone.includes(searchTerm);
        
        const matchesStatus = selectedStatus === '' || status === selectedStatus;
        const matchesType = selectedType === '' || type === selectedType;
        
        if (matchesSearch && matchesStatus && matchesType) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
