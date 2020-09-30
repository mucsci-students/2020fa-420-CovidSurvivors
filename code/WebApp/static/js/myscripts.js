$(function() {
    $(".card").draggable({
        cursor: "crosshair",
        opacity: 0.5,
        containment: "parent"
    });

    $(".card").addClass("shadow");
});