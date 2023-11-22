    window.onscroll = function() {myFunction()};

    function myFunction() {
        var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        var scrolled = (winScroll / height) * 100;
        document.getElementById("indicator").style.width = scrolled + "%";
    }

    (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = 'https://widgets.financewidget.com/loader.js';
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'financewidget-jssdk'));

//	async function fetchData() {
//		try {
//			// 비동기적으로 서버에서 데이터 가져오기
//			const response = await fetch('/your-model-endpoint/', {
//				method: 'GET',
//				credentials: 'include',  // CSRF 토큰을 함께 전송
//			});
//			const data = await response.json();
//
//			// 여러 기사에 대한 결과를 표시
//			data.result.forEach((summarize, index) => {
//				document.getElementById(`loading-screen-${index + 1}`).style.display = "none";
//				document.getElementById(`result-section-${index + 1}`).style.display = "block";
//				document.getElementById(`result-section-${index + 1}`).innerHTML = `<p>${summarize}</p>`;
//			});
//
//			// 확인용으로 모델 결과를 콘솔에 출력
//			console.log('Model result:', data.result);
//		} catch (error) {
//			console.error('Error fetching data:', error);
//		}
//		}
//
//		// fetchData 함수를 바로 호출하여 페이지 로딩시 실행
//	fetchData();
//	 fetchData 함수를 바로 호출하여 페이지 로딩시 실행
//	fetchData();

document.addEventListener("DOMContentLoaded", function () {
    // 초기 로드 시 홈 버튼의 위치에 맞게 언더라인 위치를 설정합니다.
    setUnderlinePosition(0); // 0은 홈 버튼의 인덱스입니다.

    // 스크롤 이벤트를 사용하여 네비게이션 바 고정 시 언더라인 위치를 조정하는 함수
    window.addEventListener("scroll", function () {
        var isNavFixed = isNavbarFixed(); // 네비게이션 바가 고정되었는지 여부 확인

        // 현재 활성화된 버튼의 인덱스를 가져와 언더라인 위치를 조정합니다.
        var activeButtonIndex = getActiveButtonIndex();
        setUnderlinePosition(activeButtonIndex, isNavFixed);
    });

    // 네비게이션 바 버튼을 클릭할 때마다 언더라인의 위치를 설정하는 함수입니다.
    function ul(index) {
        console.log('click!' + index);
        setUnderlinePosition(index, isNavbarFixed());
    }

    // 언더라인의 위치를 설정하는 함수입니다.
    function setUnderlinePosition(index, isNavFixed) {
        var underlines = document.querySelectorAll(".underline");
        var navButtons = document.querySelectorAll("nav a");

        if (index >= 0 && index < navButtons.length) {
            var buttonWidth = navButtons[index].offsetWidth; // 버튼의 너비 가져오기
            var buttonOffsetLeft = navButtons[index].offsetLeft; // 버튼의 왼쪽 위치 가져오기

            for (var i = 0; i < underlines.length; i++) {
                underlines[i].style.width = buttonWidth + "px"; // 언더라인의 너비 설정
                underlines[i].style.transition = 'none'; // 초기 로드 시 트랜지션 없이 설정

                // 네비게이션 바가 상단에 고정되어 있다면 상단에 마진 추가
                var topMargin = isNavFixed ? navButtons[index].offsetTop : 0;
                underlines[i].style.transform = 'translate3d(' + buttonOffsetLeft + 'px,' + topMargin + 'px,0)'; // 언더라인의 위치 설정
            }

            // Remove the 'active' class from all links
            for (var i = 0; i < navButtons.length; i++) {
                navButtons[i].classList.remove("active");
            }

            // Add the 'active' class to the clicked link
            navButtons[index].classList.add("active");

            // 다음 프레임에서 트랜지션을 다시 활성화합니다.
            setTimeout(function () {
                for (var i = 0; i < underlines.length; i++) {
                    underlines[i].style.transition = '';
                }
            }, 0);
        }
    }

    // 네비게이션 바가 상단에 고정되었는지 여부를 확인하는 함수
    function isNavbarFixed() {
        var navbar = document.querySelector("nav");
        var navbarRect = navbar.getBoundingClientRect();
        return navbarRect.top <= 0;
    }

    // 현재 활성화된 버튼의 인덱스를 가져오는 함수
    function getActiveButtonIndex() {
        var navButtons = document.querySelectorAll("nav a");
        for (var i = 0; i < navButtons.length; i++) {
            if (navButtons[i].classList.contains("active")) {
                return i;
            }
        }
        return 0; // 기본적으로 첫 번째 버튼을 반환합니다.
    }
});