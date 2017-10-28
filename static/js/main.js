$(".button-collapse").sideNav();

$('#crear_contenedor').on('click', (ev)=>{

  ev.preventDefault();
  console.log($('form').serialize());
  $.ajax({
      method: "POST",
      url:"/stations",
      data: $('form').serialize(),
      dataType: 'json',
      success: function(response){ alert("Contenedor Agregado")},
      error: function(error){alert("Error al crear")}
  });

})
