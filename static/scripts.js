$(document).ready(function() {
    $('#dataTable').DataTable();
});

function updateRow(button) {
    var row = $(button).closest('tr');
    var email = row.find('td:eq(0)').text();
    var password = btoa(row.find('td:eq(1)').text());
    var admin = row.find('td:eq(2)').text();
    var verified = row.find('td:eq(3)').text();

    fetch('http://localhost:8000/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
            admin: admin,
            verified: verified
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });
}

function addUser() {
    var newRow = '<tr>' +
        '<td contenteditable="true"></td>' +
        '<td contenteditable="true"></td>' +
        '<td contenteditable="true"></td>' +
        '<td contenteditable="true"></td>' +
        '<td>' +
            '<button class="action-btn" onclick="updateRow(this)">Update</button>' +
            '<button class="action-btn" onclick="deleteRow(this)">Delete</button>' +
            '<button class="action-btn" onclick="addRow(this)">Add</button>' +
        '</td>' +
    '</tr>';

    $('#dataTable tbody').append(newRow);
}

async function Logout() {
    try {
        let access = false;
        const response = await fetch('http://localhost:8000/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                access: access
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        cache = [];
        localStorage.clear();
        location.reload();
        window.location.href = 'http://localhost:8000';

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error during fetch operation:', error);
    }
}

function addRow(button) {
    var row = $(button).closest('tr');
    var email = row.find('td:eq(0)').text();
    var password = row.find('td:eq(1)').text();
    var admin = row.find('td:eq(2)').text();
    var verified = row.find('td:eq(3)').text();

    fetch('http://localhost:8000/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
            admin: admin,
            verified: verified
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });
}

function deleteRow(button) {
    var row = $(button).closest('tr');
    var email = row.find('td:eq(0)').text();

    fetch('http://localhost:8000/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
        row.remove();
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });
}