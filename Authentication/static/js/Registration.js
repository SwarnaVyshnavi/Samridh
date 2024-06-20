
// JavaScript code goes here...
// Function to get CSRF token from cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie name matches the expected format
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    var variable = false;

    // Function to generate and send OTP
    $("#sendOTP").click(function () {
        var email = $("#email").val();
        // Get CSRF token
        var csrftoken = getCookie('csrftoken');
        // AJAX request to send OTP to the provided email address
        $.ajax({
            url: sendOTPUrl,
            method: "POST",
            headers: { 'X-CSRFToken': csrftoken }, // Include CSRF token in headers
            data: { email: email },
            success: function (response) {
                alert("OTP sent successfully to your email.");
                // Enable the OTP input field
                $("#otp").prop('disabled', false);
            },
            error: function (xhr, status, error) {
                alert("Failed to send OTP. Please try again later.");
            }
        });
    });

    // Function to verify OTP
    $("#verifyOTP").click(function () {
        var otp = $("#otp").val();
        var email = $("#email").val();
        // Get CSRF token
        var csrftoken = getCookie('csrftoken');
        // AJAX request to verify the entered OTP
        $.ajax({
            url: verifyOTPUrl,
            method: "POST",
            headers: { 'X-CSRFToken': csrftoken }, // Include CSRF token in headers
            data: { otp: otp, email: email },
            success: function (response) {
                if (response.success) {
                    alert("OTP verified successfully.");
                    // Set the variable to true
                    variable = true;
                    // Disable OTP input field after successful verification
                    $("#otp").prop('disabled', true);
                    // Optionally, you can clear the OTP field as well
                    // $("#otp").val('');
                } else {
                    alert("Incorrect OTP. Please try again.");
                }
            },
            error: function (xhr, status, error) {
                alert("Failed to verify OTP. Please try again.");
            }
        });
    });


    // Function to check if passwords match
    $("#registrationForm").submit(function (event) {
        var password = $("#password").val();
        var confirmPassword = $("#confirmPassword").val();
        if (password !== confirmPassword) {
            event.preventDefault();
            $("#passwordMatchMessage").text("Passwords do not match!");
        }
    });


    $(".next-btn").click(function () {
        var currentStep = $(this).closest(".step-content");

        // Check if the current step is the second step (index 1, since indexing starts from 0)
        if (currentStep.index() === 2) {
            // Proceed only if the variable is true for the second step
            if (variable) {
                // Proceed with the next step only if validation is successful
                if (validateStep(currentStep)) {
                    currentStep.removeClass("active").next().addClass("active");
                    if (currentStep.is(':last-child')) {
                        $('#registrationForm').addClass('ready-to-submit');
                    } else {
                        $('#registrationForm').removeClass('ready-to-submit');
                    }
                }
            } else {
                // Perform other actions if the variable is not true for the second step
                alert("Verify OTP");
                // You can display a message or perform other actions here
            }
        } else {
            // For steps other than the second step, proceed without variable check
            if (validateStep(currentStep)) {
                currentStep.removeClass("active").next().addClass("active");
                if (currentStep.is(':last-child')) {
                    $('#registrationForm').addClass('ready-to-submit');
                } else {
                    $('#registrationForm').removeClass('ready-to-submit');
                }
            }
        }
    });


    $(".prev-btn").click(function (event) {
        event.preventDefault(); // Prevent form submission
        $(this).closest(".step-content").removeClass("active").prev().addClass("active");
        $('#registrationForm').removeClass('ready-to-submit');
    });

    function validateStep(step) {
        var inputs = step.find("input");
        var isValid = true;
        inputs.each(function () {
            if (!$(this).val()) {
                isValid = false;
                return false; // exit each loop early if a field is empty
            }
        });

        // Additional validation for OTP field
        if (step.attr('id') === 'step2') {
            var otp = $("#otp").val();
            if (!otp) {
                isValid = false;
            }
        }

        return isValid;
    }
});


// phone number validation

document.getElementById('validateButton').addEventListener('click', function () {
    var phoneNumberInput = document.getElementById('phoneNumber');
    var phoneNumber = phoneNumberInput.value.trim();

    // Regular expression to match 10-digit numbers
    var phoneNumberPattern = /^\d{10}$/;

    if (!phoneNumberPattern.test(phoneNumber)) {
        alert("Please enter a valid 10-digit phone number.");
        phoneNumberInput.focus(); // Focus on the input field
    } else {
        alert("Phone number is valid!");
        // Proceed with further actions if needed
    }
});
