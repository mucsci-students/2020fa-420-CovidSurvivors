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
    $.post(`${MODEL_NAME}/createForm`)
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
    $.post(`${MODEL_NAME}/editForm`, {class_name:classname})
        // load form inputs into class form
        .done(function (data) {
            $('#editClassForm').html(data);
            // Re-attach modal buttons
            createEditClassModalBtns();
        });
}

// =======================================================================

function loadRenameModelModal(model_name) {
    $('#renameModelModalOldNameInput').val(model_name)
}

// =======================================================================

function loadDeleteModelModal(model_name) {
    $('#deleteModelModalNameInput').val(model_name)
}

// =======================================================================

// autoselects a given class for the create relationship modal
function loadCreateRelationshipModal(class_name) {
    $(`#createRelationshipModelClassSelect`).val(class_name)
}

function loadEditRelationshipModal(relationship_type, class_name1, class_name2) {
    // Grab form from server
    $.post(`${MODEL_NAME}/editRelationshipForm`, {
            relationship_type:relationship_type,
            class_name1:class_name1,
            class_name2:class_name2
        })
        // load form inputs into class form
        .done(function (data) {
            $('#editRelationshipModalForm').html(data);
        });
    // load delete form
    $("#deleteRelationshipModalClass1").attr("value", class_name1)
    $("#deleteRelationshipModalClass2").attr("value", class_name2)
}

// =======================================================================

// Runs automatically when web application is executed
$(function() {
    classCardBtns();
    createEditClassModalBtns();
    drawRelationshipArrows();
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
            $.post(`${MODEL_NAME}/saveCardPosition`, {class_name:classname, x:x, y:y, zindex:zindex}) 
        },
        drag: function() {
            drawRelationshipArrows();
        }
    });
}

// =======================================================================

// draws the relationship arrows between cards
function drawRelationshipArrows() {

    // clear previous draw region
    $("#drawRegion").html("");
    // SVG canvas where the arrows are drawn
    var draw = SVG("#drawRegion");

    // arrow head for inheritance and realization arrows
    var realInherArrowHead = draw.marker(40, 20, function(add) {
        add.polyline([
            [0, 0],
            [10, 4],
            [0, 10],
            [0, 0]
        ]);
        this.fill('none').stroke({ width: 2, color: '#eeeeee' }).ref(0, 4).size(25, 25);
    });
    // arrow head for composition arrow
    var compArrowHead = draw.marker(30, 30, function(add) {
        add.rect(7, 7).cx(20).cy(15).fill('#eeeeee').stroke({ width: 1, color: '#eeeeee' }).transform({
            rotate: -135
        });
    });
    // arrow head for aggregation arrow
    var aggArrowHead = draw.marker(30, 30, function(add) {
        add.rect(7, 7).cx(20).cy(15).fill('none').stroke({ width: 1, color: '#eeeeee' }).transform({
            rotate: -135
        });
    });

    // for each class 
    for (var classname in classes) {
        // for each relationship
        var idClass1 = "#" + ($('.card[name="' + classname + '"]').attr('id'));
        for (var i in classes[classname].relationships) {
            var relationshipType = classes[classname].relationships[i]["type"];
            var class2 = classes[classname].relationships[i]["other"];
            var idClass2 = "#" + ($('.card[name="' + class2 + '"]').attr('id'));
            
            // calculates the path of the arrow
            var data = drawPath(idClass1, idClass2);
            var path = draw.path().fill('none').stroke({ width: 3, color: '#eeeeee' })

            // build SVG aggregation arrow 
            if (relationshipType == "aggregation") {
                // plot the path of the relationship arrow based on the draw Path data
                path.plot(data);
                // aggregation relationship arrow
                path.marker('end', aggArrowHead);
            } 
            // build SVG composition arrow 
            if (relationshipType == "composition") {
                // plot the path of the relationship arrow based on the draw Path data
                path.plot(data);
                // composition relationship arrow
                path.marker('end', compArrowHead);
            }
            // build SVG inheritance arrow 
            if (relationshipType == "inheritance") {
                // plot the path of the relationship arrow based on the draw Path data
                path.plot(data);
                // inheritance relationship arrow
                path.marker('end', realInherArrowHead);   
            } 
            // build SVG realization arrow 
            if (relationshipType == "realization") {
                // plot the path of the relationship arrow based on the draw Path data
                path.plot(data);
                // gives the arrow a dashed look
                path.attr('stroke-dasharray', 8);
                // realization relationship arrow
                path.marker('end', realInherArrowHead);
            }

            // allow path to be clicked to load the edit relationship modal
            path.attr('data-toggle',"modal")
            path.attr('data-target',"#editRelationshipModal")
            path.attr('onclick', `loadEditRelationshipModal('${relationshipType}', '${classname}', '${class2}')`)
        }
    }
}

// =======================================================================

// Calculates the length of the path for the arrow based on the card positions
function drawPath(card1, card2) {
    // controls the curvature of the arrow's path
    var weight = 0.68;
    // position of first class card
    var card1Pos = $(card1).offset();
    // outer height of the first class card
    var outerHeight1 = $(card1).outerHeight();
    // outer width of the first class card
    var outerWidth1 = $(card1).outerWidth();

    // position of second class card
    var card2Pos = $(card2).offset();
    
    // starting position from where the arrows are drawn
    // if the first class card is above the second class card, the arrow is
    // drawn from the the mid-bottom position of the first class card
    if (card1Pos.top < card2Pos.top) {
        // mid-bottom position of the first class card
        var x1 = (card1Pos.left) - (outerWidth1 / 2);
        var y1 = (card1Pos.top) + outerHeight1 - 2;
    } 
    // if the first class card is below the second class card, the arrow is
    // drawn from the the mid-top position of the first class card
    else {
        // mid-top position of the first class card
        var x1 = (card1Pos.left) - (outerWidth1 / 2);
        var y1 = (card1Pos.top) + 2;
    }
    
    // if the first class card is to the left of the second class card,
    // the arrow is drawn going to the left side of the second class card
    if (card1Pos.left < card2Pos.left) {
        // top left corner of the second class card
        var x4 = (card2Pos.left) - 200;
        var y4 = (card2Pos.top) - 20;
        // calculates the curvature of middle of the path
        var dx = Math.abs(x4 - x1) * weight;
        // makes the arrow point to the right
        var x3 = x4 - dx;
    } 
    // if the first class card is to the right of the second class card,
    // the arrow is drawn going to the right side of the second class card
    else {
        // top right corner of the second class card
        var x4 = (card2Pos.left) - 40;
        var y4 = (card2Pos.top) - 20;
        // calculates the curvature of middle of the path
        var dx = Math.abs(x4 - x1) * weight;
        // makes the arrow point to the left
        var x3 = x4 + dx;
    } 
    
    // the path of the arrow
    var data = `M${x1} ${y1} C ${x1} ${y1} ${x3} ${y4} ${x4} ${y4}`;

    return data;
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
            `<div class="input-group mb-3" id="method0">
                <select name="method_visibility" class="form-control">
                        <option selected>Public</option>
                        <option>Private</option>
                        <option>Protected</option>
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
    // Adds a text area for declaring a parameters name and type
    $('.form-group').on('click', '.addParameter', function() {
        var table = $(this).closest('.input-group');
        var method_index = table.prevAll().length-2;
        table.append(
            `<div class="input-group mb-3">
                <input hidden type="text" name="parameter_method" value="${method_index}">
                <input type="text" name="parameter_type" class="form-control" placeholder="Enter Parameter type" aria-label="Type of parameter" aria-describedby="basic-addon2">
                <input type="text" name="parameter_name" class="form-control" placeholder="Enter Parameter name" aria-label="Name of parameter" aria-describedby="basic-addon2">
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
