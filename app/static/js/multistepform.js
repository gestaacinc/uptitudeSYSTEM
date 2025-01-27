document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("multiStepForm");
    const steps = document.querySelectorAll(".step");
    const progressBar = document.getElementById("progressBar");
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    let currentStep = 0;

    // Update step visibility
    function updateSteps() {
        steps.forEach((step, index) => {
            step.classList.toggle("d-none", index !== currentStep);
        });
        progressBar.style.width = `${((currentStep + 1) / steps.length) * 100}%`;
        progressBar.textContent = `Step ${currentStep + 1}`;
        prevBtn.classList.toggle("d-none", currentStep === 0);
        nextBtn.textContent = currentStep === steps.length - 1 ? "Submit" : "Continue";
    }

    // Validate current step inputs
    function validateStep() {
        const inputs = steps[currentStep].querySelectorAll("input, select");
        for (let input of inputs) {
            if (!input.checkValidity()) {
                input.reportValidity();
                return false;
            }
        }
        return true;
    }

    // Handle Next button click
    nextBtn.addEventListener("click", function () {
        if (currentStep === steps.length - 1) {
            // Submit the form on the last step
            form.submit();
        } else {
            if (validateStep()) {
                // Save values for review
                if (currentStep === 0) {
                    document.getElementById("reviewStudentName").textContent =
                        `${document.getElementById("firstName").value} ${document.getElementById("lastName").value}`;
                    document.getElementById("reviewContactNumber").textContent =
                        document.getElementById("contactNumber").value;
                } else if (currentStep === 1) {
                    const courseSelect = document.getElementById("course");
                    const selectedCourse = courseSelect.options[courseSelect.selectedIndex].text;
                    document.getElementById("reviewCourse").textContent = selectedCourse;
                }
                currentStep++;
                updateSteps();
            }
        }
    });

    // Handle Previous button click
    prevBtn.addEventListener("click", function () {
        currentStep--;
        updateSteps();
    });

    // Initialize the form
    updateSteps();
});
