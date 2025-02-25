document.addEventListener("DOMContentLoaded", () => {
  const ideaForm = document.getElementById("ideaForm");
  const resultContainer = document.getElementById("result");
  const ideaText = document.getElementById("ideaText");
  const categoriesContainer = document.getElementById("categoriesContainer");
  const logoutBtn = document.getElementById("logout-btn");
  const addCategoryBtn = document.getElementById("addCategoryBtn");
  const newCategoryNameInput = document.getElementById("newCategoryName");
  const newCategoryMessage = document.getElementById("newCategoryMessage");

  const API_URL = "https://final-back-end-fym2.onrender.com"; 
  let accessToken = localStorage.getItem("token");

  if (!accessToken) {
    alert("Please log in.");
    window.location.href = "login.html";
    return;
  }

  loadCategories();

  async function loadCategories() {
    try {
      const response = await fetch(API_URL + "/categories");
      const categories = await response.json();
      categoriesContainer.innerHTML = categories.map(cat =>
        `<label><input type="checkbox" name="category" value="${cat.name}"> ${cat.name}</label>`
      ).join(" ");
    } catch (error) {
      console.error("Error loading categories:", error);
    }
  }

  ideaForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!accessToken) {
      alert("Please log in to generate ideas.");
      return;
    }

    const preferences = document.getElementById("preferences").value;
    const selectedCategories = Array.from(document.querySelectorAll('input[name="category"]:checked'))
      .map(checkbox => checkbox.value);

    const requestData = {
      preferences,
      categories: selectedCategories
    };

    console.log("Sending request:", requestData);

    try {
      const response = await fetch(API_URL + "/generate-idea", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + accessToken
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Error generating idea");
      }

      const data = await response.json();
      ideaText.textContent = data.idea;
      resultContainer.classList.remove("hidden");

    } catch (error) {
      console.error("Error generating idea:", error);
      alert("Failed to generate idea. Please try again.");
    }
  });

  addCategoryBtn.addEventListener("click", async () => {
    const newCategoryName = newCategoryNameInput.value.trim();
    if (!newCategoryName) {
      newCategoryMessage.classList.remove("hidden");
      newCategoryMessage.textContent = "Please enter a category name.";
      return;
    }

    try {
      const response = await fetch(API_URL + "/categories", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newCategoryName })
      });
      const result = await response.json();
      if (response.ok) {
        newCategoryMessage.classList.remove("hidden");
        newCategoryMessage.textContent = "Category added successfully!";
        newCategoryNameInput.value = "";
        loadCategories();
      } else {
        newCategoryMessage.classList.remove("hidden");
        newCategoryMessage.textContent = result.error || "An error occurred.";
      }
    } catch (error) {
      console.error("Error adding category:", error);
      newCategoryMessage.classList.remove("hidden");
      newCategoryMessage.textContent = "An error occurred. Please try again.";
    }
  });

  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username"); 
    window.location.href = "login.html"; 
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const usernameDisplay = document.getElementById("username-display");
  const storedUsername = localStorage.getItem("username"); 

  if (storedUsername) {
    usernameDisplay.textContent = storedUsername;
  } else {
    usernameDisplay.textContent = "Guest";
  }
});
