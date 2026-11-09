// Backend API URL
const API_URL = "http://98.81.138.241:5000/employees";

const employeeForm = document.getElementById("employeeForm");

const employeeTable = document.getElementById("employeeTable");

const message = document.getElementById("message");


// Display messages
function showMessage(text, isError = false) {

    message.textContent = text;

    message.style.color = isError ? "red" : "green";

}


// GET: Load all employees
async function loadEmployees() {

    try {

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Unable to retrieve employees");
        }

        const employees = await response.json();

        employeeTable.innerHTML = "";

        employees.forEach(employee => {

            const row = document.createElement("tr");

            const values = [
                employee.id,
                employee.name,
                employee.email,
                employee.department,
                employee.salary
            ];

            values.forEach(value => {

                const cell = document.createElement("td");

                cell.textContent = value;

                row.appendChild(cell);

            });


            const actions = document.createElement("td");


            // Edit button
            const editButton = document.createElement("button");

            editButton.textContent = "Edit";

            editButton.className = "edit";

            editButton.onclick = () => editEmployee(employee);


            // Delete button
            const deleteButton = document.createElement("button");

            deleteButton.textContent = "Delete";

            deleteButton.className = "delete";

            deleteButton.onclick = () => deleteEmployee(employee.id);


            actions.appendChild(editButton);

            actions.appendChild(deleteButton);

            row.appendChild(actions);

            employeeTable.appendChild(row);

        });

    } catch (error) {

        showMessage(error.message, true);

    }

}


// POST: Add employee
// PUT: Update employee
employeeForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const employeeId = document.getElementById("employeeId").value;

    const employee = {

        name: document.getElementById("name").value.trim(),

        email: document.getElementById("email").value.trim(),

        department: document.getElementById("department").value.trim(),

        salary: document.getElementById("salary").value

    };


    const isEditing = employeeId !== "";


    const url = isEditing
        ? `${API_URL}/${employeeId}`
        : API_URL;


    const method = isEditing ? "PUT" : "POST";


    try {

        const response = await fetch(url, {

            method: method,

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(employee)

        });


        const result = await response.json();


        if (!response.ok) {

            throw new Error(result.error || "Operation failed");

        }


        showMessage(result.message);

        employeeForm.reset();

        resetForm();

        await loadEmployees();


    } catch (error) {

        showMessage(error.message, true);

    }

});


// Fill form for editing
function editEmployee(employee) {

    document.getElementById("employeeId").value = employee.id;

    document.getElementById("name").value = employee.name;

    document.getElementById("email").value = employee.email;

    document.getElementById("department").value = employee.department;

    document.getElementById("salary").value = employee.salary;


    document.getElementById("form-title").textContent = "Update Employee";

    document.getElementById("submitBtn").textContent = "Update Employee";

    document.getElementById("cancelBtn").hidden = false;


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


// DELETE: Delete employee
async function deleteEmployee(id) {

    if (!confirm("Are you sure you want to delete this employee?")) {

        return;

    }


    try {

        const response = await fetch(`${API_URL}/${id}`, {

            method: "DELETE"

        });


        const result = await response.json();


        if (!response.ok) {

            throw new Error(result.error || "Delete failed");

        }


        showMessage(result.message);

        await loadEmployees();


    } catch (error) {

        showMessage(error.message, true);

    }

}


// Reset form
function resetForm() {

    document.getElementById("employeeId").value = "";

    document.getElementById("form-title").textContent = "Add Employee";

    document.getElementById("submitBtn").textContent = "Add Employee";

    document.getElementById("cancelBtn").hidden = true;

}


// Cancel edit
document.getElementById("cancelBtn").addEventListener("click", function() {

    employeeForm.reset();

    resetForm();

    showMessage("");

});


// Load employees when page opens
loadEmployees();
