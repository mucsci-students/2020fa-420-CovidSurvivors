// Runs automatically when web application is executed
$(function() {
    draggable("#cardId1");
    draggable("#cardId2");
    draggable("#cardId3");
});

// Gives class card the ability to be draggable and calculates
// the coordinates of the class card on the display  
function draggable(card) {
    $(card).draggable({
    cursor: "crosshair",
    opacity: 0.5,
    containment: "parent",
        // Calculates x and y coordinates of class card as you drag it
        drag: function() {
            var $this = $(this);
            var thisPos = $this.position();
            var parentPos = $this.parent().position();

            var x = thisPos.left - parentPos.left;
            var y = thisPos.top - parentPos.top;    
        }
    });
}
