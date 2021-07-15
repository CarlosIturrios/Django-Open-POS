miapp.productos.listar = function (argument) {

    miapp.dvmain.load("/static/mainapp/html/productos/listar.html", function () {
        var dvTitle = $("#dvTitle");
        dvTitle.text('Products');

        var cargar = function () {
            //cargar
            var dvMainCategories = $("#dvMainCategories");

            var prom = miapp.backend.ajax({
                method: "GET",
                url: "api/categories/",
            });
            var item = "";
            prom.done(function (data) {
                if (data.length === 0) {
                    console.log("count 0" + data);
                    item = "<div class=\"card\">";
                    item += "<div class=\"card-header card-header-danger\">";
                    item += "<h4 class=\"card-title\">Lo sentimos</h4>";
                    item += "<p class=\"card-category\">No existen categorias registradas";
                    item += " por favor contacta a tu supervisor</p>";
                    item += "</div>";
                    dvMainCategories.html(item);
                    return;
                }
                $.each(data, function (key, value) {
                    item += "<div class=\"col-sm-12 col-md-6 col-lg-3\">";
                    item += "<div class=\"card\">";
                    item += "<div class=\"card-header card-header-icon\">";
                    item += "<div class=\"card-icon\">";
                    item += "<a href=\"/#" + value.description + "\"><img class=\"img-responsive\" src=" + value.image + " width=\"100%\"";
                    item += "height=\"100%\" onclick=listarProductos('" + value.id + "')></a></div>";
                    item += "</div>";
                    item += "<div class=\"card-body\">";
                    item += "<h4 class=\"card-title\">" + value.description + "</h4>";
                    item += "</div>";
                    item += "<div class=\"card-footer\">";
                    item += "<div class=\"stats\">";
                    item += "Selecciona esta categoria para conocer la variedad de productos";
                    item += "</div>";
                    item += "</div>";
                    item += "</div>";
                    item += "</div>";
                    dvMainCategories.html(item);
                });

            });
            prom.fail(function (error) {
                console.log(error);
                alert("Lo siento hay un error intenta mas tarde");
            });
        };
        cargar();
    });
};
