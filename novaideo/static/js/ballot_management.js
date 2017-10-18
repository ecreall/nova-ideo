function render_end_vote() {
  return (
    '<div class="alert alert-info" role="alert">' +
    novaideo_translate("voteFinished") +
    ' <button class="reload-btn btn btn-xs btn-primary">' +
    novaideo_translate("Finish") +
    "</button>" +
    "</div>"
  )
}

function send_vote(event) {
  var $this = $(this)
  var panel = $($this.parents(".panel").first())
  var modal = $(panel.parents(".modal").first())
  var group = $($this.parents(".panel-group"))
  var button = $this.find('button.active[type="submit"]').last()
  var url = $(event.target).attr("action")
  $(button).addClass("disabled")
  var formData = new FormData($(this)[0])
  formData.append(button.val(), button.val())
  loading_progress()
  $.ajax({
    url: url,
    type: "POST",
    data: formData,
    contentType: false,
    processData: false,
    success: function(data) {
      var panel_to_remove = panel.find(".panel-collapse").first().attr("id")
      var source_body = $(
        "<div>" +
          jQuery.parseJSON($("#" + modal.data("source")).data("body")) +
          "</div>"
      )
      if (data.new_body) {
        alert_component({
          alert_msg: novaideo_translate(
            "There was a problem with your submission."
          ),
          alert_type: "error"
        })
        new_body = jQuery.parseJSON(data.new_body)
        source_body
          .find("#" + panel_to_remove)
          .find(".panel-body")
          .first()
          .html(new_body)
        panel.find(".panel-collapse .panel-body").html(new_body)
        $("#" + modal.data("source")).data(
          "body",
          JSON.stringify(source_body.html())
        )
      } else if (data.vote_body) {
        alert_component({
          alert_msg: novaideo_translate("Your vote has been validated"),
          alert_type: "success"
        })
        new_body = jQuery.parseJSON(data.vote_body)
        source_body
          .find("#" + panel_to_remove)
          .parents(".panel")
          .first()
          .replaceWith(new_body)
        panel.replaceWith(new_body)
        $("#" + modal.data("source")).data(
          "body",
          JSON.stringify(source_body.html())
        )
        var votes = $(group.find(".panel-title.collapsed"))
        if (votes.length > 0) {
          $(votes.first()).click()
        } else {
          modal.find(".modal-body>.panel-group").append(render_end_vote())
        }
      } else {
        source_body
          .find("#" + panel_to_remove)
          .parents(".panel")
          .first()
          .remove()
        panel.remove()
        $("#" + modal.data("source")).data(
          "body",
          JSON.stringify(source_body.html())
        )
        var votes = $(group.find(".panel-title.collapsed"))
        if (votes.length > 0) {
          $(votes.first()).click()
        } else {
          modal.modal("hide")
          location.reload()
        }
      }
      finish_progress()
    }
  })
  event.preventDefault()
}

function show_votes_modal(id) {
  var content = $("#" + id)
  var modal_container = $(".votes-modal-container")
  modal_container.data("source", id)
  modal_container.attr("class", "modal-l votes-modal-container modal fade")
  var action_body =
    '<div id="panel-actions-vote" class="panel-group">' +
    jQuery.parseJSON(content.data("body")) +
    "</div>"
  $(modal_container.find(".modal-body")).html(action_body)
  $(modal_container.find(".modal-title")).text(content.data("title"))
  try {
    deform.processCallbacks()
  } catch (err) {}
  modal_container.css("opacity", "1")
  modal_container.modal("show")
  $($("#panel-actions-vote").find("a.panel-title").first()).click()
}

$(document).on("submit", "form.vote-form", send_vote)

$(document).on("click", ".reload-btn", function() {
  location.reload()
})

$(document).on("click", ".vote-action", function() {
  show_votes_modal($(this).data("action_id"))
})
