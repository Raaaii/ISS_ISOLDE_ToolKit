// JavaScript code to handle copying the number when clicked
const numberToCopy = document.getElementById('copyNumber');
numberToCopy.addEventListener('click', () => {
  const tempInput = document.createElement('input');
  tempInput.value = numberToCopy.textContent;
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand('copy');
  document.body.removeChild(tempInput);
  alert('Number copied to clipboard: ' + numberToCopy.textContent);
});
