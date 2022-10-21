import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.less']
})
export class LoginPageComponent implements OnInit {

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

  onLoginFormSubmit(form: UntypedFormGroup): void {

    this.authService.login(this.my_login_form.get('email')?.value, this.my_login_form.get('password')?.value)
      .subscribe((response) => {
        console.log(response);
      })

    

  }



  toggleFieldTextType() {
    this.fieldTextType = !this.fieldTextType;
  }

}
