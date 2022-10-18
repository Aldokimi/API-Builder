import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.less']
})
export class LoginPageComponent implements OnInit {

  constructor(private fb: FormBuilder) { }
  my_login_form!: FormGroup;

  
  isLoading = false;
  fieldTextType: boolean = false;

  ngOnInit(): void {
    this.my_login_form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });

  }

  onLoginFormSubmit(form: FormGroup): void {

    console.log(form.controls);

  }



toggleFieldTextType() {
  this.fieldTextType = !this.fieldTextType;
}

}
