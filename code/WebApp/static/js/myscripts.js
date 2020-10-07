// Saves the name to the delete class modal  
function setDeleteData(classname) {
    $('#deleteClassInputName').val(classname);
} 
 
// Loads the edit class modal form 
function loadEditClassModal(classname) {

    // Grab form from server
    $.post("/editForm", {class_name:classname})
        // load form inputs into class form
        .done(function (data) {
            $('#editClassForm').html(data)
            // Re-attach modal buttons
            createEditClassModalBtns();
        });
    

}

// Runs automatically when web application is executed
$(function() {
    classCardBtns();
    createEditClassModalBtns();
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

        //alert("Edit class: #" + getId);

    });
}

// Functionality for the create class and edit class modal buttons
function createEditClassModalBtns() {

     // Adds a new text area for the fields
     $('.form-group').on('click', '.addField', function() {
        var table = $(this).closest('.form-group');
        table.append('<div class="input-group mb-3"><input type="text" name="field_name" class="form-control" placeholder="Enter field name" aria-label="Name of field" aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary delTextArea" type="button"><i class="fas fa-minus"></i></button></div>');
    });

    // Adds a new text area for the methods 
    $('.form-group').on('click', '.addMethod', function() {
        var table = $(this).closest('.form-group');
        table.append('<div class="input-group mb-3"><input type="text" name="method_name" class="form-control" placeholder="Enter method name" aria-label="Name of field" aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary delTextArea" type="button"><i class="fas fa-minus"></i></button></div>');
    });

    // Adds a new drop menu and text area for the relationships
    $('.form-group').on('click', '.addRelationship', function() {
        var table = $(this).closest('.form-group');
        table.append('<div class="input-group mb-3"><select id="inputRelationship" class="form-control"><option>Aggregation</option><option>Composition</option><option>Inheritance</option><option>Realization</option></select><input type="text" class="form-control" placeholder="Enter associated class name" aria-label="Associated class" aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary delTextArea" type="button"><i class="fas fa-minus"></i></button></div></div>');
    });

    // Deletes the fields, methods, or relationship text area that is no longer needed
    $('.form-group').on('click', '.delTextArea', function() {
        var table = $(this).closest('.form-group');
        $(this).closest('.input-group').remove();
    });
}
