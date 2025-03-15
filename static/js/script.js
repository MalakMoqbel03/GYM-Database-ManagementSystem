const tabs = document.querySelectorAll('.tab-link');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove the active class from all tabs and contents
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        // Add the active class to the clicked tab and corresponding content
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});
// Checkbox validation logic
document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('#specialty-checkboxes input[type="checkbox"]');
    const warning = document.getElementById('specialty-warning');
    const form = document.querySelector('#trainer-form');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;

            if (checkedCount > 3) {
                warning.style.display = 'block';
                checkbox.checked = false; // Uncheck the last checkbox
            } else {
                warning.style.display = 'none';
            }
        });
    });

    form.addEventListener('submit', (e) => {
        const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
        if (checkedCount > 3) {
            e.preventDefault(); // Prevent form submission
            warning.style.display = 'block';
            alert('You can select a maximum of three specialties.');
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const phoneInput = document.getElementById('phone');
    const ssnInput = document.getElementById('snn');
    const phoneError = document.getElementById('phone-error');
    const ssnError = document.getElementById('snn-error');
    const form = document.querySelector('#trainer-form');

    const checkUnique = async (field, value) => {
        const response = await fetch('/check_unique', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ field, value })
        });

        if (response.ok) {
            const data = await response.json();
            return data.exists;
        } else {
            console.error('Error checking uniqueness');
            return false;
        }
    };

    phoneInput.addEventListener('blur', async () => {
        const isDuplicate = await checkUnique('PhoneNumber_Trainer', phoneInput.value);
        if (isDuplicate) {
            phoneError.style.display = 'block';
        } else {
            phoneError.style.display = 'none';
        }
    });

    ssnInput.addEventListener('blur', async () => {
        const isDuplicate = await checkUnique('SNNTrainer', ssnInput.value);
        if (isDuplicate) {
            ssnError.style.display = 'block';
        } else {
            ssnError.style.display = 'none';
        }
    });

    form.addEventListener('submit', async (e) => {
        const isPhoneDuplicate = await checkUnique('PhoneNumber_Trainer', phoneInput.value);
        const isSSNDuplicate = await checkUnique('SNNTrainer', ssnInput.value);

        if (isPhoneDuplicate) {
            e.preventDefault();
            phoneError.style.display = 'block';
        }

        if (isSSNDuplicate) {
            e.preventDefault();
            ssnError.style.display = 'block';
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const tableBody = document.getElementById('trainersTableBody');
    const rows = Array.from(tableBody.getElementsByTagName('tr'));

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();

        rows.forEach(row => {
            const firstName = row.cells[0].textContent.toLowerCase();
            const specialty = row.cells[2].textContent.toLowerCase();

            if (firstName.includes(query) || specialty.includes(query)) {
                row.style.display = ''; // Show row
            } else {
                row.style.display = 'none'; // Hide row
            }
        });
    });
});

function searchTrainers() {
    const input = document.getElementById("search-bar").value.toLowerCase();
    const table = document.getElementById("trainers-table");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) { // Skip the header row
        const firstName = rows[i].getElementsByTagName("td")[0].textContent.toLowerCase();
        const specialty = rows[i].getElementsByTagName("td")[2].textContent.toLowerCase();

        if (firstName.includes(input) || specialty.includes(input)) {
            rows[i].style.display = ""; // Show the row
        } else {
            rows[i].style.display = "none"; // Hide the row
        }
    }
}


function reserveClass(classId, traineeId) {
    fetch(`/reserve_class/${classId}/${traineeId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.status === 'success') {
            window.location.href = `/trainee_schedule/${traineeId}`;
        }
    })
    .catch(error => console.error('Error:', error));
}
