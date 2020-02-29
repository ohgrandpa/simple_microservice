function add_to_basket()
{
    var product = $(".border-secondary").attr("name");

    var data = {
        quantity: $("#quantity").val(),
        product_id: product,
        customer_id: getCookie("customer_id")
    }

    $.ajax({
        url: "/add_item",
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json",
        complete: function(data) {
           redraw_cart(data);
        }
    });
}


function switch_customers()
{
    document.cookie = "customer_id=" + $(this).attr("name");
    $("#navbarDropdown").text($(this).text());
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function redraw_cart(data)
{
    customer_id = getCookie("customer_id");
    var req = $.get("/total",
        {
            customer_id: customer_id
        }
    );
    req.done(function(resp) {
        $("#total").text(resp.data);
    });
}

function toggle_border()
{
    var has_border = $(this).hasClass("border");
    console.log("border? " + has_border);
    $("img").each(
        function() {
            if($(this).hasClass("border")) {
                $(this).removeClass("border");
                $(this).removeClass("border-secondary");
            }
        }
    );
    if (!has_border) {
        $(this).addClass("border");
        $(this).addClass("border-secondary");
    }
}