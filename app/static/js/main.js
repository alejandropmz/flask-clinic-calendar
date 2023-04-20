document.addEventListener("DOMContentLoaded", function () {
  const eliminar = document.getElementById("boton-eliminar");

  eliminar.addEventListener("click", (e) => {
    if (!confirm("¿Estás seguro de querer eliminar el registro?")) {
      e.preventDefault();
      e.stopPropagation();
    }
  });
});
