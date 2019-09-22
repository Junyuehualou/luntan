// 入口函数

$(function () {
    // 评论提交
    $("#comment_submit").click(function (event) {
        event.preventDefault();     //阻止默认触发事件
        user_comment = $(".comment_input").val();
        console.log(user_comment);
        // 判断是否有内容
        if (!user_comment) {
            alert('请输入评论内容');
            return
        }

        $.ajax({
            url:'/cms/comment',
            type: "post",
            contentType: "application/json",
            // headers: {
            //     "X-CSRFToken": getCookie("csrf_token")
            // },
            data: JSON.stringify({
                "user_comment": user_comment,
            }),
            success:function (data) {
                console.log(data)
            }


        })

    })


});
