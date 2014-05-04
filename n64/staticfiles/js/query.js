$(document).ready(function(){
    
    var queryInfo;

    $('#runQueryButton').click(function(event){
        var query = $('#outputField').val() + " : " + $('#filterField').val();
        //$("#results-container").addClass('hidden');
        $.ajax({
            data: JSON.stringify({query: query}),
            contentType: 'application/json',
            success: function(dat) {

                var table = document.createElement('table');
                $(table).addClass('table table-hover results-table');
                var thead = document.createElement('thead');
                var trow = document.createElement('tr');
                $.each(dat.headers, function(i, item) {
                    var th = document.createElement('th');
                    $(th).text(item);
                    $(trow).append(th);
                });
                $(thead).append(trow);
                $(table).append(thead);

                var tbody = document.createElement('tbody');
                $(table).append(tbody);
                $.each(dat.results, function(i, item) {
                    var tr = document.createElement('tr');
                    $(tbody).append(tr);
                    $.each(item, function(i, it) {
                        var td = document.createElement('td');
                        $(tr).append(td);
                        $(td).text(it);
                    });
                });

                $("#results").empty();
                $("#results").append(table);
                $(table).dataTable();
                $("#results-container").removeClass('hidden');
            },
            type: 'POST',
            processData: false,
            url: "http://n64storageflask-env.elasticbeanstalk.com/query"
        });
    });

    $("#advanced").change(function(event){
        if ($("#queryFields").attr("disabled"))
            $("#queryFields").removeAttr("disabled");
        else
            $("#queryFields").attr("disabled", "disabled");
        $("#advanced").attr("disabled", "disabled");
    });

    //$.get("http://127.0.0.1:5000/query/info", function(data) {
        //queryInfo = data;
    //});
});

