// public/static/js/main.js

/**
 * Show a modal dialog
 * @param {string} modalId - The ID of the modal to show
 */
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("show");
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        hideModal(modalId);
      }
    });
  }
}

/**
 * Hide a modal dialog
 * @param {string} modalId - The ID of the modal to hide
 */
function hideModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("show");
    const form = modal.querySelector("form");
    if (form) {
      form.reset();
    }
  }
}

/**
 * Refresh the users table with new data
 * @param {Array} users - Array of user objects
 */
function updateUsersTable(users) {
  const tbody = document.querySelector("table tbody");
  tbody.innerHTML = users
    .map(
      (user) => `
        <tr>
            <td>${user[0]}</td>
            <td>${user[1]}</td>
            <td>${user[2]}</td>
            <td>
                <button class="btn btn-warning" 
                    onclick="populateEditForm('${user[0]}', '${user[1]}', '${user[2]}')">
                    Edit
                </button>
                <button class="btn btn-danger" 
                    onclick="confirmDelete('${user[0]}')">
                    Delete
                </button>
                <form id="delete-form-${user[0]}" action="/users/${user[0]}/delete" method="POST" style="display: none;"></form>
            </td>
        </tr>
    `,
    )
    .join("");
}

/**
 * Show a notification message
 * @param {string} message - Message to display
 * @param {string} type - 'success' or 'error'
 */
function showNotification(message, type = "success") {
  const container = document.querySelector(".container");
  const existingMessage = container.querySelector(
    ".success-message, .error-message",
  );
  if (existingMessage) {
    existingMessage.remove();
  }

  const messageDiv = document.createElement("div");
  messageDiv.className =
    type === "success" ? "success-message" : "error-message";
  messageDiv.textContent = message;

  container.insertBefore(messageDiv, container.querySelector(".actions"));

  // Remove message after 3 seconds
  setTimeout(() => messageDiv.remove(), 3000);
}

/**
 * Handle form submission
 * @param {Event} event - Form submission event
 */
function handleFormSubmit(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const modalId = form.closest(".modal").id;

  fetch(form.action, {
    method: form.method,
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        showNotification(data.error, "error");
      } else {
        updateUsersTable(data.users);
        hideModal(modalId);
        showNotification(data.message);
      }
    })
    .catch((error) => {
      showNotification(
        "An error occurred while processing your request",
        "error",
      );
      console.error("Error:", error);
    });
}

/**
 * Confirm and handle user deletion
 * @param {string} userId - The ID of the user to delete
 */
function confirmDelete(userId) {
  if (confirm("Are you sure you want to delete this user?")) {
    fetch(`/users/${userId}/delete`, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          showNotification(data.error, "error");
        } else {
          updateUsersTable(data.users);
          showNotification(data.message);
        }
      })
      .catch((error) => {
        showNotification("An error occurred while deleting the user", "error");
        console.error("Error:", error);
      });
  }
}

/**
 * Populate the edit form with user data
 * @param {string} userId - The user's ID
 * @param {string} name - The user's name
 * @param {string} email - The user's email
 */
function populateEditForm(userId, name, email) {
  document.getElementById("edit-id").value = userId;
  document.getElementById("edit-name").value = name;
  document.getElementById("edit-email").value = email;
  showModal("editModal");
}

// Add event listeners when the DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Handle modal clicks
  const modals = document.querySelectorAll(".modal");
  modals.forEach((modal) => {
    modal.addEventListener("click", function (event) {
      if (event.target === modal) {
        hideModal(modal.id);
      }
    });
  });

  // Handle close buttons
  const closeButtons = document.querySelectorAll(".close");
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const modal = button.closest(".modal");
      if (modal) {
        hideModal(modal.id);
      }
    });
  });

  // Handle form submissions
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", handleFormSubmit);
  });
});
