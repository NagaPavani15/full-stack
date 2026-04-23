document.getElementById('registrationForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Stop form submission

    // Clear previous errors
    document.querySelectorAll('.error-msg').forEach(el => el.innerText = "");
    document.getElementById('successMessage').style.display = "none";

    let isValid = true;

    // 1. Name Validation
    const name = document.getElementById('name').value.trim();
    if (name === "") {
        document.getElementById('nameError').innerText = "Name is required";
        isValid = false;
    }

    // 2. Email Validation (Proper format)
    const email = document.getElementById('email').value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById('emailError').innerText = "Enter a valid email address";
        isValid = false;
    }

    // 3. Phone Validation (10 digits)
    const phone = document.getElementById('phone').value.trim();
    if (phone.length !== 10 || isNaN(phone)) {
        document.getElementById('phoneError').innerText = "Enter a valid 10-digit phone number";
        isValid = false;
    }

    // 4. Gender Validation
    const gender = document.querySelector('input[name="gender"]:checked');
    if (!gender) {
        document.getElementById('genderError').innerText = "Please select your gender";
        isValid = false;
    }

    // 5. Course Selection
    const course = document.getElementById('course').value;
    if (course === "") {
        document.getElementById('courseError').innerText = "Please select a course";
        isValid = false;
    }

    // 6. Password Strength (Required & Length)
    const password = document.getElementById('password').value;
    if (password.length < 8) {
        document.getElementById('passwordError').innerText = "Password must be at least 8 characters";
        isValid = false;
    }

    // Bonus: Success Message
    if (isValid) {
        document.getElementById('successMessage').style.display = "block";
        this.reset(); // Clear form after success
    }
});