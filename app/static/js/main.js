window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 4000);


$(document).ready( function () {
    $('#table_id').DataTable();
} );

