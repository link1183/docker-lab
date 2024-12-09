let userToDelete = null;

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

function loadPage(page) {
  fetch(`/users?page=${page}`, {
    headers: {
      Accept: "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        showNotification(data.error, "error");
        return;
      }
      updateUsersTable(data.users);
      updatePagination(data.current_page, data.total_pages);
    })
    .catch((error) => {
      showNotification("Error loading users", "error");
      console.error("Error:", error);
    });
}

function updateUsersTable(users, currentPage, totalPages) {
  const container = document.getElementById("users-container");
  let html = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${users
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
                  .join("")}
            </tbody>
        </table>
    `;

  if (totalPages > 1) {
    html += `<div class="pagination">
            ${
              currentPage > 1
                ? `<a href="#" onclick="loadPage(${currentPage - 1}); return false;" class="btn">&laquo; Previous</a>`
                : ""
            }
            
            ${Array.from({ length: totalPages }, (_, i) => i + 1)
              .map((p) =>
                p === currentPage
                  ? `<span class="current-page">${p}</span>`
                  : `<a href="#" onclick="loadPage(${p}); return false;" class="btn">${p}</a>`,
              )
              .join("")}
            
            ${
              currentPage < totalPages
                ? `<a href="#" onclick="loadPage(${currentPage + 1}); return false;" class="btn">Next &raquo;</a>`
                : ""
            }
        </div>`;
  }

  container.innerHTML = html;
}

function updatePagination(currentPage, totalPages) {
  if (totalPages <= 1) return;

  const pagination = document.createElement("div");
  pagination.className = "pagination";
  let html = "";

  if (currentPage > 1) {
    html += `<a href="#" onclick="loadPage(${currentPage - 1}); return false;" class="btn">&laquo; Previous</a>`;
  }

  for (let p = 1; p <= totalPages; p++) {
    if (p === currentPage) {
      html += `<span class="current-page">${p}</span>`;
    } else {
      html += `<a href="#" onclick="loadPage(${p}); return false;" class="btn">${p}</a>`;
    }
  }

  if (currentPage < totalPages) {
    html += `<a href="#" onclick="loadPage(${currentPage + 1}); return false;" class="btn">Next &raquo;</a>`;
  }

  pagination.innerHTML = html;
  const container = document.getElementById("users-container");
  const existingPagination = container.querySelector(".pagination");
  if (existingPagination) {
    container.replaceChild(pagination, existingPagination);
  } else {
    container.appendChild(pagination);
  }
}

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

function showDeleteConfirmation(userId, userName) {
  userToDelete = userId;
  document.getElementById("deleteUserName").textContent = userName;
  showModal("deleteModal");
}

function handleDeleteConfirmation() {
  if (!userToDelete) return;

  hideModal("deleteModal");

  fetch(`/users/${userToDelete}/delete`, {
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
    })
    .finally(() => {
      userToDelete = null;
    });
}

function populateEditForm(userId, name, email) {
  document.getElementById("edit-id").value = userId;
  document.getElementById("edit-name").value = name;
  document.getElementById("edit-email").value = email;
  showModal("editModal");
}

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

  const nav = container.querySelector(".nav");
  nav.insertAdjacentElement("afterend", messageDiv);

  setTimeout(() => {
    messageDiv.style.opacity = "0";
    setTimeout(() => messageDiv.remove(), 300);
  }, 3000);
}

document.addEventListener("DOMContentLoaded", function () {
  const modals = document.querySelectorAll(".modal");
  modals.forEach((modal) => {
    modal.addEventListener("click", function (event) {
      if (event.target === modal) {
        hideModal(modal.id);
      }
    });
  });

  const closeButtons = document.querySelectorAll(".close");
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const modal = button.closest(".modal");
      if (modal) {
        hideModal(modal.id);
      }
    });
  });

  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", handleFormSubmit);
  });

  const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener("click", handleDeleteConfirmation);
  }
});
