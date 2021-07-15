miapp = {};
miStorage = window.localStorage;

$(function () {
    miapp.dvmain = $("#dvmain");

    Path.map("#/productos/listar").to(miapp.productos.listar);
    Path.map("#/dashboard/").to(miapp.dashboard.detalle);
    //Path.map("#/carrito/listar").to(miapp.dashboard.detalle);

    Path.root("#/dashboard/");

    Path.listen();
});
