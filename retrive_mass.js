
function retrieveDataAndCalculateMassExcess(particleValues) {
    // Create the overlay and popup elements first
    const overlay = document.getElementById("overlay");
    const popup = document.getElementById("popup");
    popup.innerHTML = ""; // Clear any previous content
  
    fetch("http://localhost:5500/calculate_mass_excess", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(particleValues),
    })
      .then(response => response.json())
      .then(massExcessValues => {
        const closeButton = document.createElement("span");
        masses = massExcessValues;
        closeButton.classList.add("close-button");
        closeButton.textContent = "x";
        closeButton.addEventListener("click", () => {
          overlay.style.display = "none";
          popup.style.display = "none";
        });
  
        const content = document.createElement("div");
        content.classList.add("popup-content");
  
        Object.keys(massExcessValues).forEach(particle => {
          const particleResult = document.createElement("div");
          particleResult.classList.add("particle-result");
  
          const particleName = document.createElement("h3");
          particleName.textContent = particle;
  
          const massExcessValue = document.createElement("p");
          massExcessValue.textContent = `Nuclear Mass: ${massExcessValues[particle]}`;
  
          particleResult.appendChild(particleName);
          particleResult.appendChild(massExcessValue);
          content.appendChild(particleResult);
        });
  
        massesDiv.style.display = 'block';
        mass1 = document.querySelector('#particle1').value = masses['Particle 1']
        mass2 = document.querySelector('#particle2').value = masses['Particle 2']
        mass3 = document.querySelector('#particle3').value = masses['Particle 3']
  
        popup.appendChild(closeButton);
        popup.appendChild(content);
  
        overlay.style.display = "block";
        popup.style.display = "block";
      })
      .catch(error => {
        console.error("Error:", error);
      });
  }