

const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");

menuBtn.addEventListener("click", () => {
    sideMenu.style.display = 'block';
});
closeBtn.addEventListener("click", () => {
    sideMenu.style.display = 'none';
});




// Features.forEach(feature => {
//     const tr = document.createElement('tr');
//     const trContent = `
//                         <tr>
//                         <td>${feature.Feature1}</td>
//                         <td>${feature.value1}</td>
//                         <td>${feature.Feature2}</td>
//                         <td class="warning">${feature.value2}</td>
//                         </tr>
//                         `;
//     tr.innerHTML = trContent;
//     document.querySelector('table tbody').appendChild(tr);
// });