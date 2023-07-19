const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector('#emailField');
const emailfeedbackArea = document.querySelector('.emailfeedbackArea');
const passwordField = document.querySelector('#passwordField');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const showPasswordToogle = document.querySelector('.showPasswordToogle');
const submitBtn = document.querySelector('.submit-btn')

const handleToggleInput=(e)=>{
    if(showPasswordToogle.textContent === "SHOW"){
        showPasswordToogle.textContent = "HIDE";

        passwordField.setAttribute("type", "text");
    } else{
        showPasswordToogle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    } 
};

showPasswordToogle.addEventListener("click", handleToggleInput)


emailField.addEventListener('keyup', (e)=>{

    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailfeedbackArea.style.display = "none";

    if(emailVal.length > 0){
    fetch("/authentication/validate-email",{
        body: JSON.stringify({email: emailVal}),
        method:"POST",

    })
    .then(res=>res.json())
    .then(data=>{
        console.log('data', data)
        if(data.email_error){
            submitBtn.disabled = true;
            emailField.classList.add("is-invalid");
            emailfeedbackArea.style.display = "block";
            emailfeedbackArea.innerHTML=(data.email_error);
        } else{
            submitBtn.removeAttribute("disabled");
        }
    });
  } 

})





usernameField.addEventListener("keyup", (e) => {
    console.log('77777', 77777);

    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display = "block";

    usernameSuccessOutput.textContent= 'checking ' + (usernameVal )

    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";

    if(usernameVal.length > 0){
    fetch("/authentication/validate-usernames",{
        body: JSON.stringify({username: usernameVal}),
        method:"POST",

    })
    .then(res=>res.json())
    .then(data=>{
        usernameSuccessOutput.style.display = "none";
        if(data.username_error){
            submitBtn.disabled = true;
            usernameField.classList.add("is-invalid");
            feedbackArea.style.display = "block";
            feedbackArea.innerHTML=(data.username_error);
        } else{
            submitBtn.removeAttribute("disabled");
        }
    });
  } 
})
