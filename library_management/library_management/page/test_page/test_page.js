frappe.pages['test-page'].on_page_load = function(wrapper) {
	// var page = frappe.ui.make_app_page({
	// 	parent: wrapper,
	// 	title: 'test page',
	// 	single_column: true
	// });

	new Mypage(wrapper);


}
Mypage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			title: 'My Page',
			parent: wrapper, // HTML DOM Element or jQuery object
			single_column: true // create a page without sidebar
		})
		this.make();
	},

	make:function(){
		let me = $(this);

		// let body = `<h1>Hello, World</h1>`;

		let totals = function(){
			frappe.call({
				method: "library_management.api.frappe_test",
				callback: function(r) {
					console.log(r.message)
				}
			});
		}

		$(frappe.render_template(frappe.my_page.body, this)).appendTo(this.page.main)
		totals();
	}

})

let body = `
	<table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td id="test_id">Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
    </tr>
    
  </tbody>
</table>
`;

frappe.my_page = {
	body: body
}