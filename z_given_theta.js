function calculateThetaFromZ(){

    fetch("http://localhost:5500/given_z_find_theta", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
        z_1: document.querySelector("#z_1").value,
        z_2: document.querySelector("#z_2").value,
        t_cylcotron: document.querySelector("#t_cylcotron").value
        }),

    })
}