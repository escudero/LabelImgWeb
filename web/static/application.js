var startResize = function() {
  $('#wrapperImage .boundingbox')
  .draggable({containment: "#wrapperImage", stop: update_struct})
  .resizable({containment: "#wrapperImage", handles: "all", stop: update_struct});
};
startResize();

var update_struct = function() {
  console.log('Oi');
  struct['boundingboxes'] = getBBPositions();
  update_debug();
}

var addTagBB = function(top, left, width, height, class_name) {
  let bbtag = '<div class="boundingbox" style="top: '+top+'px; left: '+left+'px; width: '+width+'px; height: '+height+'px;", data-classname="'+class_name+'"></div>'
  $("#wrapperImage").append(bbtag);
  struct['boundingboxes'].push({
    'top': top,
    'left': left,
    'width': width,
    'height': height,
    'class_name': class_name
  });
  update_debug();
  startResize();
}

var getBBPositions = function() {
  return $.map($('.boundingbox'), function(e) {
    let me = $(e);
    let pos = me.position();
    return {
      'top': pos['top'],
      'left': pos['left'],
      'width': me.outerWidth(),
      'height': me.outerHeight(),
      'class_name': me.data('classname')
    };
  });
}

$("#wrapperImage").dblclick(function(e) {
  let isBB = $(e.target).hasClass('ui-resizable');
  if(isBB && e.ctrlKey) {
    e.target.remove();
    update_struct();
  } else if(!isBB && !e.ctrlKey) {
    let top = e.offsetY;
    let left = e.offsetX;
    addTagBB(top, left, 100, 100, 'brand');
  }
  startResize();
});


var struct = {
  'image': null,
  'image_id': null,
  'boundingboxes': []
} 

var clean_bundingboxes = function() {
  struct['boundingboxes'] = [];
  $("#wrapperImage .boundingbox").remove();
  update_debug();
}

var add_image = function(data) {
  struct['image'] = data['image'];
  struct['image_id'] = data['image_id'];
  let img = $("#wrapperImage img");
  img.attr('src', struct['image']);
  img.data('imageid', struct['image_id']);
  update_debug();
}
var add_boundingbox = function(data) {
  clean_bundingboxes();
  $.each(data['boundingboxes'], function(_, bb) {
    addTagBB(bb['top'], bb['left'], bb['width'], bb['height'], bb['class_name']);
  });
  update_debug();
}

var get_change_image = function(direction) {
  let data = {
    'image_id': struct['image_id'],
    'direction': direction,
    _: new Date().getTime()
  };
  $.getJSON('/image_next', data, function(data) {
    add_image(data);
    add_boundingbox(data);
  });
  update_debug();
}

var save_boundingboxes = function() {
  $.ajax({
    type: "POST",
    url: '/save',
    data: {'data': JSON.stringify(struct)},
    success: function(data) {
      if(data['ret']) {
        $.jGrowl("Salvo com sucesso", { life: 2 * 1000 });
      } else {
        alert('ERRO ao salvar');
      }
    },
    dataType: 'json'
  });  
}

$("body").keydown(function(e) {
  if(e.keyCode == 37 || e.keyCode == 65) { // left or a
    get_change_image('back');
  }
  else if(e.keyCode == 39 || e.keyCode == 68) { // right or d
    get_change_image('forward');
  }
  else if(e.keyCode == 83) { // s
    save_boundingboxes('forward');
  }
});

var update_debug = function() {
  $('#containerDebug').text(JSON.stringify(struct, null, 2));
}
