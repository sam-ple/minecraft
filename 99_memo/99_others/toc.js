javascript:(function(){
  let headings = document.querySelectorAll('h1,h2,h3,h4,h5,h6');
  let toc = document.createElement('div');
  toc.style.position = 'fixed';
  toc.style.top = '10px';
  toc.style.right = '10px';
  toc.style.backgroundColor = 'white';
  toc.style.border = '1px solid black';
  toc.style.padding = '10px';
  toc.style.maxHeight = '80%';
  toc.style.overflow = 'auto';
  toc.innerHTML = '<h3>Table of Contents</h3>';

  headings.forEach((h,i)=>{
    if(!h.id) h.id = 'heading-'+i;
    let a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;
    a.style.display = 'block';
    toc.appendChild(a);
  });
  document.body.appendChild(toc);
})();