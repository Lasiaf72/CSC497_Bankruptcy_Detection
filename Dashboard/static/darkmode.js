let darkMode = localStorage.getItem('darkMode');
const darkModeToggle = document.querySelector('#darkModeToggle');



const enableDarkMode = () => {
    document.body.classList.add('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.remove('active');
    themeToggler.querySelector('span:nth-child(2)').classList.add('active');

    localStorage.setItem('darkMode', 'enabled');
};

const disablDarkMode = () => {
    document.body.classList.remove('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.add('active');
    themeToggler.querySelector('span:nth-child(2)').classList.remove('active');

    localStorage.setItem('darkMode', null);
};

if(darkMode === 'enabled') {
    enableDarkMode();
}

themeToggler.addEventListener("click", () => {
    darkMode = localStorage.getItem('darkMode');
    if(darkMode !== "enabled"){
        enableDarkMode();
    } else{
        disablDarkMode();
    }
    // document.body.classList.add('dark-theme-variables');

    
    // themeToggler.querySelector('span').classList.toggle('active');
});