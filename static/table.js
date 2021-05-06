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
            "infoEmpty": "No results",
            "search":"",
            "zeroRecords": "",
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
            "info": "",
            "infoFiltered": "",
            "infoEmpty": "",
            "search":"",
            "zeroRecords": "",
            "sDom": '<"top"if>t<"clear">',
        'paging': false
        },
        // "columnDefs": {
        //     className: "dt-head-left"
        // }
    });
});