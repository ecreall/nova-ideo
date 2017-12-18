function renderFilesSlider(files, id, activefile) {
  var slider = ""
  if (files.length > 0) {
    slider += '<div class="file-slider full">'
    slider +=
      '<div id="filecarousel-' +
      id +
      '" data-ride="" data-interval="3000" class="carousel slide">'
    slider += '<div role="listbox" class="carousel-inner">'
    slider += files
      .map(function(file, index) {
        var renderFile = ""
        renderFile += '<div class="item ' + (index == activefile ? "active": "") + '">'
        var url = file.content
        if (file.type === "img") {
          renderFile += '<img class="img-content" src="' + url + '"/>'
        }
        if (file.type === "flash") {
          renderFile +=
            '<object width="300" height="90" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=11,2,202,451" >'
          renderFile += '<param name="movie" value="' + url + '">'
          renderFile += '<param name="quality" value="high">'
          renderFile +=
            '<embed src="' +
            url +
            '" quality="high" class="img-content"  type="application/x-shockwave-flash"  pluginspage="http://www.macromedia.com/go/getflashplayer">'
          renderFile += "</embed></object>"
        }
        renderFile += "</div>"
        return renderFile
      })
      .join("")

    slider += "</div>"
    if (files.length > 1) {
      slider +=
        '<a class="left carousel-control" href="#filecarousel-' +
        id +
        '" role="button" data-slide="prev">'
      slider +=
        '<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>'
      slider += '<span class="sr-only">Previous</span>'
      slider += "</a>"
      slider +=
        '<a class="right carousel-control" href="#filecarousel-' +
        id +
        '" role="button" data-slide="next">'
      slider +=
        '<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>'
      slider += '<span class="sr-only">Next</span>'
      slider += "</a>"
    }
    slider += "</div>"
    slider += "</div>"
  }
  return slider
}
