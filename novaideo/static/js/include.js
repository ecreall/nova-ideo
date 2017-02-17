
var includejs_resources = []

var includejs_resources_loaded = false

var resource_included = 0

var resource_to_include_nb = 0


function init_resource_loader(){
    includejs_resources_loaded = false
    resource_included = 0
    resource_to_include_nb = 0
}


function includejs(url, callback){
    window._lload(url, callback)
}


function includecss(url){
    var link = document.createElement("link")
    link.type = "text/css";
    link.rel="stylesheet";
    link.href = url;
    document.getElementsByTagName("head")[0].appendChild(link);
    resource_included += 1
}


function include_resources(urls, callback){
    function global_callback(err){
        resource_included += 1
        if(resource_included == resource_to_include_nb){
            callback()
            init_resource_loader()
        }
    }
    if(urls && urls.length>0){
        resource_to_include_nb = urls?urls.length: 0
        $.each(urls, function(){
          var parts = this.split('@'),
              type = parts[0],
              url = parts[1];
          if(type == 'css'){
            includecss(url)
          }

          if(type == 'js'){
            includejs(url, global_callback)
          }
          includejs_resources.push(url)  
        })
    }else{
        callback()
    }
}

function update_resources(){
    includejs_resources = $('script').map(function(){return $(this).attr('src')}).get()
    $.extend(includejs_resources, $('link').map(function(){return $(this).attr('href')}).get());
}

$(document).ready(function(){
  update_resources();
  $(document).trigger('resources_loaded')
})