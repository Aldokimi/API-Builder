import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.less']
})
export class LoginPageComponent implements OnInit {

  constructor(private fb: UntypedFormBuilder) { }
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

    console.log(form.controls);

  }



toggleFieldTextType() {
  this.fieldTextType = !this.fieldTextType;
}

}
