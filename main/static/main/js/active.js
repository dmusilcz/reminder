$( '.navbar-nav li' ).on( 'click', function () {
	e.preventDefault();
	$( '.navbar-nav li').removeClass( 'active' );
	$( this ).addClass( 'active' );
});
