document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#thetaForm");
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(form);
  
      fetch("/calculate", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((data) => {
          const resultContainer = document.querySelector(".result");
          resultContainer.innerHTML = `Optimal Theta Lab: ${data.optimal_theta_lab}`;
          resultContainer.style.display = "block";
        })
        .catch((error) => {
          const resultContainer = document.querySelector(".result");
          resultContainer.innerHTML = `Error: ${error.message}`;
          resultContainer.style.display = "block";
        });
    });
  });
  