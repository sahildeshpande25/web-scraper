function search_table() {
  // Declare variables
  // var input, filter, table, tr, td, i, txtValue;
  // input = document.getElementById("keyword");
  // filter = input.value;
  // table = document.getElementById("mytable");
  // tr = table.getElementsByTagName("tr");

  // // Loop through all table rows, and hide those who don't match the search query
  // for (i = 0; i < tr.length; i++) {
  //   td = tr[i].getElementsByTagName("td")[2];
  //   if (td) {
  //     txtValue = td.textContent || td.innerText;
  //     if (txtValue.indexOf(filter) > -1) {
  //       tr[i].style.display = "";
  //     } else {
  //       tr[i].style.display = "none";
  //     }
  //   }
  // }
  var value = $(this).val().toLowerCase();
  console.log(value);
  $("#mytable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
}