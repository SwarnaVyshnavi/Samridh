// function editAbout() {
//     var aboutText = document.getElementById('aboutText').innerText.trim();
//     document.getElementById('aboutTextArea').value = aboutText;
//     $('#editAboutModal').modal('show');
// }

// // Function to save the edited about section
// function saveAbout() {
//     var newAboutText = document.getElementById('aboutTextArea').value;
//     document.getElementById('aboutText').innerText = newAboutText;

//     // AJAX request to save the edited about section
//     $.ajax({
//         url: edit_sectionUrl,
//         type: 'POST',
//         data: {
//             section_name: 'About',  // Assuming the section name for about section is fixed
//             section_description: newAboutText,
//             reg_no: registration_number,
//             csrfmiddlewaretoken: '{{ csrf_token }}' // Include CSRF token
//         },
//         success: function (response) {
//             if (response.success) {
//                 // Optionally, you can perform additional actions upon successful save
//                 console.log('About section edited successfully');
//             } else {
//                 console.error('Failed to edit about section');
//             }
//         },
//         error: function (xhr, status, error) {
//             console.error('Error:', error);
//         }
//     });

//     $('#editAboutModal').modal('hide');
// }

function editAbout(key, value) {
    var aboutText = document.getElementById(key.toLowerCase()).innerText.trim();
    document.getElementById('editKey').value = key;
    document.getElementById('editValue').value = value;
    $('#editAboutModal').modal('show');
}

// Function to save the edited about section
function saveAbout() {
    var editedKey = document.getElementById('editKey').value;
    var newAboutText = document.getElementById('editValue').value;
    document.getElementById(editedKey.toLowerCase()).innerText = newAboutText;

    // AJAX request to save the edited about section
    $.ajax({
        url: edit_sectionUrl, // Replace with your backend endpoint URL
        type: 'POST',
        data: {
            section_name: editedKey,
            section_description: newAboutText,
            reg_no: registration_number,
            csrfmiddlewaretoken: '{{ csrf_token }}' // Include CSRF token
        },
        success: function (response) {
            if (response.success) {
                // Optionally, you can perform additional actions upon successful save
                console.log('Section edited successfully');
                window.location.reload();
            } else {
                console.error('Failed to edit section');
            }
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
            // Optionally, you can display an error message to the user
            alert('Error occurred while saving. Please try again later.');
        },
        complete: function () {
            $('#editAboutModal').modal('hide');
        }
    });
}


// Function to open the modal for adding a new section
function openAddSectionModal() {
    $('#addSectionModal').modal('show');
}

// Function to add a new section
function addNewSection() {
    var sectionName = document.getElementById('sectionName').value;
    var sectionDescription = document.getElementById('sectionDescription').value;

    // AJAX request to add a new section
    $.ajax({
        url: add_sectionUrl,
        type: 'POST',
        data: {
            section_name: sectionName,
            section_description: sectionDescription,
            reg_no: registration_number,
            csrfmiddlewaretoken: '{{ csrf_token }}' // Include CSRF token
        },
        success: function (response) {
            if (response.success) {
                // Optionally, you can perform additional actions upon successful save
                console.log('New section added successfully');
                window.location.reload();
            } else {
                console.error('Failed to add new section');
            }
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
        }
    });

    $('#addSectionModal').modal('hide');
}