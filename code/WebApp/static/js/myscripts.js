// Runs automatically when web application is executed
$(function() {
    classCardBtns();
});

// Gives class card the ability to be draggable and calculates
// the coordinates of the class card on the display  
function draggable(card) {
    $(card).draggable({
        stack: ".card",
        cursor: "crosshair",
        opacity: 0.5,
        containment: "parent",
        snap: true
    });
}

// Functionality for the class card buttons
function classCardBtns() {
    var getId;
    // Gets the unique ID of a class card
    $('.card-footer').on('click', '.getID', function () {
        getId = $($(this).closest('.card')).attr("id");
    });

    // Allows us to delete a specific class card on click of its delete button
    $('.delCard').click(function () {
        // removes the class card from dashboard along with all its content
        $("#" + getId).remove("#" + getId);
        // closes the delete modal that varifies if user wants to delete the selected class card
        $("#deleteModal").modal('hide');
        // displays a confirmation modal informing user the class card has been deleted
        $("#confirmModal").modal('show');
    });

    // Allows us to edit a specific class card on click of its edit button
    $('.card-footer').on('click', '.editCard', function () {
        // Get all the information pertaining to the class we wish to edit using the unique class ID

        // Preload the information we got into the appropriate textboxes of the edit Class Modal

        alert("Edit class: #" + getId);
    });
}
