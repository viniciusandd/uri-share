const tagContainer = document.querySelector('.tag-container');
const input = document.querySelector('.tag-container input');
const inputTarget = document.querySelector('#inputTagsDigitadas')

let tags = [];

function createTag(label) {
  const div = document.createElement('div');
  div.setAttribute('class', 'tag');
  const span = document.createElement('span');
  span.innerHTML = label;
  const closeIcon = document.createElement('i');
  closeIcon.innerHTML = ' x ';
  closeIcon.setAttribute('class', 'material-icons');
  closeIcon.setAttribute('data-item', label);
  div.appendChild(span);
  div.appendChild(closeIcon);
  return div;
}

function clearTags() {
  document.querySelectorAll('.tag').forEach(tag => {
    tag.parentElement.removeChild(tag);
  });
  inputTarget.value = "";
}

function addTags() {
  clearTags();
  tags.slice().reverse().forEach(tag => {
    tagContainer.prepend(createTag(tag));
    console.log(tag);
    inputTarget.value = inputTarget.value + tag + ",";
  });
}

input.addEventListener('keyup', (e) => {
    console.log(e.key);    
    var inputLenght = e.target.value.length;
    if (e.keyCode === 32) {
      if (inputLenght > 0) {
        e.target.value.split(',').forEach(tag => {
          tags.push(tag.trim());
        });
        
        addTags();
        input.value = '';        
      } else {
        bootbox.alert({
          message: "Não é possível criar uma tag sem nenhuma informação",
          size: 'large'
        });
      }
    } 
});

document.addEventListener('click', (e) => {
  console.log(e.target.tagName);
  if (e.target.tagName === 'I') {
    const tagLabel = e.target.getAttribute('data-item');
    const index = tags.indexOf(tagLabel);
    tags = [...tags.slice(0, index), ...tags.slice(index+1)];
    console.log(tags);
    addTags();    
  }
})

input.focus();

