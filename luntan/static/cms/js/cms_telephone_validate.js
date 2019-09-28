$(function () {
    $("#get_code").click(function (event) {
        event.preventDefault();
        email = $("#email").val();
        telephone = $("#telephone").val();
        console.log(telephone);
        console.log(email);

        if (!email && !telephone) {
            alert("信息填写不完整");
            return
        }


        $.ajax({
            url: "/cms/telephone_validate/",
            type: "post",
            dataType: "json",
            data: {
                "email": email,
                "telephone": telephone
            },
            success:function (data) {
                alert("ok")
            }

        })


    });


    $("#code_submit").click(function (event) {
        event.preventDefault();
        email = $("#email").val();
        validate_code = $("#validate_code").val();
        if(!validate_code && !email){
            alert("请输入邮箱或者验证码");
            return
        }

        $.ajax({
            url: "/cms/validate_code/",
            dataType: "json",
            type: "post",
            data: {
                "email": email,
                "validate_code": validate_code
            },
            success:function (data) {
                alert("OK")
            }
        })
    })

});