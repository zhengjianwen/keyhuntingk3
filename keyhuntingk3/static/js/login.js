   // 登录验证
    $(".login_btn").on("click",function () {

        $.ajax({
            url:"",
            type:"post",
            data:{
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
                user:$("#user").val(),
                pwd:$("#pwd").val(),
                valid_code:$("#valid_code").val(),
            },
            success:function (data) {
                console.log(data)
                if (data.state){
                    location.href="/index/"
                }
                else{
                     $(".error").text(data.msg)
                }

            }
        })

    })

    // 验证码刷新

    $("#valid_img").click(function () {
        $(this)[0].src+="?"
    });
