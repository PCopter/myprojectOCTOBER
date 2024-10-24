console.log("certificate");

const subscriptionForm = document.querySelector('.subscription-form');

function certificationValidation(event){
    const checkedCertificationSet = document.querySelectorAll('input[name = "certification_set"]:checked')
    if(checkedCertificationSet.length === 0){
        event.preventDefault();
        alert('กรุณาเลือกอย่างน้อย 1 ข้อ')
    }
}

if(!!subscriptionForm){
    subscriptionForm.addEventListener('submit',certificationValidation);
}

// ---------horizontal-navbar-menu-----------
		var tabsNewAnim = $('#navbar-animmenu');
		var selectorNewAnim = $('#navbar-animmenu').find('li').length;
		//var selectorNewAnim = $(".tabs").find(".selector");
		var activeItemNewAnim = tabsNewAnim.find('.active');
		var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
		var itemPosNewAnimLeft = activeItemNewAnim.position();
		$(".hori-selector").css({
			"left":itemPosNewAnimLeft.left + "px",
			"width": activeWidthNewAnimWidth + "px"
		});
		$("#navbar-animmenu").on("click","li",function(e){
			$('#navbar-animmenu ul li').removeClass("active");
			$(this).addClass('active');
			var activeWidthNewAnimWidth = $(this).innerWidth();
			var itemPosNewAnimLeft = $(this).position();
			$(".hori-selector").css({
				"left":itemPosNewAnimLeft.left + "px",
				"width": activeWidthNewAnimWidth + "px"
			});
		});


		
// '.tbl-content' consumed little space for vertical scrollbar, scrollbar width depend on browser/os/platfrom. Here calculate the scollbar width .
		$(window).on("load resize ", function() {
		var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
		$('.tbl-header').css({'padding-right':scrollWidth});
  		}).resize();


// menu search bar 
		  function filterCards() {
			var input, filter, container, cards, card, i, txtValue;
			input = document.getElementById('searchInput');
			filter = input.value.toUpperCase();
			container = document.getElementById('cardContainer');
			cards = container.getElementsByClassName('card');
	
			for (i = 0; i < cards.length; i++) {
				card = cards[i];
				txtValue = card.getAttribute('data-name');
				if (txtValue.toUpperCase().indexOf(filter) > -1) {
					card.style.display = "";
				} else {
					card.style.display = "none";
				}
			}
		}
	
		function updateCardClasses() {
			var container = document.querySelector('.body-cardview .container');
			var cards = container.querySelectorAll('.card');
			var visibleCards = 0;
	
			cards.forEach(function(card) {
				if (card.style.display !== 'none') {
					visibleCards++;
				}
			});
	
			container.classList.remove('single-card', 'two-cards', 'three-cards','four-cards','five-cards');
	
			if (visibleCards === 1) {
				container.classList.add('single-card');
			} else if (visibleCards === 2) {
				container.classList.add('two-cards');
			} else if (visibleCards === 3) {
				container.classList.add('three-cards');
			}else if (visibleCards === 4) {
				container.classList.add('four-cards');
			}else if (visibleCards === 5) {
				container.classList.add('five-cards');
			}
		}

//clock


		






		