function yammer_logout(callback) {
  // yam.platform.logout(function (response) {
  callback()
  // })
}

function connect_to_yammer() {
  yammer_logout(function() {
    setTimeout(function() {
      yam.platform.login(function(resp) {
        if (resp.access_token) {
          var user_container = $("#yammer-user")
          yam.platform.request({
            url: "users/current.json",
            method: "GET",
            data: {},
            success: function(user) {
              var first_name = user.first_name
              var last_name = user.last_name
              user_container.text(first_name + " " + last_name)
            }
          })
          var token = resp.access_token.token
          var form = user_container.parents("form").first()
          form.find('input[name="access_token"]').val(token)
          $("#yammer-remove").css("display", "inline-block")
          $(".yammer-only-from-default").css("display", "block")
        }
      })
    }, 1000)
  })
}

function remove_yammer_acount() {
  var form = $(this).parents("form").first()
  form.find('input[name="access_token"]').val("")
  $(this).css("display", "none")
  $(".yammer-only-from-default").css("display", "none")
  $("#yammer-user").text("")
}

$(document).on("click", "#yammer-login", connect_to_yammer)

$(document).on("click", "#yammer-remove", remove_yammer_acount)
