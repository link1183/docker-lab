// Track user to be deleted
let userToDelete = null;

/**
 * Show a modal dialog
 * @param {string} modalId - The ID of the modal to show
 */
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("show");
    // Add escape key listener when modal is shown
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
                    onclick="showDeleteConfirmation('${user[0]}', '${user[1]}')">
                    Delete
                </button>
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

  // Remove existing notifications
  const existingMessage = container.querySelector(
    ".success-message, .error-message",
  );
  if (existingMessage) {
    existingMessage.remove();
  }

  // Create and insert new notification
  const messageDiv = document.createElement("div");
  messageDiv.className =
    type === "success" ? "success-message" : "error-message";
  messageDiv.textContent = message;

  // Insert after the navigation
  const nav = container.querySelector(".nav");
  nav.insertAdjacentElement("afterend", messageDiv);

  // Auto-remove after 3 seconds
  setTimeout(() => {
    messageDiv.style.opacity = "0";
    setTimeout(() => messageDiv.remove(), 300);
  }, 3000);
}

/**
 * Handle form submission with AJAX
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
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
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
 * Show delete confirmation modal
 * @param {string} userId - The ID of the user to delete
 * @param {string} userName - The name of the user to delete
 */
function showDeleteConfirmation(userId, userName) {
  userToDelete = userId;
  const nameElement = document.getElementById("deleteUserName");
  nameElement.textContent = userName;
  showModal("deleteModal");
}

/**
 * Handle the actual deletion after confirmation
 */
function handleDeleteConfirmation() {
  if (!userToDelete) return;

  hideModal("deleteModal");

  fetch(`/users/${userToDelete}/delete`, {
    method: "POST",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
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
    })
    .finally(() => {
      userToDelete = null;
    });
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

// Initialize all event listeners when the DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Handle modal background clicks
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

  // Handle delete confirmation
  const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener("click", handleDeleteConfirmation);
  }
});
