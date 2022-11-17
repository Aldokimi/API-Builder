import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./../../../assets/css-js-login-signup/my-login.less']
})
export class RegisterPageComponent implements OnInit {

  constructor(private fb: UntypedFormBuilder, private authService : AuthService, private router:Router) { }
  my_register_form!: UntypedFormGroup;
  API_message! :string
  submitted = false;
  errorOccured = false;
  isLoading = false;
  fieldTextType: boolean = false;

  ngOnInit(): void {
    this.authService.isLoggedIn.subscribe(isLogged => {
      if (isLogged)
        this.router.navigate(['home'])
    })
    this.my_register_form = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });

  }

  onRegisterFormSubmit(): void {
    this.API_message = '';
    this.isLoading = true;
    this.submitted = true;
    this.authService.register(this.my_register_form.get('username')?.value,this.my_register_form.get('email')?.value, this.my_register_form.get('password')?.value)
    .subscribe(
      () => {
      this.isLoading = false;
      }
      ,(errorRes) => {
        this.isLoading =false;
        if(errorRes.error?.email)
            {this.API_message = errorRes.error?.email.join(', ');}
        else if(errorRes.error?.username)
        {this.API_message = errorRes.error?.email.username(', ');}
        else{
          this.API_message = "Unknown Error, Please try again later.";
        }
        console.log(errorRes.error)}
    )

  }



toggleFieldTextType() {
  this.fieldTextType = !this.fieldTextType;
}

}
