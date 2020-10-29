// Javascript/JQuery for the GUI UML Editor
// Course:   CSCI 420 - Software Engineering
// Authors:  Adisa, Amy, Carli, David, Joan
// Date:     October 21 2020
// =======================================================================

// Closes the popup status message box with the given ID
function closeFlashMessage(id) {
    $(id).remove();
}

// =======================================================================

// Saves the name to the delete class modal  
function setDeleteData(classname) {
    $('#deleteClassInputName').val(classname);
} 

// =======================================================================

// Loads the create class modal form 
// at the moment, the only loaded data is 
// for the dropdown that shows valid classes
function loadCreateClassModal() {

    // Grab form from server
    $.post("/createForm")
        // load form inputs into class form
        .done(function (data) {
            $('#createClassForm').html(data);
            // Re-attach modal buttons
            createEditClassModalBtns();
        });
    
}

// =======================================================================

// Loads the edit class modal form 
function loadEditClassModal(classname) {

    // Grab form from server
    $.post("/editForm", {class_name:classname})
        // load form inputs into class form
        .done(function (data) {
            $('#editClassForm').html(data);
            // Re-attach modal buttons
            createEditClassModalBtns();
        });

}

// =======================================================================

// Runs automatically when web application is executed
$(function() {
    classCardBtns();
    createEditClassModalBtns();
});

// =======================================================================

// Gives class card the ability to be draggable and calculates
// the coordinates of the class card on the display  
function draggable(card) {
    $(card).draggable({
        stack: ".card",
        cursor: "crosshair",
        opacity: 0.5,
        containment: "parent",
        snap: true,
        // sends x and y position of class card, along with its z-index, after the class card has been moved
        stop: function() {
            // name of class associated with the class card
            var classname = $($(this)).attr('name');
            // x coordinate representing the horizontal position of card on dashboard
            var x = $(card).css("left");
            // y coordinate representing the vertical position of card on dashboard
            var y = $(card).css("top");
            // the z-index specifing the stack order of the class cards on the dashboard
            var zindex = $(card).css("z-index");

            // sends class name and the appropriate position data of a class card to the server 
            $.post("/saveCardPosition", {class_name:classname, x:x, y:y, zindex:zindex}) 
        }
    });
}

// =======================================================================

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
}

// =======================================================================

// Functionality for the create class and edit class modal buttons
function createEditClassModalBtns() {

     // Adds a new text area for the fields
     $('.form-group').on('click', '.addField', function() {
        var table = $(this).closest('.form-group');
        table.append(
            `<div class="input-group mb-3">
                <select name="field_visibility" class="form-control">
                    <option>Public</option>
                    <option selected>Private</option>
                </select>
                <input type="text" name="field_type" class="form-control" placeholder="Enter field type" aria-label="Type of field" aria-describedby="basic-addon2">
                <input type="text" name="field_name" class="form-control" placeholder="Enter field name" aria-label="Name of field" aria-describedby="basic-addon2">
                <div class="input-group-append">
                    <button class="btn btn-outline-secondary delTextArea" type="button">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>`);
    });

    // Adds a new text area for the methods 
    $('.form-group').on('click', '.addMethod', function() {
        var table = $(this).closest('.form-group');
        table.append(
            `<div class="input-group mb-3">
                <select name="method_visibility" class="form-control">
                        <option selected>Public</option>
                        <option>Private</option>
                </select>
                <input type="text" name="method_type" class="form-control" placeholder="Enter method return type" aria-label="Type of method" aria-describedby="basic-addon2">
                <input type="text" name="method_name" class="form-control" placeholder="Enter method name" aria-label="Name of method" aria-describedby="basic-addon2">
                <div class="input-group-append">
                    <button class="btn btn-outline-secondary btn-sm addParameter" type="button">
                        Add Parameter
                    </button>
                    <button class="btn btn-outline-secondary delTextArea" type="button">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>`);
    });

    // wip
    // Adds a drop down menu and text area for declaring a parameters name and type
    $('form-group').on('click', '.addParameter', function() {
        var table = $(this).closest('.form-group');
        table.append(
            `<div class="input-group mb-3">
                <select name="parameter_type" id="inputRelationship" class="form-control">
                    <option>Type 1</option>
                    <option>Type 2</option>
                </select>
                <input type="text" name="parameter_name" class="form-control" placeholder="Enter Parameter name" aria-label="Name of parameter" aria-describedby="basic-addon2">
                <div class="input-group-append">
                    <button class="btn btn-outline-secondary delTextArea" type="button">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>`);
    });

    // Adds a new drop menu and text area for the relationships
    $('.form-group').on('click', '.addRelationship', function() {
        var table = $(this).closest('.form-group');
        table.append(
            `<div class="input-group mb-3">
                <select name="relationship_type" id="inputRelationship" class="form-control">
                    <option>Aggregation</option>
                    <option>Composition</option>
                    <option>Inheritance</option>
                    <option>Realization</option>
                </select>
                <input type="text" name="relationship_other" class="form-control" placeholder="Enter associated class name" aria-label="Associated class" aria-describedby="basic-addon2">
                <div class="input-group-append">
                    <button class="btn btn-outline-secondary delTextArea" type="button">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>`);
    });

    // Deletes the fields, methods, or relationship text area that is no longer needed
    $('.form-group').on('click', '.delTextArea', function() {
        var table = $(this).closest('.form-group');
        $(this).closest('.input-group').remove();
    });
}

// =======================================================================
