$(document).ready( function () {
    $('#table_id').DataTable( {
        "order": [[ 0, "desc" ]],
        "bLengthChange": false,
        "pageLength": 200,
        "bPaginate": false,
        "sDom": '<"top"if>rt<"clear">',
        "language": {
            "info": "_TOTAL_ name(s) total",
            "infoFiltered": " - _MAX_ name(s) total",
            "infoEmpty":"No names match this query"
        }
    });
});