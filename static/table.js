$(document).ready( function () {
    $.fn.dataTable.moment( 'MMM DD, YYYY @ HH:mm:ss A' );
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

$(document).ready( function () {
    $('#playercount').DataTable( {
        "bLengthChange": false,
        "pageLength": 100,
        "bPaginate": false,
        "language": {
            "info": "_TOTAL_ games total",
            "infoFiltered": " - _MAX_ games total",
            "infoEmpty": "No matching results",
            "search":"",
            "zeroRecords": "No matching results",
        'paging': false
        },
        // "columnDefs": {
        //     className: "dt-head-left"
        // }
    });
});