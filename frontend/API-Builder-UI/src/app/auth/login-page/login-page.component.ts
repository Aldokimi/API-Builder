import { Component, OnInit, Output } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { error } from 'console';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.less']
})
export class LoginPageComponent implements OnInit {
  API_message:string = '';

  constructor(private fb: UntypedFormBuilder, private authService: AuthService, private router: Router) { }
  my_login_form!: UntypedFormGroup;
  isLoading = false;
  fieldTextType: boolean = false;

  ngOnInit(): void {
    this.my_login_form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });

  }

  onLoginFormSubmit(): void {
    this.API_message = '';
    this.isLoading = true
    this.authService.login(this.my_login_form.get('email')?.value, this.my_login_form.get('password')?.value)
      .subscribe(
        (response) => {
        console.log(response);
        this.isLoading = false;
        }
        ,(errorRes) => {
          this.isLoading =false;
          if(errorRes.status === 401)
              {this.API_message = "Email address or password are incorrect.";}
          else{
            this.API_message = "Unknown Error, Please try again later.";
          }
          console.log(errorRes.status)}
      )

    

  }



  toggleFieldTextType() {
    this.fieldTextType = !this.fieldTextType;
  }

}