$(function () {

    $("#comment_submit").click(function (event) {
        event.preventDefault();
        user_comment = $("#comment_input").val();
        console.log(user_comment);
        new_id = $("#new_id").val();
        if (!user_comment) {
            alert('请输入评论内容');
            return
        }


        $.ajax({
            url: "/cms/comment/",
            type: "post",
            dataType: "json",
            data: {
                'user_comment': user_comment,
                'new_id': new_id,
            },
            success: function (data) {
                alert("评论成功");
                $("#comment_input").val("");
                location.reload()

            }
        });


    })


});