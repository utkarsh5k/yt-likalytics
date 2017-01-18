list = []; 
var divs = document.getElementsByClassName('hotvideos-single-trend-title-container'); 
for (var i  = 0; i < divs.length; ++i) 
{ 
	div = divs[i]; a = div.getElementsByTagName('a')[0]; 
	href = a.title; 
	list.push(href) 
} 
console.log(list);