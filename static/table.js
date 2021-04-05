$(document).ready( function () {
    $('#table_id').DataTable( {
        "order": [[ 0, "desc" ]],
        "bLengthChange": false,
        "pageLength": 200,
        "bPaginate": false,
        "sDom": '<"top"if>rt<"clear">',
        "language": {
            "info": "_TOTAL_ results",
            "infoFiltered": " - _MAX_ total",
            "infoEmpty": "No matching results",
            "search":"",
            "zeroRecords": "No matching results",
        'scrollY':'50vh',
        'scrollCollapse': true,
        'paging': false
        }
    });
});