$(document).ready( function () {
    $('#table_id').DataTable( {
        "order": [[ 0, "desc" ]],
        "bLengthChange": false,
        "pageLength": 200,
        "bPaginate": false,
        "sDom": '<"top"f>rt<"clear">'
    });
});