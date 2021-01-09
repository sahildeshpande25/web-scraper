// var data = {{ data | safe}};

function display(data) {

		var cols = Object.keys(data[0]);
		// console.log(cols)
		var headerRow = '';
		var bodyRows = '';
		cols.map(function(col) {
  			headerRow += '<th nowrap="nowrap">' + col + '</th>';
  		});
		data.map(function(row) {
  			bodyRows += '<tr>';
  			
  			cols.map(function(colName) {
  				bodyRows += '<td>' + row[colName] + '</td>';
			});

  			bodyRows += '</tr>';
		});

		document.getElementById('tabledata').innerHTML = '<table class="table table-hover"><thead class="table-dark" style="position: -webkit-sticky; position: sticky; top: 0; z-index: 2;"><tr>' +
		headerRow + '</tr></thead><tbody id="mytable">' +bodyRows + '</tbody></table>';

		document.getElementById('searchbar').innerHTML = '<input type="text" id="keyword" class="form-control mb-3" placeholder="Search by keyword">'

 		console.log('Success');
 	}
