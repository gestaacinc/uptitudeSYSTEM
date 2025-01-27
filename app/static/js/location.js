document.addEventListener("DOMContentLoaded", function () {
    const countrySelect = document.getElementById("country");
    const regionContainer = document.getElementById("region-container");
    const regionSelect = document.getElementById("region");
    const municipalityContainer = document.getElementById("municipality-container");
    const municipalitySelect = document.getElementById("municipality");
    const barangayContainer = document.getElementById("barangay-container");
    const barangaySelect = document.getElementById("barangay");

    // Fetch countries dynamically
    fetch("https://restcountries.com/v3.1/all")
        .then((response) => response.json())
        .then((countries) => {
            countries.forEach((country) => {
                const option = document.createElement("option");
                option.value = country.name.common;
                option.textContent = country.name.common;
                countrySelect.appendChild(option);
            });
        })
        .catch((error) => console.error("Error fetching countries:", error));

    // Handle country selection
    countrySelect.addEventListener("change", function () {
        const country = this.value;
        if (country === "Philippines") {
            // Fetch regions for the Philippines
            fetch("https://psgc.gitlab.io/api/regions/")
                .then((response) => response.json())
                .then((regions) => {
                    regionContainer.style.display = "block";
                    regionSelect.innerHTML = '<option value="">Select Region</option>';
                    regions.forEach((region) => {
                        const option = document.createElement("option");
                        option.value = region.code; // Use region code
                        option.textContent = region.name; // Display region name
                        regionSelect.appendChild(option);
                    });
                })
                .catch((error) => console.error("Error fetching regions:", error));
        } else {
            regionContainer.style.display = "none";
            municipalityContainer.style.display = "none";
            barangayContainer.style.display = "none";
        }
    });

    // Handle region selection
    regionSelect.addEventListener("change", function () {
        const regionCode = this.value;

        if (regionCode) {
            municipalityContainer.style.display = "block";
            municipalitySelect.innerHTML = '<option value="">Select Municipality/City</option>';

            // Fetch municipalities
            fetch(`https://psgc.gitlab.io/api/regions/${regionCode}/municipalities`)
                .then((response) => response.json())
                .then((municipalities) => {
                    municipalities.forEach((municipality) => {
                        const option = document.createElement("option");
                        option.value = municipality.name; // Set name as value
                        option.dataset.code = municipality.code; // Save code for further API use
                        option.textContent = municipality.name; // Display municipality name
                        municipalitySelect.appendChild(option);
                    });
                })
                .catch((error) => console.error("Error fetching municipalities:", error));

            // Fetch cities
            fetch(`https://psgc.gitlab.io/api/regions/${regionCode}/cities`)
                .then((response) => response.json())
                .then((cities) => {
                    cities.forEach((city) => {
                        const option = document.createElement("option");
                        option.value = city.name; // Set name as value
                        option.dataset.code = city.code; // Save code for further API use
                        option.textContent = city.name; // Display city name
                        municipalitySelect.appendChild(option);
                    });
                })
                .catch((error) => console.error("Error fetching cities:", error));
        } else {
            municipalityContainer.style.display = "none";
            barangayContainer.style.display = "none";
        }
    });




    // Handle municipality selection
    municipalitySelect.addEventListener("change", function () {
        const selectedCode = municipalitySelect.options[municipalitySelect.selectedIndex]?.dataset?.code;

        if (selectedCode) {
            fetch(`https://psgc.gitlab.io/api/municipalities/${selectedCode}/barangays`)
                .then((response) => {
                    if (!response.ok) {
                        if (response.status === 404) {
                            throw new Error("Barangay information not available for this municipality.");
                        }
                        throw new Error("Failed to fetch barangays");
                    }
                    return response.json();
                })
                .then((barangays) => {
                    barangayContainer.style.display = "block";
                    barangaySelect.innerHTML = '<option value="">Select Barangay</option>';
                    barangays.forEach((barangay) => {
                        const option = document.createElement("option");
                        option.value = barangay.name;
                        option.textContent = barangay.name;
                        barangaySelect.appendChild(option);
                    });
                })
                .catch((error) => {
                    console.error("Error fetching barangays:", error);
                    barangayContainer.style.display = "none";
                    alert(error.message);
                    // Allow manual input as fallback
                    const manualInput = `
                    <label for="manual-barangay" class="form-label">Barangay (Manual Input)</label>
                    <input type="text" id="manual-barangay" class="form-control" name="manual_barangay" placeholder="Enter barangay">
                `;
                    barangayContainer.innerHTML = manualInput;
                    barangayContainer.style.display = "block";
                });
        } else {
            barangayContainer.style.display = "none";
        }
    });


});
