// Runs automatically when web application is executed
$(function() {
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

// Functionality for the create class and edit class modal buttons
function createEditClassModalBtns() {
    // Adds a new text area for the fields and methods 
    $('.form-group').on('click', '.addTextArea', function() {
        var table = $(this).closest('.form-group');
        table.append('<div class="input-group mb-3"><input type="text" class="form-control" placeholder="Enter name" aria-label="Name of field" aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary addTextArea" type="button"><i class="fas fa-plus"></i></button><button class="btn btn-outline-secondary delTextArea" type="button"><i class="fas fa-minus"></i></button></div>');
    });

    // Adds a new drop menu and text area for the relationships
    $('.form-group').on('click', '.addRelationship', function() {
        var table = $(this).closest('.form-group');
        table.append('<div class="input-group mb-3"><select id="inputRelationship" class="form-control"><option selected>Choose type...</option><option>Aggregation</option><option>Composition</option><option>Inheritance</option><option>Generalization</option></select><input type="text" class="form-control" placeholder="Enter associated class name" aria-label="Associated class" aria-describedby="basic-addon2"><div class="input-group-append"><button class="btn btn-outline-secondary addRelationship" type="button"><i class="fas fa-plus"></i></button><button class="btn btn-outline-secondary delTextArea" type="button"><i class="fas fa-minus"></i></button></div></div>');
    });

    // Deletes the fields, methods, or relationship text area that is no longer needed
    $('.form-group').on('click', '.delTextArea', function() {
        var table = $(this).closest('.form-group');
        if (table.find('input:text').length > 1) {
            $(this).closest('.input-group').remove();
        }
    });

    // Displays new class card
    $('#saveNewClass').click(function () {
        $('#display').prepend('<div class="card shadow" id="cardId1"><div class="card-header">New Card</div><div class="card-body"><ul class="list-group list-group-flush" id="fieldName"><li>Field 1</li></ul></div><div class="card-body"><ul class="list-group list-group-flush"><li>Method 1</li></ul></div><div class="card-body"><ul class="list-group list-group-flush"><li>Relationship <i class="fas fa-long-arrow-alt-right"></i> Class 2</li></ul></div><div class="card-footer nav justify-content-end nav-pills "><button type="button" class="btn btn-primary getID editCard" data-toggle="modal" data-target="#editClassModal"><i class="fas fa-edit"></i></button><button type="button" class="btn btn-primary getID" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-trash-alt"></i></button></div></div>');
        $("#createClassModal").modal('hide');
    });
}
