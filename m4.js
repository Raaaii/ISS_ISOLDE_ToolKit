function calculateM4() {
    fetch("http://localhost:5500/calculate_m4", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(selectedParticles), // selectedParticles is a list of particles
    })
      .then((response) => response.json())
      .then((res) => {
        console.log("Received m4:", res);  // Debug log
        if (res.hasOwnProperty('Particle 4')) {
          masses['Particle 4'] = res['Particle 4']; // Assign the calculated m4 value to masses object
          calculateV3(); // Call calculateV3 after calculating m4
        } else {
          console.error("Error calculating m4:", res.error);  // Handle error
        }
      })
      .catch((error) => {
        console.error("Error:", error); // Handle fetch error
      });
  }
  