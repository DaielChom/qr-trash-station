$(".button-collapse").sideNav();

$('#crear_contenedor').on('click', (ev)=>{

  ev.preventDefault();

  $.ajax({
      method: "POST",
      url:"/stations",
      data: $('form').serialize(),
      dataType: 'json',
      success: function(response){ alert("Contenedor Agregado"); location.reload(); },
      error: function(error){alert("Error al crear")}
  });

})
