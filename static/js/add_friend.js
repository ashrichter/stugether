function addFriend() {
    $.ajax({
        url : "{% url 'addFriend' %}", // the endpoint
        type : "POST", // http method
        data : { the_post : $('#post-text').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$("#test").textContent = "hello i am text";
        var frm = $('#friend-form');
        document.getElementById('test').textContent = "succfound formess";
        frm.submit(function (e) {
            e.preventDefault();
            document.getElementById('test').textContent = "sending";
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                success: function (data) {
                    document.getElementById('friend').textContent = "success";
                },
                error: function (data) {
                    document.getElementById('friend').textContent = "error";
                }
            });
            document.getElementById('test').textContent = "sent";
            return false;
        });