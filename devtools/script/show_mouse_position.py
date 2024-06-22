def show_mouse_position():
    return '''
    (function(){ 

function luna_createMouseTrail() {
	  const trail = document.createElement('div');
	  trail.style.position = 'fixed';
	  trail.style.top = '0';
	  trail.style.left = '0';
	  trail.style.pointerEvents = 'none';
	  trail.style.zIndex = '9999';
	  trail.style.width = '10px';
	  trail.style.height = '10px';
	  trail.style.borderRadius = '50%';
	  trail.style.backgroundColor = 'black';
	  trail.style.opacity = '0.5';
	  trail.style.transition = 'transform 0.1s ease-out';
	
	  document.body.appendChild(trail);
	
	  const coordinates = document.createElement('div');
	  coordinates.style.position = 'fixed';
	  coordinates.style.top = '10px';
	  coordinates.style.right = '10px';
	  coordinates.style.background = '#fff';
	  coordinates.style.border = '1px solid #000';
	  coordinates.style.padding = '5px';
	  coordinates.style.userSelect = 'none'; // 禁止选中文字
	  coordinates.style.zIndex = '9999';
	
	  document.body.appendChild(coordinates);
	
	  document.addEventListener('mousemove', (event) => {
		const { clientX, clientY } = event;
		const x = clientX - 5;
		const y = clientY - 5;
		trail.style.transform = 'translate(' + x + 'px, ' + y + 'px)';
		const initialX = clientX;
		const initialY = clientY;
		const pageWidth = window.innerWidth;
		const offsetX = (clientX > window.innerWidth / 2) ? 20 : -80; // 偏移量
		coordinates.style.right = (window.innerWidth - initialX + offsetX) + 'px';
		coordinates.style.top = (initialY + 10) + 'px';
		coordinates.innerHTML = 'X: ' + clientX + ', Y: ' + clientY + '';
	  });
};
//
luna_createMouseTrail();

})();
    '''
